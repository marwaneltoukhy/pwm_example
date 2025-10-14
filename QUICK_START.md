# PWM Project - Quick Start Guide

## 🚀 Run All Tests

```bash
cd /workspace/pwm_example/verilog/dv/cocotb

# Test 1: Simple PWM (50% duty cycle)
caravel_cocotb -t pwm_simple_test -tag test1

# Test 2: Four Channels (25%, 50%, 75%, 90%)
caravel_cocotb -t pwm_four_channel_test -tag test2

# Test 3: Duty Cycle Sweep (10%, 25%, 50%, 75%, 90%)
caravel_cocotb -t pwm_duty_sweep_test -tag test3

# Test 4: Boundary Cases (0%, 1%, 99%, 100%)
caravel_cocotb -t pwm_boundary_test -tag test4
```

## ✅ Check Results

```bash
# All tests should PASS
ls sim/test1/RTL-pwm_simple_test/passed        # Should exist
ls sim/test2/RTL-pwm_four_channel_test/passed  # Should exist
ls sim/test3/RTL-pwm_duty_sweep_test/passed    # Should exist
ls sim/test4/RTL-pwm_boundary_test/passed      # Should exist

# View test logs
cat sim/test1/RTL-pwm_simple_test/test.log
cat sim/test2/RTL-pwm_four_channel_test/test.log
cat sim/test3/RTL-pwm_duty_sweep_test/test.log
cat sim/test4/RTL-pwm_boundary_test/test.log
```

## 📊 View Waveforms

```bash
gtkwave sim/test1/RTL-pwm_simple_test/waves.vcd &
gtkwave sim/test2/RTL-pwm_four_channel_test/waves.vcd &
gtkwave sim/test3/RTL-pwm_duty_sweep_test/waves.vcd &
gtkwave sim/test4/RTL-pwm_boundary_test/waves.vcd &
```

## 📝 Key Signals to Monitor

In GTKWave, add these signals:
- `caravel_top.uut.mprj.pwm0.pwm0` - PWM0 output
- `caravel_top.uut.mprj.pwm1.pwm0` - PWM1 output
- `caravel_top.uut.mprj.pwm2.pwm0` - PWM2 output
- `caravel_top.uut.mprj.pwm3.pwm0` - PWM3 output
- `caravel_top.uut.chip_core.mprj_io[0]` - PWM0 on GPIO
- `caravel_top.uut.chip_core.mprj_io[1]` - PWM1 on GPIO
- `caravel_top.uut.chip_core.mprj_io[2]` - PWM2 on GPIO
- `caravel_top.uut.chip_core.mprj_io[3]` - PWM3 on GPIO

## 📚 Documentation

- **README.md** - Project overview
- **docs/test_summary.md** - Detailed test results
- **docs/register_map.md** - Register addresses
- **docs/FINAL_SUMMARY.md** - Complete project summary
- **QUICK_START.md** - This file

## ⚡ Expected Results

All 4 tests should **PASS** with:
- **pwm_simple_test**: 49.0% duty cycle (target 50%)
- **pwm_four_channel_test**: 
  - PWM0: 25.0%
  - PWM1: 49.0%
  - PWM2: 74.0%
  - PWM3: 89.0%
- **pwm_duty_sweep_test**:
  - 10% → 9.7%
  - 25% → 24.0%
  - 50% → 49.0%
  - 75% → 74.0%
  - 90% → 89.0%
- **pwm_boundary_test**:
  - 0% → 0.0%
  - 1% → 0.7%
  - 99% → 98.6%
  - 100% → 100.0%

**All measurements within ±2% tolerance** ✅

## 🎯 Test Pass Rate: 4/4 (100%)

Happy testing! 🎉
