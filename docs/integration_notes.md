# Integration Notes

## Overview

This document provides technical details for integrating and using the PWM example user project with the Caravel harness.

## System Architecture

### Clock and Reset

- **Clock Source**: `wb_clk_i` from Caravel management SoC
  - Typical frequency: 25 MHz (configurable via PLL)
  - Single clock domain (no CDC required)
  
- **Reset**: `wb_rst_i` from Caravel
  - Active HIGH synchronous reset
  - Reset is applied to all PWM peripherals simultaneously

### Bus Interface

#### Wishbone B4 Classic Protocol

All PWM peripherals are accessed via the Wishbone B4 classic bus interface. The design uses a custom bus splitter to decode addresses and route transactions to the appropriate peripheral.

**Key Timing Characteristics:**
- Single-cycle read latency (registered outputs)
- One-cycle acknowledgment per transaction
- No wait states under normal operation
- Address decoding based on bits [19:16] for 4 peripherals

**Supported Features:**
- 32-bit data bus
- 32-bit address bus
- 4-bit byte lane selection (wbs_sel_i)
- Word-aligned accesses
- Byte-lane writes supported

#### Address Decoding

The `wishbone_bus_splitter` module decodes addresses as follows:

```
Address Range             Peripheral Selected
0x3000_0000 - 0x3000_FFFF → PWM Timer 0
0x3001_0000 - 0x3001_FFFF → PWM Timer 1
0x3002_0000 - 0x3002_FFFF → PWM Timer 2
0x3003_0000 - 0x3003_FFFF → PWM Timer 3
Out of range              → Bus error (wbs_err_o asserted)
```

**Decoder Implementation:**
```verilog
wire [1:0] sel = wbs_adr_i[19:16];
wire [BITS-1:0] ADDR_MASK = 32'hFFFF_0000;
```

### Interrupt System

#### Interrupt Routing

Three interrupt lines are routed from PWM peripherals to Caravel:
- `user_irq[0]` ← PWM Timer 0 interrupt
- `user_irq[1]` ← PWM Timer 1 interrupt
- `user_irq[2]` ← PWM Timer 2 interrupt

Note: PWM Timer 3 interrupt (irq_3) is not currently connected to user_irq due to the 3-bit limitation.

#### Interrupt Sources

Each PWM timer can generate interrupts on:
- **TO (Timeout)**: Timer reaches RELOAD (up count) or 0 (down count)
- **MX (Match X)**: Timer matches CMPX register
- **MY (Match Y)**: Timer matches CMPY register

#### Interrupt Handling

1. Enable desired interrupt sources via IM register (offset 0xFF00)
2. Check MIS register (offset 0xFF04) to read masked interrupt status
3. Service the interrupt
4. Clear interrupt flag by writing to IC register (offset 0xFF0C)

Example:
```c
// Enable timeout interrupt for PWM Timer 0
write32(0x30000000 + 0xFF00, 0x01);  // IM: Enable TO

// In ISR: Check which interrupt fired
uint32_t status = read32(0x30000000 + 0xFF04);  // MIS
if (status & 0x01) {
    // Handle timeout interrupt
    write32(0x30000000 + 0xFF0C, 0x01);  // IC: Clear TO
}
```

## PWM Generation

### Basic PWM Configuration

To generate a PWM signal:

1. **Configure Timer Prescaler** (PR register)
   - Determines timer counting frequency
   - Timer_freq = Clock_freq / (PR + 1)

2. **Set Timer Period** (RELOAD register)
   - Defines PWM period
   - PWM_freq = Timer_freq / RELOAD

3. **Set Duty Cycle** (CMPX or CMPY register)
   - Determines pulse width
   - Duty_cycle = CMPX / RELOAD × 100%

4. **Configure PWM Actions** (PWM0CFG or PWM1CFG)
   - Define output behavior on timer events
   - Typical: High on zero, Low on compare match

5. **Set Counting Mode** (CFG register)
   - Up counting: 0b10
   - Down counting: 0b01
   - Up/Down counting: 0b11
   - Periodic vs. One-shot mode

6. **Enable Timer and PWM** (CTRL register)
   - Set TE (Timer Enable)
   - Set P0E or P1E (PWM Enable)

### Example: 1 kHz PWM at 50% Duty Cycle

Assuming 25 MHz system clock:

```c
#define PWM_BASE 0x30000000

// Step 1: Set prescaler for 25 kHz timer frequency
// 25 MHz / (999 + 1) = 25 kHz
write32(PWM_BASE + 0x0008, 999);

// Step 2: Set period for 1 kHz PWM
// 25 kHz / 25 = 1 kHz
write32(PWM_BASE + 0x0004, 25);

// Step 3: Set duty cycle to 50%
// 25 * 0.5 = 12.5 ≈ 12
write32(PWM_BASE + 0x000C, 12);

// Step 4: Configure PWM actions
// E0=10 (High on zero), E1=01 (Low on CMPX match)
write32(PWM_BASE + 0x001C, 0x24);

// Step 5: Set up-counting, periodic mode
write32(PWM_BASE + 0x0018, 0x06);

// Step 6: Enable timer and PWM0
write32(PWM_BASE + 0x0014, 0x05);
```

### Advanced PWM Features

#### Complementary PWM with Deadtime

For motor control and H-bridge applications:

```c
// Enable both PWM channels with deadtime
write32(PWM_BASE + 0x0024, 10);      // PWMDT: 10 cycles deadtime
write32(PWM_BASE + 0x0014, 0x1D);    // CTRL: Enable timer, PWM0, PWM1, DTE
```

#### PWM Inversion

Invert PWM output polarity:

```c
// Invert PWM0 output
uint32_t ctrl = read32(PWM_BASE + 0x0014);
ctrl |= (1 << 5);  // Set PI0 bit
write32(PWM_BASE + 0x0014, ctrl);
```

## Simulation and Testing

### Caravel-Cocotb Testing

#### Test Environment Setup

1. **Setup Caravel-Cocotb**:
   ```bash
   cd /workspace/pwm_example
   python verilog/dv/setup-cocotb.py /workspace/pwm_example
   ```

2. **Add RTL Files to Includes**:
   Edit `verilog/includes/includes.rtl.caravel_user_project`:
   ```
   -v $(USER_PROJECT_VERILOG)/rtl/user_project_wrapper.v
   -v $(USER_PROJECT_VERILOG)/rtl/wb_bus_splitter.v
   -v $(USER_PROJECT_VERILOG)/../ip/CF_TMR32/hdl/rtl/CF_TMR32_WB.v
   -v $(USER_PROJECT_VERILOG)/../ip/CF_TMR32/hdl/rtl/CF_TMR32.v
   ```

3. **Run Tests**:
   ```bash
   cd verilog/dv/cocotb
   caravel_cocotb -t pwm_test -tag pwm_rtl
   ```

#### Test Structure

Firmware (C) side:
```c
#include <firmware_apis.h>

void main() {
    // Initialize management GPIO
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    // Configure GPIOs for PWM outputs
    // ... GPIO configuration ...
    
    // Enable user interface
    User_enableIF();
    
    // Signal testbench: configuration done
    ManagmentGpio_write(1);
    
    // Configure and test PWM
    // ... PWM test logic ...
}
```

Testbench (Python) side:
```python
from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb

@cocotb.test()
@report_test
async def pwm_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10_000_000)
    await caravelEnv.release_csb()
    
    # Wait for firmware to complete configuration
    await caravelEnv.wait_mgmt_gpio(1)
    
    # Monitor PWM outputs and verify behavior
    # ... test logic ...
```

### Expected Results

**RTL Simulation:**
- PWM outputs should appear on io_out[3:0]
- Frequency and duty cycle should match register configuration
- Interrupts should fire at expected times

**Waveform Analysis:**
- Check PWM period matches: Period = (PR + 1) × RELOAD / Clock_freq
- Verify duty cycle: Duty = CMPX / RELOAD
- Confirm interrupt timing aligns with timer events

## Debug and Troubleshooting

### Common Issues

#### No PWM Output

**Possible Causes:**
1. Timer or PWM not enabled in CTRL register
2. GPIO not configured as output in firmware
3. PWM action configuration incorrect
4. RELOAD or CMPX values are 0

**Debug Steps:**
1. Verify CTRL register: TE=1, P0E=1 (or P1E=1)
2. Check GPIO configuration in firmware
3. Verify PWM0CFG/PWM1CFG settings
4. Confirm RELOAD > 0 and CMPX <= RELOAD

#### Incorrect Frequency

**Possible Causes:**
1. Prescaler (PR) miscalculated
2. RELOAD value incorrect
3. Clock frequency assumption wrong

**Debug Steps:**
1. Measure actual clock frequency
2. Recalculate: PWM_freq = Clock_freq / ((PR+1) × RELOAD)
3. Verify register writes completed successfully

#### Interrupts Not Firing

**Possible Causes:**
1. Interrupt not enabled in IM register
2. Interrupt flag already set (needs clearing)
3. Timer not running

**Debug Steps:**
1. Read RIS register to check raw interrupt status
2. Verify IM register has correct bits set
3. Clear IC register before starting timer
4. Confirm timer is enabled (TE bit in CTRL)

### Debugging Tools

**Simulation:**
- VCD waveforms: `sim/<tag>/rtl-<test>/waves.vcd`
- Firmware log: `sim/<tag>/rtl-<test>/firmware.log`
- Test log: `sim/<tag>/rtl-<test>/test.log`

**Register Readback:**
Most registers are write-only and read back as 0. Only TMR, RIS, and MIS can be read for debugging.

**Logic Analyzer:**
The Caravel logic analyzer (la_data_in/out) can be used to observe internal signals if needed.

## Performance Characteristics

### Timing

- **Register Access Latency**: 1 cycle (read), immediate (write)
- **PWM Resolution**: Determined by (RELOAD + 1) steps
- **Minimum PWM Frequency**: Clock_freq / (65536 × 65536) with max prescaler
- **Maximum PWM Frequency**: Clock_freq / 2 with PR=0, RELOAD=1

### Resource Utilization

Per CF_TMR32_WB instance (from OpenLane2 synthesis):
- **Standard Cells**: ~1669 cells
- **Maximum Frequency**: ~63 MHz (with Wishbone wrapper)
- **Area**: TBD after place & route

Total for 4 instances:
- **Estimated Cells**: ~6700 cells
- **Plus bus splitter**: ~100 cells
- **Total**: ~6800 cells

## References

- CF_TMR32 IP Documentation: `/nc/ip/CF_TMR32/v2.1.0-nc/README.md`
- CF_TMR32 Datasheet: `/nc/ip/CF_TMR32/v2.1.0-nc/CF_TMR32.pdf`
- Caravel Documentation: https://caravel-harness.readthedocs.io/
- Wishbone B4 Specification: https://opencores.org/howto/wishbone

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-14 | 1.0 | Initial documentation |
