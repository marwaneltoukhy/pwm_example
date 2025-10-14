# Pad Mapping Documentation

## GPIO Pin Assignment

This document describes the mapping between the PWM peripherals and the Caravel GPIO pads (mprj_io).

## Default Pin Assignment

| GPIO Pin | Direction | Signal Name | Description |
|----------|-----------|-------------|-------------|
| io_out[0] | Output | pwm0_timer0 | PWM Timer 0, Channel 0 output |
| io_out[1] | Output | pwm0_timer1 | PWM Timer 1, Channel 0 output |
| io_out[2] | Output | pwm0_timer2 | PWM Timer 2, Channel 0 output |
| io_out[3] | Output | pwm0_timer3 | PWM Timer 3, Channel 0 output |
| io_out[7:4] | Output | Unused | Reserved for future use |

## Pin Configuration

All PWM output pins are configured as:
- **Direction**: Output
- **Output Enable (OEB)**: Low (0) - Output enabled
- **Drive Strength**: Standard CMOS push-pull
- **Voltage Level**: 1.8V (VCCD domain)

## Output Enable Configuration

The output enable is set in `user_project_wrapper.v`:

```verilog
assign io_oeb[7:0] = 8'b0;  // All pins 0-7 configured as outputs
```

## Pin Assignment Table

### Detailed Pin Mapping

| mprj_io Pin | User Signal | Peripheral | Channel | Notes |
|-------------|-------------|------------|---------|-------|
| mprj_io[0] | io_out[0] | PWM Timer 0 | pwm0 | Primary PWM output |
| mprj_io[1] | io_out[1] | PWM Timer 1 | pwm0 | Primary PWM output |
| mprj_io[2] | io_out[2] | PWM Timer 2 | pwm0 | Primary PWM output |
| mprj_io[3] | io_out[3] | PWM Timer 3 | pwm0 | Primary PWM output |
| mprj_io[4] | io_out[4] | - | - | Available for expansion |
| mprj_io[5] | io_out[5] | - | - | Available for expansion |
| mprj_io[6] | io_out[6] | - | - | Available for expansion |
| mprj_io[7] | io_out[7] | - | - | Available for expansion |

## Unused Signals

The following PWM outputs from CF_TMR32 are not currently routed to GPIO pads:
- **pwm1_timer0**: PWM Timer 0, Channel 1
- **pwm1_timer1**: PWM Timer 1, Channel 1
- **pwm1_timer2**: PWM Timer 2, Channel 1
- **pwm1_timer3**: PWM Timer 3, Channel 1

These signals can be connected if additional PWM outputs are needed.

## Fault Inputs

The PWM fault inputs (`pwm_fault`) are currently tied to logic 0 (no fault condition). These can be connected to GPIO inputs if external fault detection is required:

```verilog
// Current configuration (no external fault input)
wire pwm_fault_0 = 1'b0;
wire pwm_fault_1 = 1'b0;
wire pwm_fault_2 = 1'b0;
wire pwm_fault_3 = 1'b0;

// Example: To connect to GPIO input
// wire pwm_fault_0 = io_in[8];
```

## Modifying Pin Assignments

To change the pin mapping, edit the assignments in `verilog/rtl/user_project_wrapper.v`:

### Example: Moving PWM outputs to different pins

```verilog
// Original mapping
assign io_out[0] = pwm0_0;
assign io_out[1] = pwm0_1;
assign io_out[2] = pwm0_2;
assign io_out[3] = pwm0_3;

// Alternative mapping (moved to pins 8-11)
assign io_out[8] = pwm0_0;
assign io_out[9] = pwm0_1;
assign io_out[10] = pwm0_2;
assign io_out[11] = pwm0_3;

// Update OEB accordingly
assign io_oeb[11:8] = 4'b0;  // Enable outputs for pins 8-11
```

### Example: Adding second PWM channel outputs

```verilog
// Add PWM channel 1 outputs
assign io_out[0] = pwm0_0;  // Timer 0, Channel 0
assign io_out[1] = pwm1_0;  // Timer 0, Channel 1
assign io_out[2] = pwm0_1;  // Timer 1, Channel 0
assign io_out[3] = pwm1_1;  // Timer 1, Channel 1
assign io_out[4] = pwm0_2;  // Timer 2, Channel 0
assign io_out[5] = pwm1_2;  // Timer 2, Channel 1
assign io_out[6] = pwm0_3;  // Timer 3, Channel 0
assign io_out[7] = pwm1_3;  // Timer 3, Channel 1
```

## GPIO Pad Restrictions

### Reserved Pads
- **mprj_io[0]**: JTAG (normally available for user project)
- **mprj_io[1]**: SDO (SPI - should not be used unless housekeeping SPI is disabled)
- **mprj_io[2]**: SDI (SPI - should not be used unless housekeeping SPI is disabled)
- **mprj_io[3]**: CSB (SPI - should not be used unless housekeeping SPI is disabled)
- **mprj_io[4]**: SCK (SPI - should not be used unless housekeeping SPI is disabled)

### Analog Pads
- GPIO pads 0-6 do not have analog_io connections
- GPIO pads 7-37 support both digital and analog (via analog_io)
- Upper 2 GPIO pads (36-37) do not have analog_io

## Pad Configuration in Firmware

When using the PWM peripherals, configure the GPIO pads in firmware before enabling PWM:

```c
#include <defs.h>
#include <stub.c>

void main() {
    // Disable housekeeping SPI (if not needed)
    reg_spimaster_config = 0x00;
    
    // Configure GPIOs 0-3 as outputs for management SoC
    reg_mprj_io_0 = GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_1 = GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_3 = GPIO_MODE_USER_STD_OUTPUT;
    
    // Apply configuration
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);
    
    // Now configure and enable PWM peripherals...
}
```

## Testing Pin Connections

To verify pin connections during testing:
1. Configure PWM with known frequency and duty cycle
2. Use logic analyzer or oscilloscope on physical pins
3. Measure frequency and duty cycle
4. Compare with expected values from register configuration

## Notes

- All IO assignments should be verified before tape-out
- Unused outputs should be tied to a known state (typically 0)
- Consider signal integrity and EMI when assigning high-frequency PWM signals
- Group related signals together when possible
- Document any non-standard pin assignments clearly
