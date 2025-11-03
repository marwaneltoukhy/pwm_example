# Quick Start Guide

Get up and running with the PWM Example project in under 30 minutes!

---

## 🎯 What You'll Accomplish

By the end of this guide, you will have:
1. ✅ Set up the complete development environment
2. ✅ Run your first PWM simulation
3. ✅ Modified PWM parameters
4. ✅ Viewed waveforms in GTKWave
5. ✅ Understanding of how to extend the design

**Estimated Time:** 20-30 minutes (excluding initial setup downloads)

---

## 📋 Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Linux (Ubuntu 20.04+) | Ubuntu 22.04 |
| **RAM** | 8GB | 16GB+ |
| **Disk Space** | 20GB free | 50GB+ free |
| **CPU** | 2 cores | 4+ cores |

### Software Requirements

- **Docker** - For running OpenLane and tools
- **Python 3.8+** - For cocotb testbenches
- **Git** - For version control
- **Make** - For build automation

### Installation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y docker.io python3 python3-pip git make
sudo usermod -aG docker $USER  # Add user to docker group
newgrp docker  # Activate group without logout
```

**Verify installations:**
```bash
docker --version    # Should show version 20.10+
python3 --version   # Should show 3.8+
git --version       # Should show 2.25+
make --version      # Should show 4.2+
```

---

## 🚀 Step 1: Clone and Setup (5 minutes)

### Clone the Repository

```bash
cd ~
git clone https://github.com/marwaneltoukhy/pwm_example.git
cd pwm_example
```

### Run Initial Setup

This downloads Caravel, OpenLane, PDK, and other dependencies (~15GB):

```bash
make setup
```

**Expected Output:**
```
Cloning Caravel...
Installing OpenLane...
Downloading Sky130 PDK...
Setup complete!
```

**⏰ This step takes 10-20 minutes on first run.** Grab a coffee! ☕

### Setup Cocotb Simulation

```bash
make setup-cocotb
```

**Expected Output:**
```
Installing cocotb...
Setting up Caravel simulation infrastructure...
Cocotb setup complete!
```

---

## 🎮 Step 2: Run Your First Test (2 minutes)

### Test the PWM Functionality

```bash
make cocotb-verify-pwm_test-rtl
```

**What's Happening:**
1. Compiling Verilog RTL
2. Building firmware
3. Running cocotb testbench
4. Simulating chip behavior
5. Checking PWM outputs

**Expected Output:**
```
========================================
Running test: pwm_test
========================================
[INFO] Firmware ready, starting test
[INFO] Checking 6 PWMs (io[13:8])
[INFO] All 6 PWMs toggling after 12543 cycles
[TEST] SUCCESS: All 6 PWM outputs functional

**Test          : pwm_test
**PASS          : True
**SIM TIME      : 125000 ns
========================================
```

**✅ Success!** You've verified the PWM controller works!

---

## 🔍 Step 3: View Waveforms (2 minutes)

### Open GTKWave

```bash
gtkwave verilog/dv/cocotb/sim_build/pwm_test/pwm_test.vcd &
```

### Add Signals to View

1. **In the Signals pane (left)**, expand the hierarchy:
   - `pwm_test` → `uut` → `mprj`

2. **Drag these signals to the waveform viewer:**
   ```
   wb_clk_i          (Clock)
   wb_rst_i          (Reset)
   wbs_stb_i         (Wishbone strobe)
   wbs_ack_o         (Wishbone acknowledge)
   io_out[15:0]      (GPIO outputs)
   ```

3. **Zoom to fit:** Click the "Zoom Fit" button or press `Ctrl+Alt+F`

4. **Find PWM signals:** Look for toggling on `io_out[13:8]`

### What to Look For

**Good PWM Waveform:**
```
io_out[8]   ▁▁▁▁▁▁▁▁██████████▁▁▁▁▁▁▁▁██████████
io_out[9]   ▁▁▁▁▁▁▁▁▁▁▁▁██████▁▁▁▁▁▁▁▁▁▁▁▁██████
```

The signals should have regular, repeating patterns with different duty cycles.

---

## ✏️ Step 4: Modify PWM Configuration (5 minutes)

Let's change the PWM frequency and duty cycle!

### Edit the Firmware

```bash
nano verilog/dv/cocotb/user_proj_tests/pwm_test/pwm_test.c
```

**Find this section (around line 50):**
```c
// Configure PWM0
reg_write(PWM0_BASE + REG_PERIOD, 1000);
reg_write(PWM0_BASE + REG_CMP0, 500);    // 50% duty cycle
reg_write(PWM0_BASE + REG_CMP1, 250);    // 25% duty cycle
```

**Change to:**
```c
// Configure PWM0 - Faster frequency, different duty cycles
reg_write(PWM0_BASE + REG_PERIOD, 500);   // 2x faster
reg_write(PWM0_BASE + REG_CMP0, 400);     // 80% duty cycle
reg_write(PWM0_BASE + REG_CMP1, 100);     // 20% duty cycle
```

**Save and exit:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Re-run the Test

```bash
make cocotb-verify-pwm_test-rtl
```

### View Updated Waveforms

```bash
gtkwave verilog/dv/cocotb/sim_build/pwm_test/pwm_test.vcd &
```

**You should now see:**
- PWM toggling twice as fast
- Different duty cycles (80% and 20%)

---

## 🧪 Step 5: Run All Tests (5 minutes)

### Test Individual PWM Timers

```bash
make cocotb-verify-pwm0_test-rtl  # Test PWM0
make cocotb-verify-pwm1_test-rtl  # Test PWM1
make cocotb-verify-pwm2_test-rtl  # Test PWM2
make cocotb-verify-pwm3_test-rtl  # Test PWM3
```

### Test SRAM

```bash
make cocotb-verify-sram_test-rtl
```

**Expected Output:**
```
[INFO] Testing SRAM0 at 0x30040000
[INFO] Write pattern: sequential
[INFO] Read and verify...
[INFO] SRAM0 test PASSED
[INFO] Testing SRAM1...
[INFO] All SRAM banks functional
**PASS : True
```

### Run Complete Test Suite

```bash
make cocotb-verify-all-rtl
```

This runs all tests sequentially. **Estimated time:** 2-3 minutes.

---

## 🔨 Step 6: Understanding the Design (5 minutes)

### Memory Map Reference

| Address | What's There | How to Use |
|---------|-------------|------------|
| `0x3000_0000` | PWM0 registers | Configure timer 0 (outputs pwm0, pwm1) |
| `0x3001_0000` | PWM1 registers | Configure timer 1 (outputs pwm2, pwm3) |
| `0x3002_0000` | PWM2 registers | Configure timer 2 (outputs pwm4, pwm5) |
| `0x3003_0000` | PWM3 registers | Configure timer 3 (outputs pwm6, pwm7) |
| `0x3004_0000` | SRAM0 | 4KB memory bank 0 |
| `0x3005_0000` | SRAM1 | 4KB memory bank 1 |
| `0x3006_0000` | SRAM2 | 4KB memory bank 2 |

### Register Offsets (per PWM timer)

| Offset | Register | Description |
|--------|----------|-------------|
| `0x00` | CTRL | Control: bit 0 = enable |
| `0x04` | PRE | Prescaler (divide clock) |
| `0x08` | PERIOD | Timer period |
| `0x0C` | CMP0 | Compare 0 (sets PWM channel 0 duty cycle) |
| `0x10` | CMP1 | Compare 1 (sets PWM channel 1 duty cycle) |

### Calculate PWM Frequency

```
PWM_frequency = Clock_frequency / ((Prescaler + 1) × (Period + 1))

Example:
  Clock = 40 MHz
  Prescaler = 0
  Period = 999
  
  Frequency = 40,000,000 / ((0 + 1) × (999 + 1))
            = 40,000,000 / 1000
            = 40,000 Hz (40 kHz)
```

### Calculate Duty Cycle

```
Duty_cycle = (Compare_value / Period) × 100%

Example:
  Period = 999
  Compare = 500
  
  Duty = (500 / 999) × 100% ≈ 50%
```

---

## 📦 Next Steps

### Option 1: Run Physical Design (Advanced)

**Synthesize the design to gates:**
```bash
make user_proj_example
```

This runs OpenLane to convert RTL → GDS. **Takes 30-60 minutes.**

**Then run gate-level simulation:**
```bash
make cocotb-verify-pwm_test-gl
```

### Option 2: Add a New PWM Channel

Currently using 4 timers (8 channels). Add a 5th timer:

1. Edit `verilog/rtl/user_project.v`
2. Instantiate 5th CF_TMR32_WB module
3. Update bus splitter to 8 peripherals
4. Add firmware test
5. Run simulation

### Option 3: Create Custom Firmware

**Create a new test:**
```bash
mkdir verilog/dv/cocotb/user_proj_tests/my_custom_test
cd verilog/dv/cocotb/user_proj_tests/my_custom_test
```

**Copy template:**
```bash
cp ../pwm0_test/pwm0_test.c my_custom_test.c
cp ../pwm0_test/pwm0_test.py my_custom_test.py
```

**Edit firmware to do something interesting:**
- Sweep duty cycle (LED fading)
- Generate complementary PWM (motor control)
- Store patterns in SRAM and play back

### Option 4: Explore the IPs

**Read the IP documentation:**
```bash
ls /nc/ip/CF_TMR32/     # PWM timer docs
ls /nc/ip/CF_SRAM_1024x32/  # SRAM docs
```

Each IP has:
- RTL source code
- Register documentation
- Example usage
- Testbenches

---

## 🐛 Troubleshooting

### Test Fails with "Timeout"

**Cause:** Firmware not running or PWM not enabled

**Solution:**
```bash
# Check firmware compiled
ls -lh verilog/dv/cocotb/user_proj_tests/*/firmware.hex

# View waveforms to see where it stopped
gtkwave verilog/dv/cocotb/sim_build/*/pwm_test.vcd

# Look for wb_rst_i stuck high (should go low)
```

### "Command not found" Errors

**Cause:** Tools not in PATH

**Solution:**
```bash
# Ensure setup completed
make setup-cocotb

# Check paths
which iverilog  # Should show path
which cocotb-config  # Should show path
```

### Waveforms Show Only 'X' or 'Z'

**Cause:** Module not instantiated or signals unconnected

**Solution:**
- Check hierarchy in RTL
- Verify module instantiation
- Look for typos in signal names

### "Permission denied" Running Docker

**Cause:** User not in docker group

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
# Or logout and login again
```

### Simulation is Very Slow

**Cause:** Gate-level simulation or large VCD file

**Solution:**
- Use RTL simulation (faster) for development
- Reduce simulation time in test
- Disable VCD dumping if not needed

---

## 📚 Learn More

### Documentation
- **[README.md](../README.md)** - Full project documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design details
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive test guide
- **[PROJECT_DASHBOARD.md](../PROJECT_DASHBOARD.md)** - Project status

### External Resources
- **[Caravel Documentation](https://caravel-sim-infrastructure.readthedocs.io/)** - Chip infrastructure
- **[Cocotb Documentation](https://docs.cocotb.org/)** - Testbench framework
- **[Wishbone Spec](https://opencores.org/howto/wishbone)** - Bus protocol
- **[OpenLane Docs](https://librelane.readthedocs.io/)** - Physical design flow

---

## 🎉 Congratulations!

You've successfully:
- ✅ Set up the PWM Example project
- ✅ Run simulations
- ✅ Modified firmware
- ✅ Viewed waveforms
- ✅ Understand the basic architecture

**You're now ready to:**
- Create custom PWM patterns
- Integrate with other Caravel projects
- Extend the design with new features
- Contribute back to the project

---

## 💬 Get Help

- **GitHub Issues:** https://github.com/marwaneltoukhy/pwm_example/issues
- **Discussions:** https://github.com/marwaneltoukhy/pwm_example/discussions
- **Email:** marwaneltoukhy@example.com

---

**Happy Hacking! 🚀**

**Document Version:** 1.0  
**Last Updated:** 2025-11-03
