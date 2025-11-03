# Architecture Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Descriptions](#component-descriptions)
- [Bus Architecture](#bus-architecture)
- [Memory Organization](#memory-organization)
- [Interrupt Architecture](#interrupt-architecture)
- [Clock and Reset](#clock-and-reset)
- [Power Architecture](#power-architecture)

---

## Overview

The PWM Example project implements a multi-channel PWM controller with integrated memory, designed as a Caravel user project. The architecture follows a hierarchical design with clear separation of concerns:

- **Top Level:** `user_project_wrapper` (Caravel integration layer)
- **System Level:** `user_project` (main functional module)
- **Peripheral Level:** PWM timers and SRAM banks
- **Infrastructure:** Wishbone bus interconnect

---

## System Architecture

### Hierarchy

```
user_project_wrapper (Caravel interface)
    │
    └── user_project (Main system)
            │
            ├── wishbone_bus_splitter (1→7 decoder)
            │       │
            │       ├─→ PWM0 (CF_TMR32_WB) → pwm0, pwm1
            │       ├─→ PWM1 (CF_TMR32_WB) → pwm2, pwm3
            │       ├─→ PWM2 (CF_TMR32_WB) → pwm4, pwm5
            │       ├─→ PWM3 (CF_TMR32_WB) → pwm6, pwm7
            │       ├─→ SRAM0 (CF_SRAM_1024x32_wb_wrapper)
            │       ├─→ SRAM1 (CF_SRAM_1024x32_wb_wrapper)
            │       └─→ SRAM2 (CF_SRAM_1024x32_wb_wrapper)
            │
            └── Interrupt aggregation logic
```

### Data Flow

1. **Wishbone Master → Bus Splitter**
   - Caravel management SoC initiates transactions
   - Address, data, and control signals propagate

2. **Bus Splitter → Peripherals**
   - Address decoder selects target peripheral
   - Transaction routed to selected slave

3. **Peripheral Processing**
   - PWM timers: Update registers, generate PWM
   - SRAM: Execute read/write operations

4. **Response Path**
   - Peripheral generates acknowledgment
   - Data (if read) returned to master
   - Bus splitter routes response back

5. **PWM Outputs**
   - Timer compare logic generates PWM signals
   - Signals routed to GPIO pins via wrapper

6. **Interrupt Path**
   - PWM interrupts generated on events
   - Aggregated to 2 user IRQ lines
   - Routed to Caravel interrupt controller

---

## Component Descriptions

### 1. user_project_wrapper

**Purpose:** Caravel integration layer

**Key Features:**
- Interfaces with Caravel SoC infrastructure
- Provides Wishbone slave interface
- Routes GPIO signals to/from user_project
- Manages power connections (VPWR/VGND)
- Implements logic analyzer connections

**Port Summary:**
- Wishbone: Standard B4 Classic slave
- GPIO: 38 bidirectional I/O pins
- Logic Analyzer: 128 probes
- Power: VPWR, VGND, VDD3V3, VSS

### 2. user_project

**Purpose:** Main functional module

**Module Instantiation:**
- 1× wishbone_bus_splitter
- 4× CF_TMR32_WB (pwm0-pwm3)
- 3× CF_SRAM_1024x32_wb_wrapper (sram0-sram2)

**Parameters:**
```verilog
parameter ADDR_WIDTH = 32
parameter DATA_WIDTH = 32
```

**Key Signals:**
```verilog
// Clock & Reset
input  wire wb_clk_i
input  wire wb_rst_i

// Wishbone Interface
input  wire wbs_stb_i
input  wire wbs_cyc_i
input  wire wbs_we_i
input  wire [3:0] wbs_sel_i
input  wire [31:0] wbs_dat_i
input  wire [31:0] wbs_adr_i
output wire wbs_ack_o
output wire [31:0] wbs_dat_o

// Interrupts
output wire [2:0] user_irq

// PWM Outputs
output wire [7:0] pwm_out
```

### 3. wishbone_bus_splitter

**Purpose:** Address-based bus multiplexer

**Configuration:**
```verilog
.NUM_PERIPHERALS(7)
.ADDR_MASK(32'hFFFF_0000)  // Upper 16 bits for decoding
```

**Address Mapping:**
| Peripheral | Base Address | Size |
|------------|--------------|------|
| PWM0 | 0x3000_0000 | 64KB |
| PWM1 | 0x3001_0000 | 64KB |
| PWM2 | 0x3002_0000 | 64KB |
| PWM3 | 0x3003_0000 | 64KB |
| SRAM0 | 0x3004_0000 | 64KB |
| SRAM1 | 0x3005_0000 | 64KB |
| SRAM2 | 0x3006_0000 | 64KB |

**Operation:**
1. Compare incoming address with each base address
2. Activate corresponding peripheral select
3. Route data and control signals
4. Multiplex acknowledgment back to master

### 4. CF_TMR32_WB (×4)

**Purpose:** 32-bit timer with dual PWM outputs

**Configuration:**
```verilog
.PRW(16)  // 16-bit prescaler width
```

**Key Features:**
- 32-bit up-counter
- Programmable period register
- Two independent compare registers
- Edge-aligned PWM generation
- Interrupt on overflow/match
- Fault input (unused, tied to 0)

**Register Map (per instance):**
| Offset | Register | Width | Function |
|--------|----------|-------|----------|
| 0x00 | CTRL | 32 | Control and status |
| 0x04 | PRE | 16 | Clock prescaler |
| 0x08 | PERIOD | 32 | Timer period |
| 0x0C | CMP0 | 32 | Compare 0 (PWM0) |
| 0x10 | CMP1 | 32 | Compare 1 (PWM1) |
| 0x14 | COUNT | 32 | Current count (RO) |
| 0x18 | IRQ | 32 | Interrupt status |

**PWM Generation Logic:**
```
if (counter < compare_value)
    pwm_output = 1
else
    pwm_output = 0

if (counter >= period)
    counter = 0
    generate_interrupt()
```

### 5. CF_SRAM_1024x32_wb_wrapper (×3)

**Purpose:** 1KB SRAM with Wishbone interface

**Configuration:**
```verilog
.WIDTH(12)  // 12-bit address = 1024 words
```

**Memory Organization:**
- 1024 words × 32 bits = 4KB
- Single-port synchronous SRAM
- Registered outputs
- Byte-select for partial writes

**Access Timing:**
| Cycle | Operation |
|-------|-----------|
| T0 | Address/data presented, STB/CYC asserted |
| T1 | SRAM reads/writes, ACK asserted |
| T2 | Read data valid, transaction complete |

---

## Bus Architecture

### Wishbone B4 Classic

**Protocol Characteristics:**
- **Type:** Synchronous, single-clock-edge
- **Mode:** Classic (non-pipelined)
- **Data Width:** 32 bits
- **Address Width:** 32 bits
- **Byte Granularity:** Yes (via SEL)

**Signal Description:**

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| `wb_clk_i` | 1 | Input | Clock |
| `wb_rst_i` | 1 | Input | Synchronous reset |
| `wbs_adr_i` | 32 | Input | Address |
| `wbs_dat_i` | 32 | Input | Write data |
| `wbs_dat_o` | 32 | Output | Read data |
| `wbs_we_i` | 1 | Input | Write enable |
| `wbs_sel_i` | 4 | Input | Byte select |
| `wbs_stb_i` | 1 | Input | Strobe |
| `wbs_cyc_i` | 1 | Input | Cycle |
| `wbs_ack_o` | 1 | Output | Acknowledge |

**Transaction Timing:**

```
       ┌───┐   ┌───┐   ┌───┐
CLK    ┘   └───┘   └───┘   └───
       ┌───────────────────────
CYC ───┘                     └─
       ┌───────────────────────
STB ───┘                     └─
       ───────┬───────────────
ADR    ───────X──ADDR────X─────
       ───────┬───────────────
DAT_I  ───────X──DATA────X───── (write)
           ┌───────────┐
ACK ───────┘           └───────
               ┌───────────────
DAT_O  ────────X──DATA────X──── (read)
```

**Bus Splitting Algorithm:**

```verilog
for each peripheral i:
    if ((wbs_adr_i & ADDR_MASK) == BASE_ADDR_i)
        s_wb_stb[i] = wbs_stb_i & wbs_cyc_i
        s_wb_adr[i] = wbs_adr_i
        s_wb_dat_w[i] = wbs_dat_i
        wbs_ack_o = s_wb_ack[i]
        wbs_dat_o = s_wb_dat_r[i]
    else
        s_wb_stb[i] = 0
```

---

## Memory Organization

### Address Space Layout

```
0x0000_0000 ├─────────────────────────┐
            │  Caravel System Memory  │
            │  (Management SoC)       │
0x2FFF_FFFF ├─────────────────────────┤
0x3000_0000 ├─────────────────────────┤
            │  PWM0 Registers         │
0x3000_FFFF ├─────────────────────────┤
0x3001_0000 ├─────────────────────────┤
            │  PWM1 Registers         │
0x3001_FFFF ├─────────────────────────┤
0x3002_0000 ├─────────────────────────┤
            │  PWM2 Registers         │
0x3002_FFFF ├─────────────────────────┤
0x3003_0000 ├─────────────────────────┤
            │  PWM3 Registers         │
0x3003_FFFF ├─────────────────────────┤
0x3004_0000 ├─────────────────────────┤
            │  SRAM0 (4KB)            │
0x3004_0FFF ├─────────────────────────┤
            │  Unused (60KB)          │
0x3004_FFFF ├─────────────────────────┤
0x3005_0000 ├─────────────────────────┤
            │  SRAM1 (4KB)            │
0x3005_0FFF ├─────────────────────────┤
            │  Unused (60KB)          │
0x3005_FFFF ├─────────────────────────┤
0x3006_0000 ├─────────────────────────┤
            │  SRAM2 (4KB)            │
0x3006_0FFF ├─────────────────────────┤
            │  Unused (60KB)          │
0x3006_FFFF └─────────────────────────┘
```

### GPIO Mapping

| Pin | Signal | Direction | Description |
|-----|--------|-----------|-------------|
| io[0:4] | Reserved | - | Caravel system use |
| io[5:7] | Unused | - | Available for expansion |
| io[8] | pwm_out[0] | Output | PWM0 channel 0 |
| io[9] | pwm_out[1] | Output | PWM0 channel 1 |
| io[10] | pwm_out[2] | Output | PWM1 channel 0 |
| io[11] | pwm_out[3] | Output | PWM1 channel 1 |
| io[12] | pwm_out[4] | Output | PWM2 channel 0 |
| io[13] | pwm_out[5] | Output | PWM2 channel 1 |
| io[14] | pwm_out[6] | Output | PWM3 channel 0 |
| io[15] | pwm_out[7] | Output | PWM3 channel 1 |
| io[16:37] | Unused | - | Available for expansion |

---

## Interrupt Architecture

### Interrupt Sources

| Source | Signal | IRQ Line |
|--------|--------|----------|
| PWM0 | pwm_irq[0] | user_irq[0] |
| PWM1 | pwm_irq[1] | user_irq[0] |
| PWM2 | pwm_irq[2] | user_irq[1] |
| PWM3 | pwm_irq[3] | user_irq[1] |

### Aggregation Logic

```verilog
assign user_irq[0] = pwm_irq[0] | pwm_irq[1];
assign user_irq[1] = pwm_irq[2] | pwm_irq[3];
assign user_irq[2] = 1'b0;  // Unused
```

### Interrupt Handling Flow

1. **PWM Event Occurs:**
   - Counter overflow or compare match
   - Timer sets interrupt flag in IRQ register

2. **Signal Propagation:**
   - IRQ signal asserted at timer output
   - Aggregation logic combines to user_irq

3. **Caravel Processing:**
   - Management SoC interrupt controller detects
   - Firmware interrupt handler invoked

4. **Software Response:**
   - Read IRQ status registers to identify source
   - Service the interrupt
   - Write to IRQ register to clear flag

5. **Signal Deassertion:**
   - Timer clears IRQ output
   - user_irq deasserts when all sources clear

---

## Clock and Reset

### Clock Distribution

```
                    wb_clk_i (40 MHz max)
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
  [PWM Timers]    [Bus Splitter]      [SRAM Banks]
      │                  │                  │
  Counter logic    Address decode    Memory array
```

**Clock Characteristics:**
- **Source:** Caravel management SoC
- **Frequency:** Up to 40 MHz (25ns period)
- **Type:** Single-phase, synchronous
- **Distribution:** Balanced tree (handled by OpenLane)

### Reset Strategy

**Reset Type:** Synchronous, active-high

**Reset Sequence:**
1. Caravel asserts `wb_rst_i`
2. All peripherals reset simultaneously:
   - PWM timers: Counters → 0, outputs → 0
   - SRAM: No initialization (data unknown)
   - Bus splitter: Internal state → idle
3. Caravel deasserts reset
4. System begins operation on next clock edge

**Reset Requirements:**
- Minimum reset pulse: 2 clock cycles
- Setup time: 1ns before clock
- Hold time: 1ns after clock

---

## Power Architecture

### Power Domains

| Domain | Signal | Voltage | Purpose |
|--------|--------|---------|---------|
| Digital Core | `VPWR` | 1.8V | Logic power (Sky130) |
| Digital Ground | `VGND` | 0V | Logic ground |
| I/O Power | `VDD3V3` | 3.3V | GPIO buffers |
| I/O Ground | `VSS` | 0V | I/O ground |

### Power Distribution

```
Caravel Power Grid
    │
    ├── VPWR ──┬─→ user_project logic
    │          ├─→ PWM timers
    │          └─→ SRAM arrays
    │
    ├── VGND ──┬─→ Ground return paths
    │          
    ├── VDD3V3 ─→ GPIO pads
    │
    └── VSS ────→ I/O ground
```

### SRAM Power Connections

SRAM instances have explicit power pins:
```verilog
`ifdef USE_POWER_PINS
    .VPWR(VPWR),
    .VGND(VGND),
`endif
```

This ensures proper power routing during physical design.

### Power Considerations

**Dynamic Power:**
- Dominated by PWM counter switching
- Proportional to clock frequency
- Reducible by clock gating (not implemented)

**Static Power:**
- Minimal in digital logic
- SRAM leakage dependent on temperature
- I/O pad leakage negligible

**Power Optimization Opportunities:**
1. Clock gating for unused timers
2. PWM output disable when duty = 0 or 100%
3. SRAM power-down modes
4. Dynamic voltage/frequency scaling

---

## Design Considerations

### Scalability

**Current Limits:**
- 7 peripherals (bus splitter limitation)
- 8 PWM channels (4 timers × 2)
- 12KB SRAM (3 banks × 4KB)

**Expansion Options:**
- Add second-level bus splitters
- Use CF_TMR32 instances with more channels
- Integrate larger SRAM banks
- Implement DMA for memory transfers

### Performance

**Worst-Case Paths:**
1. Bus splitter address decode
2. SRAM access time
3. PWM compare logic

**Timing Margins:**
- Target: 25ns clock period (40 MHz)
- Typical slack: +2-5ns (with Sky130)
- Critical paths: Bus multiplexers

### Reliability

**Design for Test (DFT):**
- Scan chain insertion (handled by OpenLane)
- Logic analyzer probes for debug
- Full boundary scan capability

**Error Handling:**
- No bus timeout (relies on peripheral ACK)
- No address decode error checking
- Firmware must validate addresses

---

## References

- [Wishbone B4 Specification](https://opencores.org/howto/wishbone)
- [CF_TMR32 IP Documentation](/nc/ip/CF_TMR32/)
- [CF_SRAM_1024x32 IP Documentation](/nc/ip/CF_SRAM_1024x32/)
- [Caravel Documentation](https://github.com/chipfoundry/caravel)
- [OpenLane Physical Design](https://librelane.readthedocs.io/)

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-03
