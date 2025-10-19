# PWM Servo Test

This test verifies the PWM servo control functionality of the user project with 4 CF_TMR32 PWM timer instances.

## Test Overview

The test exercises servo control with standard RC servo PWM signals:
- **Frequency**: 50 Hz (20ms period)
- **Pulse widths**: 500us to 2500us (corresponding to servo positions -180° to +180°)

## Address Map

The design implements 4 PWM timers with Wishbone interfaces:
- **PWM0**: 0x30000000 (outputs to io_out[0])
- **PWM1**: 0x30010000 (outputs to io_out[1])
- **PWM2**: 0x30020000 (outputs to io_out[2])
- **PWM3**: 0x30030000 (outputs to io_out[3])

## Firmware Test Sequence

The C firmware performs the following sequence:

1. **Initialize GPIOs**: Configure all GPIOs as user outputs
2. **Enable User Interface**: Enable Wishbone interface to user project
3. **Signal Ready**: Set management GPIO to indicate configuration complete
4. **Test Phase 1**: Configure all PWMs to 18000 ticks (~1500us - neutral position)
5. **Test Phase 2**: Configure all PWMs to 6000 ticks (~500us - minimum position/-180°)
6. **Test Phase 3**: Configure all PWMs to 18000 ticks (~1500us - neutral position)
7. **Test Phase 4**: Configure all PWMs to 30000 ticks (~2500us - maximum position/+180°)

The firmware uses the management GPIO to signal phase transitions to the Python testbench.

## PWM Configuration

Each PWM is configured with the following parameters:
- **RELOAD**: 240000 (for 50 Hz at 12 MHz clock)
- **PRESCALE**: 0 (no prescaling)
- **CFG**: 0b110 (count up | periodic mode)
- **CMPX**: Variable (controls pulse width)
- **CMPY**: 2400000 (used for comparison)
- **PWM0CFG/PWM1CFG**: 0b000010000110 (match events configuration)
- **CTRL**: 0b1101 (enable timer, enable PWM0, enable PWM1, timer start)

### Register Offsets

Based on CF_TMR32 register map:
- 0x00: TMR (read-only timer value)
- 0x04: RELOAD
- 0x08: PR (prescaler)
- 0x0C: CMPX
- 0x10: CMPY
- 0x14: CTRL
- 0x18: CFG
- 0x1C: PWM0CFG
- 0x20: PWM1CFG

## Python Test Verification

The Python cocotb testbench:

1. **Waits for initialization**: Synchronizes with firmware using management GPIO
2. **Measures PWM pulse widths**: For each test phase, measures the actual PWM pulse width
3. **Verifies pulse width ranges**: Checks that measured pulse widths are within expected ranges
4. **Reports results**: Provides detailed pass/fail status for each PWM channel and phase

### Expected Pulse Width Ranges

The test uses tolerant ranges to account for timing variations:

- **Neutral (18000 ticks)**: 16000-20000 cycles
- **Minimum (6000 ticks)**: 4000-8000 cycles
- **Maximum (30000 ticks)**: 28000-32000 cycles

## Timing Calculations

With a 12 MHz clock (83.33ns period):
- **6000 ticks** = 500us (minimum servo position)
- **18000 ticks** = 1500us (neutral servo position)
- **30000 ticks** = 2500us (maximum servo position)
- **240000 ticks** = 20ms (50 Hz period for servos)

## Running the Test

From the project root:

```bash
cd verilog/dv/cocotb
caravel_cocotb -t pwm_servo_test -tag pwm_test
```

For gate-level simulation:
```bash
caravel_cocotb -t pwm_servo_test -tag pwm_test -sim GL
```

## Test Results

The test provides detailed logging including:
- Individual pulse width measurements
- Average pulse widths for each PWM channel
- Pass/fail status for each verification point
- Overall test summary with total passed/failed checks

## Expected Output

When the test passes, you should see:
```
[TEST] PWM0 average pulse width: 18000 cycles
[TEST] PWM1 average pulse width: 18000 cycles
[TEST] PWM2 average pulse width: 18000 cycles
[TEST] PWM3 average pulse width: 18000 cycles
...
[TEST] Test Summary: 16/16 checks passed
[TEST] PWM Servo Test PASSED
```

## Dependencies

- caravel_cocotb test environment
- CF_TMR32 IP (v2.0.0 or compatible)
- firmware_apis.h (Caravel firmware APIs)
