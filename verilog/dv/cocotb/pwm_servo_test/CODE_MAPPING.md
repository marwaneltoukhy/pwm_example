# Code Mapping: C Firmware to Python Cocotb

This document shows the direct mapping between the original C firmware and the Python cocotb test.

## Initialization Sequence

### Original C Code
```c
reg_gpio_mode1 = 1;
reg_gpio_mode0 = 0;
reg_gpio_ien = 1;
reg_gpio_oe = 1;
reg_wb_enable = 1;
configure_io();
reg_uart_enable = 1;
reg_la0_oenb = reg_la0_iena = 0x00000000;
```

### Converted Firmware (pwm_servo_test.c)
```c
ManagmentGpio_outputEnable();
ManagmentGpio_write(0);
enableHkSpi(0);
GPIOs_configureAll(GPIO_MODE_USER_STD_OUTPUT);
GPIOs_loadConfigs();
User_enableIF();
ManagmentGpio_write(1);  // Signal configuration complete
```

### Python Testbench (pwm_servo_test.py)
```python
caravelEnv = await test_configure(dut, timeout_cycles=30000000)
await caravelEnv.release_csb()
await caravelEnv.wait_mgmt_gpio(1)  # Wait for firmware ready
```

## PWM Configuration Function

### Original C Code
```c
csr_write_simple(disable, CSR_PWM0_BASE + 0x14L);       // Disable Timer
csr_write_simple(reload, CSR_PWM0_BASE + 0x04L);        // Reload
csr_write_simple(prescale, CSR_PWM0_BASE + 0x08L);      // Set prescale
csr_write_simple(config, CSR_PWM0_BASE + 0x18L);        // Set Cfg
csr_write_simple(p0_ticks, CSR_PWM0_BASE + 0x0cL);      // Cmpx
csr_write_simple(cmpy_value, CSR_PWM0_BASE + 0x10L);    // Cmpy
csr_write_simple(match, CSR_PWM0_BASE + 0x1cL);         // pwm0cfg
csr_write_simple(match, CSR_PWM0_BASE + 0x20L);         // pwm1cfg
csr_write_simple(enable, CSR_PWM0_BASE + 0x14L);        // Enable PWM
```

### Converted Firmware (pwm_servo_test.c)
```c
USER_writeWord(CSR_PWM0_BASE + 0x14L, disable);
USER_writeWord(CSR_PWM0_BASE + 0x04L, reload);
USER_writeWord(CSR_PWM0_BASE + 0x08L, prescale);
USER_writeWord(CSR_PWM0_BASE + 0x18L, config);
USER_writeWord(CSR_PWM0_BASE + 0x0cL, p0_ticks);
USER_writeWord(CSR_PWM0_BASE + 0x10L, cmpy_value);
USER_writeWord(CSR_PWM0_BASE + 0x1cL, match);
USER_writeWord(CSR_PWM0_BASE + 0x20L, match);
USER_writeWord(CSR_PWM0_BASE + 0x14L, enable);
```

### Python Verification
```python
# Python testbench doesn't write registers directly
# Instead, it monitors the PWM output pins and verifies behavior
pwm0_pin = dut.uut.mprj.io_out[0]
pulse_width = await measure_pwm_pulse(pwm0_pin)
```

## Test Sequence Mapping

### Original C Main Loop
```c
while (1) {
    reg_gpio_out = 1; // OFF
    config_pwm_ticks(18000, 18000, 18000, 18000);
    delay(_DELAY_VALUE);
    
    reg_gpio_out = 0;  // ON
    config_pwm_ticks(6000, 6000, 6000, 6000);
    delay(_DELAY_VALUE);
    
    reg_gpio_out = 1; // OFF
    config_pwm_ticks(18000, 18000, 18000, 18000);
    delay(_DELAY_VALUE);
    
    reg_gpio_out = 0;  // ON
    config_pwm_ticks(30000, 30000, 30000, 30000);
    delay(_DELAY_VALUE);
}
```

### Converted Firmware - Finite Sequence
```c
ManagmentGpio_write(0);
config_pwm_ticks(18000, 18000, 18000, 18000);  // Neutral
delay_cyc(_DELAY_VALUE);

ManagmentGpio_write(1);
config_pwm_ticks(6000, 6000, 6000, 6000);      // Minimum
delay_cyc(_DELAY_VALUE);

ManagmentGpio_write(0);
config_pwm_ticks(18000, 18000, 18000, 18000);  // Neutral
delay_cyc(_DELAY_VALUE);

ManagmentGpio_write(1);
config_pwm_ticks(30000, 30000, 30000, 30000);  // Maximum
delay_cyc(_DELAY_VALUE);

ManagmentGpio_write(0);  // Test complete
```

### Python Test Sequence
```python
# Phase 1: Neutral (18000)
cocotb.log.info("[TEST] Phase 1: Testing neutral position")
await caravelEnv.wait_mgmt_gpio(0)
await ClockCycles(caravelEnv.clk, 10000)
result1 = await verify_pwm_range(pwm0_pin, "PWM0", 16000, 20000)

# Phase 2: Minimum (6000)
cocotb.log.info("[TEST] Phase 2: Testing minimum position")
await caravelEnv.wait_mgmt_gpio(1)
await ClockCycles(caravelEnv.clk, 10000)
result5 = await verify_pwm_range(pwm0_pin, "PWM0", 4000, 8000)

# Phase 3: Neutral (18000)
cocotb.log.info("[TEST] Phase 3: Testing neutral position again")
await caravelEnv.wait_mgmt_gpio(0)
await ClockCycles(caravelEnv.clk, 10000)
result9 = await verify_pwm_range(pwm0_pin, "PWM0", 16000, 20000)

# Phase 4: Maximum (30000)
cocotb.log.info("[TEST] Phase 4: Testing maximum position")
await caravelEnv.wait_mgmt_gpio(1)
await ClockCycles(caravelEnv.clk, 10000)
result13 = await verify_pwm_range(pwm0_pin, "PWM0", 28000, 32000)
```

## PWM Measurement Implementation

### Original C Code
The original code doesn't verify PWM output - it just configures and runs.

### Python Verification Added
```python
async def measure_pwm_pulse(pin, timeout_cycles=500000):
    # Wait for rising edge
    await RisingEdge(caravelEnv.clk)
    for _ in range(timeout_cycles):
        if pin.value == 1:
            break
        await RisingEdge(caravelEnv.clk)
    
    # Measure high time
    high_time = 0
    for _ in range(timeout_cycles):
        if pin.value == 0:
            break
        high_time += 1
        await RisingEdge(caravelEnv.clk)
    
    return high_time

async def verify_pwm_range(pin, pwm_name, expected_min, expected_max, num_samples=3):
    pulse_widths = []
    for i in range(num_samples):
        pulse_width = await measure_pwm_pulse(pin)
        if pulse_width > 0:
            pulse_widths.append(pulse_width)
    
    avg_pulse_width = sum(pulse_widths) / len(pulse_widths)
    
    if expected_min <= avg_pulse_width <= expected_max:
        cocotb.log.info(f"[TEST] {pwm_name} pulse width PASSED")
        return True
    else:
        cocotb.log.error(f"[TEST] {pwm_name} pulse width FAILED")
        return False
```

## Configuration Values Mapping

### Original C Constants
```c
const int reload = 240000;      // 50 Hz period
const int prescale = 0;         // No prescaling
const int config = 0b110;       // Count up | periodic
const int cmpy_value = 2400000; // Compare Y
const int disable = 0b0000;     // Timer disabled
const int enable = 0b1101;      // TE | TS | P0E | P1E
const int match = 0b000010000110; // Match configuration
```

### Converted Firmware
Same values, just moved to local function scope:
```c
void config_pwm_ticks(int p0_ticks, int p1_ticks, int p2_ticks, int p3_ticks)
{
    const int reload = 240000;
    const int prescale = 0;
    const int config = 0b110;
    const int cmpy_value = 2400000;
    const int disable = 0b0000;
    const int enable = 0b1101;
    const int match = 0b000010000110;
    // ... configuration code ...
}
```

### Python Expected Values
```python
# Pulse width expected ranges (in clock cycles @ 12 MHz)
# Neutral (18000): 16000-20000 cycles
# Minimum (6000):  4000-8000 cycles
# Maximum (30000): 28000-32000 cycles
```

## Pin/Signal Mapping

### Original C Code
```c
reg_gpio_out = 1;  // Used as indicator
```

### Hardware Design (user_project_wrapper.v)
```verilog
assign io_out[0] = pwm0_0;  // PWM0 channel 0
assign io_out[1] = pwm0_1;  // PWM1 channel 0
assign io_out[2] = pwm0_2;  // PWM2 channel 0
assign io_out[3] = pwm0_3;  // PWM3 channel 0
```

### Python Test
```python
pwm0_pin = dut.uut.mprj.io_out[0]
pwm1_pin = dut.uut.mprj.io_out[1]
pwm2_pin = dut.uut.mprj.io_out[2]
pwm3_pin = dut.uut.mprj.io_out[3]
mgmt_gpio = dut.uut.chip_core.gpio
```

## Summary of Key Changes

| Aspect | Original C | Converted Firmware | Python Testbench |
|--------|-----------|-------------------|------------------|
| Register Access | `csr_write_simple()` | `USER_writeWord()` | Monitor outputs only |
| GPIO Control | `reg_gpio_out` | `ManagmentGpio_write()` | `wait_mgmt_gpio()` |
| Loop Structure | Infinite `while(1)` | Finite sequence | Phase-based verification |
| Delay | Custom `delay()` | `delay_cyc()` | `ClockCycles()` |
| Verification | None | None | Self-checking with ranges |
| Initialization | Direct register writes | Firmware API calls | `test_configure()` |
| Synchronization | None | Management GPIO | `wait_mgmt_gpio()` |
