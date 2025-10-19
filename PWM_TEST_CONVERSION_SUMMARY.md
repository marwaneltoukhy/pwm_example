# PWM Servo Test Conversion Summary

## Overview

This document describes the conversion of the C firmware code to a complete cocotb-based verification test for the PWM servo control design.

## Original C Code Analysis

The original C firmware implements a servo control demo that:
1. Configures 4 PWM timers (CF_TMR32) at base addresses 0x30000000 to 0x30030000
2. Sequences through different servo positions using management GPIO as a state indicator
3. Uses register-level access via `csr_write_simple()` to configure timers

### Key Configuration Parameters

- **Clock**: 12 MHz (83.33ns period)
- **PWM Frequency**: 50 Hz (20ms period - standard for RC servos)
- **Reload Value**: 240000 (creates 20ms period)
- **Pulse Widths**:
  - 6000 ticks = 500us = -180° (minimum)
  - 18000 ticks = 1500us = 0° (neutral)
  - 30000 ticks = 2500us = +180° (maximum)

## Conversion Approach

### 1. Firmware Adaptation (pwm_servo_test.c)

**Changes made**:
- Replaced direct `csr_write_simple()` calls with `USER_writeWord()` from Caravel firmware APIs
- Simplified the `delay()` function to use `delay_cyc()` from firmware APIs
- Added proper initialization sequence:
  - `ManagmentGpio_outputEnable()` and `ManagmentGpio_write(0)`
  - `enableHkSpi(0)` to disable housekeeping SPI
  - `GPIOs_configureAll(GPIO_MODE_USER_STD_OUTPUT)` to configure GPIOs
  - `GPIOs_loadConfigs()` to load configuration
  - `User_enableIF()` to enable Wishbone interface
- Used management GPIO as handshake signal to synchronize with Python testbench
- Removed commented-out code and unused functions (multiply, divide, etc.)

**Test Sequence**:
1. Signal configuration complete (mgmt_gpio = 1)
2. Set neutral position (18000 ticks) → mgmt_gpio = 0
3. Wait for delay
4. Set minimum position (6000 ticks) → mgmt_gpio = 1
5. Wait for delay
6. Set neutral position (18000 ticks) → mgmt_gpio = 0
7. Wait for delay
8. Set maximum position (30000 ticks) → mgmt_gpio = 1
9. Wait for delay

### 2. Python Cocotb Test (pwm_servo_test.py)

**Key Features**:

- **Initialization**: Uses `test_configure()` to set up Caravel test environment
- **Synchronization**: Uses `wait_mgmt_gpio()` to synchronize with firmware phases
- **PWM Measurement**: Implements `measure_pwm_pulse()` function to measure actual pulse widths
- **Verification**: Implements `verify_pwm_range()` to check pulse widths against expected ranges
- **Self-Checking**: Automatically verifies all 4 PWM channels across 4 test phases (16 checks total)

**Test Flow**:
1. Wait for firmware initialization (`wait_mgmt_gpio(1)`)
2. For each test phase:
   - Wait for management GPIO transition
   - Allow PWM signals to stabilize (10000 clock cycles)
   - Measure PWM pulse widths (3 samples per channel)
   - Verify measurements are within expected range
3. Report final test summary

**Pulse Width Verification Ranges**:
- Neutral (18000): 16000-20000 cycles (±11% tolerance)
- Minimum (6000): 4000-8000 cycles (±33% tolerance)
- Maximum (30000): 28000-32000 cycles (±7% tolerance)

### 3. Test Configuration (pwm_servo_test.yaml)

Standard caravel-cocotb test configuration:
- Test name and description
- Timeout value (30M cycles to accommodate long delays)
- RTL and GL simulation configurations

### 4. Test Integration

Updated `cocotb_tests.py` to import the new test:
```python
from pwm_servo_test.pwm_servo_test import pwm_servo_test
```

## File Structure

```
verilog/dv/cocotb/pwm_servo_test/
├── pwm_servo_test.c          # Firmware (runs on management SoC)
├── pwm_servo_test.py         # Python cocotb testbench
├── pwm_servo_test.yaml       # Test configuration
└── README.md                 # Detailed test documentation
```

## Key Differences from Original Code

### Removed/Simplified
- Commented-out PWM configuration function (old version)
- Multiply and divide functions (not needed)
- Direct register manipulation via `reg_timer0_*` (replaced with firmware APIs)
- Infinite loop (converted to finite test sequence)

### Added
- Proper Caravel initialization sequence
- Management GPIO handshake for synchronization
- Python verification logic
- Self-checking test with pass/fail criteria
- Comprehensive logging and error reporting

## Register Map Reference

Each CF_TMR32 instance has the following registers (relative to base address):

| Offset | Register | Access | Description |
|--------|----------|--------|-------------|
| 0x00 | TMR | RO | Current timer value |
| 0x04 | RELOAD | WO | Reload/period value |
| 0x08 | PR | WO | Prescaler value |
| 0x0C | CMPX | WO | Compare X value (pulse width) |
| 0x10 | CMPY | WO | Compare Y value |
| 0x14 | CTRL | WO | Control register |
| 0x18 | CFG | WO | Configuration register |
| 0x1C | PWM0CFG | WO | PWM0 action configuration |
| 0x20 | PWM1CFG | WO | PWM1 action configuration |

### Control Register (CTRL) Bit Fields
- Bit 0: TE (Timer Enable)
- Bit 1: TS (Timer Start)
- Bit 2: P0E (PWM0 Enable)
- Bit 3: P1E (PWM1 Enable)

### Configuration Register (CFG) Bit Fields
- Bits [1:0]: DIR (Direction: 0=up, 1=down, 2=up-down)
- Bit 2: P (Periodic mode: 1=periodic, 0=one-shot)

## Running the Test

### Prerequisites
1. Caravel user project environment set up
2. caravel-cocotb installed
3. Design info configured: `python verilog/dv/setup-cocotb.py <project_root>`

### Execution
```bash
cd verilog/dv/cocotb
caravel_cocotb -t pwm_servo_test -tag pwm_test
```

### Expected Results
- Firmware should compile without errors
- Simulation should complete without timeout
- All 16 verification checks (4 PWMs × 4 phases) should pass
- Final message: "[TEST] PWM Servo Test PASSED"

## Verification Methodology

The test uses a **synchronization handshake** approach:

1. **Firmware Side**: Uses management GPIO to signal test phase transitions
2. **Python Side**: Monitors management GPIO and performs measurements/verification
3. **Self-Checking**: Python testbench automatically verifies PWM pulse widths

This approach ensures:
- Deterministic test execution
- Clear pass/fail criteria
- Detailed logging for debugging
- No manual waveform inspection required

## Potential Extensions

The test can be extended to:
1. Verify PWM period (20ms)
2. Test PWM1 outputs (currently only PWM0 outputs are routed to pins)
3. Verify interrupt generation on timer overflow
4. Test different prescaler and reload values
5. Verify PWM fault input functionality
6. Test dynamic PWM reconfiguration

## Troubleshooting

If the test fails:

1. **Check pulse width measurements**: Review log for actual measured values
2. **Verify timing**: Ensure clock frequency is 12 MHz in simulation
3. **Check GPIO routing**: Verify PWM outputs are correctly connected to io_out[3:0]
4. **Review firmware logs**: Check firmware compilation and execution logs
5. **Increase timeout**: If test times out, increase timeout_cycles parameter
6. **Adjust tolerances**: If measurements are close but outside range, adjust verification ranges

## Conclusion

The converted test provides:
- ✅ Comprehensive verification of 4 PWM channels
- ✅ Self-checking with clear pass/fail criteria
- ✅ Proper synchronization between firmware and testbench
- ✅ Detailed logging and error reporting
- ✅ Standard caravel-cocotb test structure
- ✅ Ready for CI/CD integration
