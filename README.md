# Multi-Channel PWM Controller for Caravel

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/chipfoundry/caravel_user_project/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/chipfoundry/caravel_user_project/actions/workflows/user_project_ci.yml)

**A production-ready 8-channel PWM controller with integrated SRAM for the Caravel ASIC platform.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Memory Map](#memory-map)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Physical Implementation](#physical-implementation)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a **multi-channel PWM (Pulse Width Modulation) controller** designed for integration with the [Caravel](https://github.com/chipfoundry/caravel) open-source ASIC platform. It provides 8 independent PWM output channels ideal for motor control, LED dimming, servo control, and other pulse-width modulation applications.

### Key Specifications

| Specification | Value |
|--------------|-------|
| **PWM Channels** | 8 (4 timers × 2 channels each) |
| **Resolution** | 32-bit timer with 16-bit prescaler |
| **Memory** | 12KB SRAM (3 banks × 4KB) |
| **Bus Interface** | Wishbone B4 Classic |
| **Clock Frequency** | Up to 40 MHz (25ns period) |
| **Technology** | Sky130, GF180MCU support |
| **License** | Apache 2.0 |

---

## ✨ Features

### PWM Capabilities
- ✅ **8 Independent PWM Channels:** Four CF_TMR32 timer modules, each providing dual PWM outputs
- ✅ **Configurable Frequency:** 32-bit period register with 16-bit prescaler
- ✅ **Adjustable Duty Cycle:** 32-bit compare register per channel
- ✅ **Interrupt Support:** Per-timer interrupt generation
- ✅ **Edge-Aligned Mode:** Standard PWM waveform generation

### Memory & Bus
- ✅ **3 SRAM Banks:** 1024×32-bit memory (4KB each)
- ✅ **Wishbone Interface:** Standard B4 Classic protocol
- ✅ **Memory-Mapped I/O:** Simple register-based control
- ✅ **Byte-Select Support:** 32-bit word with byte granularity

### Integration
- ✅ **Caravel Compatible:** Meets all user project wrapper requirements
- ✅ **Verified Design:** Comprehensive cocotb testbench suite
- ✅ **DRC/LVS Clean:** Fully hardened with OpenLane
- ✅ **Production Ready:** Gate-level simulation passing

---

## 🏗️ Architecture

### System Block Diagram

```
                    Caravel Management SoC
                            │
                    [Wishbone Master]
                            │
                   ┌────────┴────────┐
                   │  user_project   │
                   │  (Top Module)   │
                   └────────┬────────┘
                            │
              ┌─────────────┴─────────────┐
              │  Wishbone Bus Splitter    │
              │     (1-to-7 Decoder)      │
              └─┬──┬──┬──┬──┬──┬──┬──────┘
                │  │  │  │  │  │  │
        ┌───────┴──┴──┴──┴──┘  │  │
        │  4× CF_TMR32_WB       │  │
        │  ┌─────────────────┐  │  │
        │  │ PWM0 → io[8:9]  │  │  │
        │  │ PWM1 → io[10:11]│  │  │
        │  │ PWM2 → io[12:13]│  │  │
        │  │ PWM3 → io[14:15]│  │  │
        │  └─────────────────┘  │  │
        │                       │  │
        └───────────────────────┘  │
                                   │
                   ┌───────────────┴──────────┐
                   │ 3× CF_SRAM_1024x32       │
                   │ (12KB total memory)      │
                   └──────────────────────────┘
```

### Component Details

#### CF_TMR32_WB Timer/PWM Module
Each of the 4 timer instances provides:
- 32-bit up-counter with programmable period
- 16-bit clock prescaler (divide by 1 to 65535)
- Dual 32-bit compare registers → 2 PWM outputs
- Interrupt on overflow/match
- Wishbone slave interface

#### CF_SRAM_1024x32 Memory Module  
Each of the 3 SRAM instances provides:
- 1024 words × 32 bits (4KB)
- Single-cycle read/write access
- Wishbone slave interface
- Byte-select support (4 × 8-bit lanes)

#### Wishbone Bus Splitter
- Decodes upper 16 address bits
- Routes transactions to 7 peripherals
- Base addresses: 0x3000_0000 through 0x3006_0000
- Each peripheral has 64KB address space

---

## 🚀 Getting Started

### Prerequisites

- **Docker** ([Install Docker](https://docs.docker.com/get-docker/))
- **Python 3.8+** with pip
- **Git**
- **8GB+ RAM** recommended
- **30GB+ disk space** for tools and dependencies

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/marwaneltoukhy/pwm_example.git
   cd pwm_example
   ```

2. **Set up the environment:**
   ```bash
   make setup
   ```
   This installs:
   - Caravel Lite SoC
   - OpenLane for ASIC hardening
   - PDK (Sky130 or GF180MCU)
   - Management core for simulation
   - Timing analysis scripts

3. **Install cocotb simulation environment:**
   ```bash
   make setup-cocotb
   ```

### Quick Test

Run a simple PWM test to verify the installation:

```bash
make cocotb-verify-pwm_test-rtl
```

You should see output indicating all 6 PWM outputs are toggling.

---

## 🗺️ Memory Map

### Base Addresses

| Address | Module | Description |
|---------|--------|-------------|
| `0x3000_0000` | PWM0 | Timer/PWM controller 0 (outputs pwm0, pwm1) |
| `0x3001_0000` | PWM1 | Timer/PWM controller 1 (outputs pwm2, pwm3) |
| `0x3002_0000` | PWM2 | Timer/PWM controller 2 (outputs pwm4, pwm5) |
| `0x3003_0000` | PWM3 | Timer/PWM controller 3 (outputs pwm6, pwm7) |
| `0x3004_0000` | SRAM0 | 1024×32 SRAM bank 0 |
| `0x3005_0000` | SRAM1 | 1024×32 SRAM bank 1 |
| `0x3006_0000` | SRAM2 | 1024×32 SRAM bank 2 |

### CF_TMR32 Register Map (per timer)

| Offset | Register | Access | Description |
|--------|----------|--------|-------------|
| `0x00` | CTRL | R/W | Control register (enable, mode) |
| `0x04` | PRE | R/W | Prescaler value (16-bit) |
| `0x08` | PERIOD | R/W | Timer period (32-bit) |
| `0x0C` | CMP0 | R/W | Compare value for PWM0 |
| `0x10` | CMP1 | R/W | Compare value for PWM1 |
| `0x14` | COUNT | R | Current counter value |
| `0x18` | IRQ | R/W | Interrupt status/clear |

*Note: Refer to [CF_TMR32 documentation](/nc/ip/CF_TMR32/) for complete register details.*

### SRAM Access

SRAM is accessed as 32-bit words at byte-aligned addresses:
```
Word Address = Base + (index × 4)
Valid range: index = 0 to 1023
```

---

## 💡 Usage Examples

### Example 1: Configure PWM for LED Dimming

```c
#define PWM0_BASE 0x30000000
#define REG_CTRL    0x00
#define REG_PRE     0x04
#define REG_PERIOD  0x08
#define REG_CMP0    0x0C

// Configure PWM0 for ~1kHz @ 40MHz clock
*(volatile uint32_t*)(PWM0_BASE + REG_PRE) = 39;      // Prescaler = 40
*(volatile uint32_t*)(PWM0_BASE + REG_PERIOD) = 999;  // Period = 1000 counts
*(volatile uint32_t*)(PWM0_BASE + REG_CMP0) = 500;    // 50% duty cycle
*(volatile uint32_t*)(PWM0_BASE + REG_CTRL) = 0x01;   // Enable timer

// Adjust brightness (0-100%)
void set_brightness(uint8_t percent) {
    uint32_t compare = (percent * 999) / 100;
    *(volatile uint32_t*)(PWM0_BASE + REG_CMP0) = compare;
}
```

### Example 2: Motor Control with Multiple PWM Channels

```c
#define PWM1_BASE 0x30010000
#define PWM2_BASE 0x30020000

// Configure two motors with complementary PWM
void init_motor_control(void) {
    // Motor 1 (PWM1, channel 0-1)
    *(volatile uint32_t*)(PWM1_BASE + REG_PRE) = 0;
    *(volatile uint32_t*)(PWM1_BASE + REG_PERIOD) = 1999;
    *(volatile uint32_t*)(PWM1_BASE + REG_CMP0) = 1000;  // Forward
    *(volatile uint32_t*)(PWM1_BASE + REG_CMP1) = 0;     // Reverse off
    *(volatile uint32_t*)(PWM1_BASE + REG_CTRL) = 0x01;
    
    // Motor 2 (PWM2, channel 0-1)
    *(volatile uint32_t*)(PWM2_BASE + REG_PRE) = 0;
    *(volatile uint32_t*)(PWM2_BASE + REG_PERIOD) = 1999;
    *(volatile uint32_t*)(PWM2_BASE + REG_CMP0) = 800;
    *(volatile uint32_t*)(PWM2_BASE + REG_CMP1) = 0;
    *(volatile uint32_t*)(PWM2_BASE + REG_CTRL) = 0x01;
}
```

### Example 3: Use SRAM for Waveform Storage

```c
#define SRAM0_BASE 0x30040000

// Store 256-point sine wave lookup table
void init_sine_table(void) {
    for (int i = 0; i < 256; i++) {
        float angle = (i * 2 * 3.14159) / 256;
        uint32_t value = (uint32_t)((sin(angle) + 1.0) * 500);
        *(volatile uint32_t*)(SRAM0_BASE + i*4) = value;
    }
}

// Play sine wave on PWM
void play_sine_wave(void) {
    for (int i = 0; i < 256; i++) {
        uint32_t duty = *(volatile uint32_t*)(SRAM0_BASE + i*4);
        *(volatile uint32_t*)(PWM0_BASE + REG_CMP0) = duty;
        delay_us(100);  // 10kHz sample rate
    }
}
```

---

## 🧪 Testing

### Run All Tests

**RTL Simulation (fast, pre-synthesis):**
```bash
make cocotb-verify-all-rtl
```

**Gate-Level Simulation (slow, post-synthesis):**
```bash
make cocotb-verify-all-gl
```

### Run Individual Tests

```bash
# Test individual PWM channels
make cocotb-verify-pwm0_test-rtl
make cocotb-verify-pwm1_test-rtl
make cocotb-verify-pwm2_test-rtl
make cocotb-verify-pwm3_test-rtl

# Test all PWM channels together
make cocotb-verify-pwm_test-rtl

# Test SRAM functionality
make cocotb-verify-sram_test-rtl

# Test basic firmware execution
make cocotb-verify-hello_world-rtl
```

### Test Results

All tests should report:
```
**Test          : pwm_test
**PASS          : True
```

View waveforms using GTKWave:
```bash
gtkwave verilog/dv/cocotb/sim_build/pwm_test/pwm_test.vcd
```

---

## 🔨 Physical Implementation

### Harden the Design

**Step 1: Harden the user project macro**
```bash
make user_proj_example
```

This runs OpenLane to:
- Synthesize RTL to gate-level netlist
- Floorplan and place cells
- Route interconnects
- Generate GDS/LEF files

**Step 2: Harden the wrapper**
```bash
make user_project_wrapper
```

This integrates `user_proj_example` into the Caravel wrapper.

### Verify Timing

```bash
make extract-parasitics
make create-spef-mapping
make caravel-sta
```

Review timing report in `signoff/caravel/openlane-signoff/timing/`.

### Run Precheck

Before submitting to shuttle:
```bash
make precheck
make run-precheck
```

This verifies:
- ✅ DRC (Design Rule Check)
- ✅ LVS (Layout vs. Schematic)
- ✅ XOR check against golden wrapper
- ✅ Pin placement
- ✅ Power grid

---

## 📚 Documentation

### Quick Links

- **[Project Dashboard](PROJECT_DASHBOARD.md)** - Comprehensive status overview
- **[Caravel Integration Guide](docs/source/index.md)** - Detailed integration steps
- **[Test Documentation](verilog/dv/cocotb/user_proj_tests/README.md)** - Testbench descriptions
- **[OpenLane Configuration](openlane/user_proj_example/config.json)** - Synthesis settings

### IP Core Documentation

This project uses pre-verified IP cores:
- **CF_TMR32 v2.1.0** - [Documentation](/nc/ip/CF_TMR32/)
- **CF_SRAM_1024x32 v1.2.1** - [Documentation](/nc/ip/CF_SRAM_1024x32/)

### External Resources

- [Caravel Repository](https://github.com/chipfoundry/caravel)
- [OpenLane Documentation](https://librelane.readthedocs.io/)
- [Wishbone B4 Specification](https://opencores.org/howto/wishbone)
- [Sky130 PDK](https://skywater-pdk.readthedocs.io/)

---

## 🛠️ Project Structure

```
pwm_example/
├── verilog/
│   ├── dv/                      # Design verification
│   │   └── cocotb/              # Cocotb testbenches
│   │       └── user_proj_tests/ # Custom test cases
│   ├── rtl/                     # RTL source files
│   │   ├── user_project.v       # Top-level module
│   │   └── user_project_wrapper.v
│   └── gl/                      # Gate-level netlists
├── openlane/
│   ├── user_proj_example/       # OpenLane config
│   └── user_project_wrapper/
├── ip/
│   └── dependencies.json        # IP version manifest
├── docs/                        # Documentation
├── gds/                         # GDSII layout files
├── lef/                         # LEF abstracts
├── sdc/                         # Timing constraints
└── signoff/                     # Verification reports
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Run tests:** Ensure all tests pass
4. **Commit changes:** `git commit -m 'Add amazing feature'`
5. **Push to branch:** `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Workflow

1. Make changes to RTL in `verilog/rtl/`
2. Update testbenches in `verilog/dv/cocotb/`
3. Run RTL simulation: `make cocotb-verify-<test>-rtl`
4. Harden design: `make user_proj_example`
5. Run gate-level simulation: `make cocotb-verify-<test>-gl`
6. Submit PR with test results

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

### Third-Party IP Licenses

- **CF_TMR32:** Apache 2.0
- **CF_SRAM_1024x32:** Apache 2.0
- **Caravel:** Apache 2.0

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/marwaneltoukhy/pwm_example/issues)
- **Discussions:** [GitHub Discussions](https://github.com/marwaneltoukhy/pwm_example/discussions)
- **Email:** marwaneltoukhy@example.com

---

## 🎓 Citation

If you use this project in your research or publication, please cite:

```bibtex
@misc{pwm_caravel_2025,
  title={Multi-Channel PWM Controller for Caravel ASIC Platform},
  author={Marwan El Toukhy},
  year={2025},
  publisher={GitHub},
  url={https://github.com/marwaneltoukhy/pwm_example}
}
```

---

## 🙏 Acknowledgments

- **Efabless/ChipFoundry** - Caravel platform and MPW shuttle program
- **OpenLane Team** - Open-source ASIC flow
- **Google/SkyWater** - Sky130 open PDK
- **IP Providers** - CF_TMR32 and CF_SRAM_1024x32 cores

---

**Project Status:** ✅ Production Ready  
**Last Updated:** 2025-11-03  
**Version:** 1.0
