# Register Map Documentation

## Address Space Overview

The PWM Example user project provides four independent PWM timer peripherals. Each peripheral occupies a 64KB address window.

| Peripheral | Base Address | Address Range | Description |
|------------|--------------|---------------|-------------|
| PWM Timer 0 | 0x3000_0000 | 0x3000_0000 - 0x3000_FFFF | First PWM Timer |
| PWM Timer 1 | 0x3001_0000 | 0x3001_0000 - 0x3001_FFFF | Second PWM Timer |
| PWM Timer 2 | 0x3002_0000 | 0x3002_0000 - 0x3002_FFFF | Third PWM Timer |
| PWM Timer 3 | 0x3003_0000 | 0x3003_0000 - 0x3003_FFFF | Fourth PWM Timer |

## CF_TMR32 Register Map

Each PWM timer peripheral (CF_TMR32_WB) has the following register map. All offsets are relative to the peripheral's base address.

### Core Registers

| Register Name | Offset | Access | Reset Value | Description |
|---------------|--------|--------|-------------|-------------|
| TMR | 0x0000 | R | 0x00000000 | Current timer value (read-only) |
| RELOAD | 0x0004 | W | 0x00000000 | Timer reload value (terminal count for up, initial for down) |
| PR | 0x0008 | W | 0x00000000 | Prescaler register; Timer freq = Clock freq / (PR + 1) |
| CMPX | 0x000C | W | 0x00000000 | Compare register X (for PWM generation) |
| CMPY | 0x0010 | W | 0x00000000 | Compare register Y (for PWM generation) |
| CTRL | 0x0014 | W | 0x00000000 | Control register |
| CFG | 0x0018 | W | 0x00000000 | Configuration register |
| PWM0CFG | 0x001C | W | 0x00000000 | PWM0 configuration register |
| PWM1CFG | 0x0020 | W | 0x00000000 | PWM1 configuration register |
| PWMDT | 0x0024 | W | 0x00000000 | PWM deadtime register |
| PWMFC | 0x0028 | W | 0x00000000 | PWM fault clear register |

### Interrupt Registers

| Register Name | Offset | Access | Reset Value | Description |
|---------------|--------|--------|-------------|-------------|
| IM | 0xFF00 | W | 0x00000000 | Interrupt mask (1=enable, 0=disable) |
| MIS | 0xFF04 | R | 0x00000000 | Masked interrupt status |
| RIS | 0xFF08 | R | 0x00000000 | Raw interrupt status |
| IC | 0xFF0C | W | 0x00000000 | Interrupt clear (W1C - write 1 to clear) |

### Clock Gating Register

| Register Name | Offset | Access | Reset Value | Description |
|---------------|--------|--------|-------------|-------------|
| GCLK | 0xFF10 | W | 0x00000000 | Gated clock enable (1=enable, 0=disable) |

## Register Detailed Descriptions

### CTRL Register (Offset: 0x0014)

Control register for timer and PWM operation.

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 0 | TE | 1 | Timer Enable (1=enabled, 0=disabled) |
| 1 | TS | 1 | Timer re-Start (write 1 then 0 to restart in one-shot mode) |
| 2 | P0E | 1 | PWM0 Enable (1=enabled, 0=disabled) |
| 3 | P1E | 1 | PWM1 Enable (1=enabled, 0=disabled) |
| 4 | DTE | 1 | Deadtime Enable (1=enabled, 0=disabled) |
| 5 | PI0 | 1 | Invert PWM0 output (1=inverted, 0=normal) |
| 6 | PI1 | 1 | Invert PWM1 output (1=inverted, 0=normal) |
| 31:7 | - | 25 | Reserved (must be 0) |

### CFG Register (Offset: 0x0018)

Configuration register for timer behavior.

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 1:0 | DIR | 2 | Count Direction: 10=Up, 01=Down, 11=Up/Down |
| 2 | P | 1 | Mode: 1=Periodic, 0=One-Shot |
| 31:3 | - | 29 | Reserved (must be 0) |

### PWM0CFG Register (Offset: 0x001C)

PWM0 action configuration for various timer events.

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 1:0 | E0 | 2 | Action on zero match: 00=None, 01=Low, 10=High, 11=Invert |
| 3:2 | E1 | 2 | Action on CMPX match (up): 00=None, 01=Low, 10=High, 11=Invert |
| 5:4 | E2 | 2 | Action on CMPY match (up): 00=None, 01=Low, 10=High, 11=Invert |
| 7:6 | E3 | 2 | Action on RELOAD match: 00=None, 01=Low, 10=High, 11=Invert |
| 9:8 | E4 | 2 | Action on CMPY match (down): 00=None, 01=Low, 10=High, 11=Invert |
| 11:10 | E5 | 2 | Action on CMPX match (down): 00=None, 01=Low, 10=High, 11=Invert |
| 31:12 | - | 20 | Reserved (must be 0) |

### PWM1CFG Register (Offset: 0x0020)

PWM1 action configuration (same format as PWM0CFG).

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 1:0 | E0 | 2 | Action on zero match: 00=None, 01=Low, 10=High, 11=Invert |
| 3:2 | E1 | 2 | Action on CMPX match (up): 00=None, 01=Low, 10=High, 11=Invert |
| 5:4 | E2 | 2 | Action on CMPY match (up): 00=None, 01=Low, 10=High, 11=Invert |
| 7:6 | E3 | 2 | Action on RELOAD match: 00=None, 01=Low, 10=High, 11=Invert |
| 9:8 | E4 | 2 | Action on CMPY match (down): 00=None, 01=Low, 10=High, 11=Invert |
| 11:10 | E5 | 2 | Action on CMPX match (down): 00=None, 01=Low, 10=High, 11=Invert |
| 31:12 | - | 20 | Reserved (must be 0) |

### PWMDT Register (Offset: 0x0024)

PWM deadtime register for generating complementary PWM signals with deadband (useful for H-bridge drivers).

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 7:0 | PWMDT | 8 | Deadtime value in clock cycles |
| 31:8 | - | 24 | Reserved (must be 0) |

### PWMFC Register (Offset: 0x0028)

PWM fault clear register.

| Bit | Field | Width | Description |
|-----|-------|-------|-------------|
| 15:0 | PWMFC | 16 | Write any value to clear PWM fault condition |
| 31:16 | - | 16 | Reserved (must be 0) |

## Interrupt Flags

The interrupt system uses four registers: IM, RIS, MIS, and IC.

### Interrupt Flag Definitions

| Bit | Flag | Width | Description |
|-----|------|-------|-------------|
| 0 | TO | 1 | Timeout - TMR matches 0 (down count) or RELOAD (up count) |
| 1 | MX | 1 | Match X - TMR matches CMPX register |
| 2 | MY | 1 | Match Y - TMR matches CMPY register |
| 31:3 | - | 29 | Reserved |

### Interrupt Register Operations

- **IM (0xFF00)**: Write 1 to enable interrupt source, 0 to disable
- **RIS (0xFF08)**: Read current interrupt flags (raw status, regardless of mask)
- **MIS (0xFF04)**: Read masked interrupt status (RIS & IM)
- **IC (0xFF0C)**: Write 1 to clear the corresponding interrupt flag

## Example Register Access

### Example 1: Configure Simple PWM

To generate a 50% duty cycle PWM at 1 kHz with a 25 MHz clock:

```c
// Base address for PWM Timer 0
#define PWM0_BASE 0x30000000

// Calculate values for 1 kHz PWM
// Timer frequency = 25MHz / (PR + 1) = 25kHz for PR=999
// RELOAD = 25 for 1kHz (25kHz / 25 = 1kHz)
// CMPX = 12 for 50% duty cycle

write32(PWM0_BASE + 0x0008, 999);      // PR: Prescaler = 999
write32(PWM0_BASE + 0x0004, 25);       // RELOAD: Period = 25
write32(PWM0_BASE + 0x000C, 12);       // CMPX: Compare = 12 (50%)
write32(PWM0_BASE + 0x0018, 0x6);      // CFG: Up count (10b), Periodic (1b)
write32(PWM0_BASE + 0x001C, 0x24);     // PWM0CFG: High on zero, Low on CMPX
write32(PWM0_BASE + 0x0014, 0x05);     // CTRL: Enable timer and PWM0
```

### Example 2: Enable Interrupts

```c
// Enable timeout interrupt
write32(PWM0_BASE + 0xFF00, 0x01);     // IM: Enable TO interrupt

// Clear any pending interrupts
write32(PWM0_BASE + 0xFF0C, 0x07);     // IC: Clear all interrupt flags
```

## Notes

- All registers are 32-bit word-aligned
- Reserved bits should always be written as 0
- All write-only registers read back as 0x00000000
- Byte-lane writes are supported via the Wishbone sel_i signals
- Clock gating is disabled by default (GCLK should be set to 1 for normal operation)
