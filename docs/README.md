# PWM Example - Caravel User Project

## Initial User Prompt
"This repo has RTL for a PWM, I want to test this RTL using caravel-cocotb, also create documentation"

## Project Objectives
The goal of this project is to:
1. Test the existing PWM RTL design using caravel-cocotb verification framework
2. Create comprehensive documentation for the PWM user project
3. Ensure the design is fully verified and ready for integration with Caravel

## Project Overview
This Caravel user project implements four independent PWM (Pulse Width Modulation) timer peripherals using the CF_TMR32 IP core. Each PWM peripheral:
- Supports dual PWM outputs (pwm0 and pwm1)
- Has configurable period, duty cycle, and prescaler
- Provides interrupt capabilities
- Is accessible via Wishbone B4 classic bus interface
- Occupies a 64KB address space

## Design Architecture

### Components
1. **user_project_wrapper**: Top-level wrapper connecting to Caravel
2. **wishbone_bus_splitter**: Address decoder and bus multiplexer for 4 peripherals
3. **CF_TMR32_WB** (x4): Four instances of PWM timer peripherals with Wishbone interface

### Address Map
- **PWM Timer 0**: 0x3000_0000 - 0x3000_FFFF (64KB)
- **PWM Timer 1**: 0x3001_0000 - 0x3001_FFFF (64KB)
- **PWM Timer 2**: 0x3002_0000 - 0x3002_FFFF (64KB)
- **PWM Timer 3**: 0x3003_0000 - 0x3003_FFFF (64KB)

### IO Mapping
- **io_out[0]**: PWM Timer 0 output (pwm0)
- **io_out[1]**: PWM Timer 1 output (pwm0)
- **io_out[2]**: PWM Timer 2 output (pwm0)
- **io_out[3]**: PWM Timer 3 output (pwm0)

### Interrupt Mapping
- **user_irq[0]**: PWM Timer 0 interrupt
- **user_irq[1]**: PWM Timer 1 interrupt
- **user_irq[2]**: PWM Timer 2 interrupt

## Requirements
- Verify PWM functionality using caravel-cocotb
- Test all four PWM instances
- Verify Wishbone bus protocol compliance
- Verify PWM output signals
- Verify interrupt generation
- Document register map and usage

## Current Status
- **Phase**: Documentation and Testing Setup
- **Next Steps**: 
  1. Link CF_TMR32 IP with firmware
  2. Setup caravel-cocotb environment
  3. Create functional tests
  4. Run verification

## Directory Structure
```
pwm_example/
├── docs/                           # Documentation
│   ├── README.md                   # This file
│   ├── register_map.md            # Register descriptions
│   ├── pad_map.md                 # IO pad assignments
│   └── integration_notes.md       # Integration guide
├── verilog/
│   ├── rtl/                       # RTL source files
│   │   ├── user_project_wrapper.v
│   │   └── wb_bus_splitter.v
│   ├── dv/                        # Design verification
│   │   └── cocotb/               # Cocotb tests
│   └── includes/                  # Include file lists
├── ip/                            # IP cores
│   └── CF_TMR32/                 # PWM Timer IP
└── openlane/                      # OpenLane configuration
```

## References
- CF_TMR32 IP Documentation: See `ip/CF_TMR32/docs/`
- Caravel Documentation: https://caravel-harness.readthedocs.io/
- Wishbone B4 Specification: https://opencores.org/howto/wishbone
