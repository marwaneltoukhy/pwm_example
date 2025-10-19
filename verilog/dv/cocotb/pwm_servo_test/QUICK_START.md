# Quick Start Guide - PWM Servo Test

## Prerequisites

Ensure you have the Caravel cocotb environment set up:

```bash
cd /workspace/pwm_example
python verilog/dv/setup-cocotb.py $(pwd)
```

## Running the Test

### Single Test Execution

From the `verilog/dv/cocotb` directory:

```bash
cd verilog/dv/cocotb
caravel_cocotb -t pwm_servo_test -tag pwm_test
```

### RTL Simulation (Default)
```bash
caravel_cocotb -t pwm_servo_test -tag pwm_rtl
```

### Gate-Level Simulation
```bash
caravel_cocotb -t pwm_servo_test -tag pwm_gl -sim GL
```

### Using Test List
Create a test list file `pwm_tests.yaml`:
```yaml
tests:
  - pwm_servo_test
```

Then run:
```bash
caravel_cocotb -tl pwm_tests.yaml -tag pwm_batch
```

## Test Results Location

After running, results are in:
```
sim/<tag>/RTL-pwm_servo_test/
├── firmware.log      # Firmware compilation log
├── test.log          # Test execution log
├── waves.vcd         # Waveform dump
├── passed            # Created if test passes
└── failed            # Created if test fails
```

## Viewing Waveforms

To view the waveforms with GTKWave:

```bash
gtkwave sim/<tag>/RTL-pwm_servo_test/waves.vcd &
```

### Key Signals to Monitor

Add these signals to your GTKWave view:
- `uut.mprj.io_out[3:0]` - PWM outputs
- `uut.chip_core.gpio` - Management GPIO (handshake)
- `uut.wb_clk_i` - Wishbone clock
- `uut.wb_rst_i` - Wishbone reset
- `uut.wbs_adr_i` - Wishbone address bus
- `uut.wbs_dat_i` - Wishbone data input
- `uut.wbs_we_i` - Wishbone write enable
- `uut.wbs_stb_i` - Wishbone strobe
- `uut.wbs_ack_o` - Wishbone acknowledge

### PWM Timer Internal Signals (if accessible)

For each timer instance (0-3):
- `uut.mprj.pwm_timer_X.tmr` - Current timer value
- `uut.mprj.pwm_timer_X.cmpx` - Compare X value (pulse width)
- `uut.mprj.pwm_timer_X.reload` - Reload value
- `uut.mprj.pwm_timer_X.pwm0` - PWM0 output

## Expected Test Output

### Successful Test
```
[TEST] Starting PWM Servo Test
[TEST] Firmware configuration complete
[TEST] Phase 1: Testing neutral position (18000 ticks ~1500us)
[TEST] PWM0 pulse width sample 1: 18000 cycles
[TEST] PWM0 pulse width sample 2: 18000 cycles
[TEST] PWM0 pulse width sample 3: 18000 cycles
[TEST] PWM0 average pulse width: 18000 cycles
[TEST] Expected range: 16000 - 20000 cycles
[TEST] PWM0 pulse width PASSED
...
[TEST] Test Summary: 16/16 checks passed
[TEST] PWM Servo Test PASSED
```

### Failed Test
```
[TEST] PWM0 average pulse width: 12000 cycles
[TEST] Expected range: 16000 - 20000 cycles
[TEST] PWM0 pulse width FAILED - out of range
...
[TEST] Test Summary: 12/16 checks passed
[TEST] PWM Servo Test FAILED
```

## Common Issues and Solutions

### Issue: Test times out
**Solution**: Increase timeout in the Python test:
```python
caravelEnv = await test_configure(dut, timeout_cycles=50000000)  # Increase from 30M
```

### Issue: No PWM pulses detected
**Possible causes**:
1. PWM outputs not routed to pins correctly
2. Timer not enabled
3. Clock not reaching user project

**Debug steps**:
1. Check `io_oeb[3:0]` is set to 0 (output enable)
2. Verify Wishbone transactions in waveform
3. Check timer enable bit in CTRL register

### Issue: Pulse width measurements off by constant factor
**Possible causes**:
1. Clock frequency mismatch
2. Prescaler value incorrect

**Debug steps**:
1. Verify clock frequency is 12 MHz
2. Check prescaler register value (should be 0)
3. Measure actual clock period in waveform

### Issue: Firmware doesn't complete
**Possible causes**:
1. Wishbone interface not enabled
2. Bus hanging (no ACK)
3. Incorrect base addresses

**Debug steps**:
1. Check `User_enableIF()` is called
2. Monitor `wbs_ack_o` signal
3. Verify address decoding logic

### Issue: Management GPIO not toggling
**Possible causes**:
1. GPIO not configured as output
2. Wrong GPIO signal monitored

**Debug steps**:
1. Check `ManagmentGpio_outputEnable()` is called
2. Verify signal path: `dut.uut.chip_core.gpio`
3. Check GPIO configuration registers

## Test Customization

### Adjust Verification Tolerances

In `pwm_servo_test.py`, modify the ranges:

```python
# For tighter tolerance
result1 = await verify_pwm_range(pwm0_pin, "PWM0", 17500, 18500)  # ±500

# For looser tolerance
result1 = await verify_pwm_range(pwm0_pin, "PWM0", 15000, 21000)  # ±3000
```

### Change Number of Samples

```python
result1 = await verify_pwm_range(pwm0_pin, "PWM0", 16000, 20000, num_samples=5)
```

### Modify Test Sequence

In `pwm_servo_test.c`, add more positions:

```c
ManagmentGpio_write(0);
config_pwm_ticks(12000, 12000, 12000, 12000);  // -60 degrees
delay_cyc(_DELAY_VALUE);
```

Then add corresponding verification in Python:

```python
result17 = await verify_pwm_range(pwm0_pin, "PWM0", 10000, 14000)
```

## Performance Considerations

### Simulation Time
- RTL simulation: ~5-10 minutes
- Gate-level simulation: ~30-60 minutes (depends on design size)

### Memory Usage
- RTL: ~500 MB
- Gate-level: ~2-4 GB

### Waveform Size
- With all signals: ~200-500 MB
- To reduce: limit waveform dump scope or duration

## Debugging Tips

1. **Enable verbose logging**:
   ```python
   cocotb.log.setLevel(logging.DEBUG)
   ```

2. **Add debug prints in firmware**:
   ```c
   print("Configuring PWM0\n");
   ```

3. **Check register values after write**:
   ```c
   uint32_t readback = USER_readWord(CSR_PWM0_BASE + 0x0cL);
   ```

4. **Monitor specific cycles**:
   ```python
   await ClockCycles(caravelEnv.clk, 1)
   cocotb.log.info(f"PWM0 value: {pwm0_pin.value}")
   ```

5. **Add breakpoints in simulation**:
   Use `$stop` in Verilog or breakpoints in the simulator GUI

## Next Steps

After successful test:
1. Review waveforms to understand timing
2. Run gate-level simulation
3. Integrate with CI/CD pipeline
4. Add more test cases for edge conditions
5. Test with different clock frequencies
6. Verify interrupt functionality
7. Test fault input behavior

## Support and Resources

- **CF_TMR32 Documentation**: `/nc/ip/CF_TMR32/v2.1.0-nc/CF_TMR32.pdf`
- **Caravel Documentation**: Caravel README and documentation
- **cocotb Documentation**: https://docs.cocotb.org/
- **Test Documentation**: `README.md` and `CODE_MAPPING.md` in this directory
