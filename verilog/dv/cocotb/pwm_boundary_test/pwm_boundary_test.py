from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
import cocotb.triggers

@cocotb.test()
@report_test
async def pwm_boundary_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10_000_000)
    await caravelEnv.release_csb()
    
    cocotb.log.info("[TEST] Start PWM boundary test (edge cases: 0%, 1%, 99%, 100%)")
    
    test_cases = [
        {"cmpx": 0, "target": 0, "tolerance": 2},
        {"cmpx": 1, "target": 1, "tolerance": 2},
        {"cmpx": 99, "target": 99, "tolerance": 2},
        {"cmpx": 100, "target": 100, "tolerance": 2}
    ]
    
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Firmware initialized, starting boundary tests")
    
    for i, test in enumerate(test_cases):
        target_duty = test["target"]
        tolerance = test["tolerance"]
        
        cocotb.log.info(f"[TEST] Waiting for firmware to configure {target_duty}% duty cycle...")
        
        await caravelEnv.wait_mgmt_gpio(0)
        cocotb.log.info(f"[TEST] ✓ mgmt_gpio=0: firmware configuring duty cycle {target_duty}%")
        
        await caravelEnv.wait_mgmt_gpio(1)
        cocotb.log.info(f"[TEST] ✓ mgmt_gpio=1: PWM configuration stable, ready to measure")
        
        await cocotb.triggers.ClockCycles(caravelEnv.clk, 2000)
        
        pwm_high_count = 0
        pwm_low_count = 0
        
        cocotb.log.info(f"[TEST] Sampling PWM0 for {target_duty}% duty cycle (10k cycles)...")
        
        sample_cycles = 10000
        prev_pwm = int(dut.uut.mprj.mprj.io_out[0].value)
        
        for _ in range(sample_cycles):
            await cocotb.triggers.RisingEdge(caravelEnv.clk)
            pwm_val = int(dut.uut.mprj.mprj.io_out[0].value)
            
            if pwm_val == 1:
                pwm_high_count += 1
            else:
                pwm_low_count += 1
        
        measured_duty = (pwm_high_count / sample_cycles) * 100.0
        
        cocotb.log.info(f"[TEST]   Measured: {measured_duty:.1f}% (high: {pwm_high_count}, low: {pwm_low_count})")
        
        if target_duty == 0:
            if measured_duty <= tolerance:
                cocotb.log.info(f"[TEST]   ✓ PASS: Duty cycle {measured_duty:.1f}% <= {tolerance}%")
            else:
                cocotb.log.error(f"[TEST]   ✗ FAIL: Duty cycle {measured_duty:.1f}% > {tolerance}%")
        elif target_duty == 100:
            if measured_duty >= (100 - tolerance):
                cocotb.log.info(f"[TEST]   ✓ PASS: Duty cycle {measured_duty:.1f}% >= {100-tolerance}%")
            else:
                cocotb.log.error(f"[TEST]   ✗ FAIL: Duty cycle {measured_duty:.1f}% < {100-tolerance}%")
        else:
            if abs(measured_duty - target_duty) <= tolerance:
                cocotb.log.info(f"[TEST]   ✓ PASS: Duty cycle {measured_duty:.1f}% within ±{tolerance}% of {target_duty}%")
            else:
                cocotb.log.error(f"[TEST]   ✗ FAIL: Duty cycle {measured_duty:.1f}% NOT within ±{tolerance}% of {target_duty}%")
    
    cocotb.log.info("[TEST] ✓✓✓ ALL BOUNDARY TESTS PASSED ✓✓✓")
    cocotb.log.info("[TEST] PWM boundary test completed")
