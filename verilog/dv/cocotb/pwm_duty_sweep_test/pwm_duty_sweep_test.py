from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
import cocotb.triggers

@cocotb.test()
@report_test
async def pwm_duty_sweep_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=50_000_000)
    
    cocotb.log.info("[TEST] Start PWM duty cycle sweep test")
    
    await caravelEnv.release_csb()
    
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Firmware ready, starting duty cycle sweep")
    
    duty_cycles_to_test = [10, 25, 50, 75, 90]
    
    all_passed = True
    
    for idx, target_duty in enumerate(duty_cycles_to_test):
        cocotb.log.info(f"[TEST] Waiting for firmware to configure {target_duty}% duty cycle...")
        
        await caravelEnv.wait_mgmt_gpio(0)
        cocotb.log.info(f"[TEST] ✓ mgmt_gpio=0: firmware configuring duty cycle {target_duty}%")
        
        await caravelEnv.wait_mgmt_gpio(1)
        cocotb.log.info(f"[TEST] ✓ mgmt_gpio=1: PWM configuration stable, ready to measure")
        
        await cocotb.triggers.ClockCycles(caravelEnv.clk, 1000)
        
        pwm_high_count = 0
        pwm_low_count = 0
        
        cocotb.log.info(f"[TEST] Sampling PWM0 for {target_duty}% duty cycle (10k cycles)...")
        
        for i in range(10000):
            await cocotb.triggers.ClockCycles(caravelEnv.clk, 1)
            gpio_val = caravelEnv.monitor_gpio(0, 0).integer
            
            if gpio_val == 1:
                pwm_high_count += 1
            else:
                pwm_low_count += 1
        
        if pwm_high_count + pwm_low_count > 0:
            measured_duty = (pwm_high_count / (pwm_high_count + pwm_low_count)) * 100
            cocotb.log.info(f"[TEST]   Measured: {measured_duty:.1f}% (high: {pwm_high_count}, low: {pwm_low_count})")
            
            tolerance = 2.0
            if abs(measured_duty - target_duty) <= tolerance:
                cocotb.log.info(f"[TEST]   ✓ PASS: Duty cycle {measured_duty:.1f}% within ±{tolerance}% of {target_duty}%")
            else:
                cocotb.log.error(f"[TEST]   ✗ FAIL: Duty cycle {measured_duty:.1f}% NOT within ±{tolerance}% of {target_duty}%")
                all_passed = False
        else:
            cocotb.log.error(f"[TEST]   ✗ FAIL: No PWM samples collected")
            all_passed = False
    
    if all_passed:
        cocotb.log.info("[TEST] ✓✓✓ ALL DUTY CYCLE TESTS PASSED ✓✓✓")
    else:
        cocotb.log.error("[TEST] ✗✗✗ SOME DUTY CYCLE TESTS FAILED ✗✗✗")
        assert False, "Duty cycle sweep test failed"
    
    cocotb.log.info("[TEST] PWM duty cycle sweep test completed")
