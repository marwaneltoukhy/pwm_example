from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
import cocotb.triggers

@cocotb.test()
@report_test
async def pwm_duty_sweep_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=50_000_000)
    
    cocotb.log.info("[TEST] Start PWM duty cycle sweep test")
    
    await caravelEnv.release_csb()
    
    duty_cycles_to_test = [10, 25, 50, 75, 90]
    
    all_passed = True
    
    for target_duty in duty_cycles_to_test:
        cocotb.log.info(f"[TEST] Waiting for firmware to configure {target_duty}% duty cycle...")
        await caravelEnv.wait_mgmt_gpio(1)
        cocotb.log.info(f"[TEST] Configuration complete for {target_duty}%")
        
        await cocotb.triggers.ClockCycles(caravelEnv.clk, 2000)
        
        pwm_high_count = 0
        pwm_low_count = 0
        
        cocotb.log.info(f"[TEST] Sampling PWM0 for {target_duty}% duty cycle...")
        
        for i in range(5000):
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
                cocotb.log.info(f"[TEST]   Duty cycle {measured_duty:.1f}% is within {tolerance}% of {target_duty}% - PASS")
            else:
                cocotb.log.error(f"[TEST]   Duty cycle {measured_duty:.1f}% is NOT within {tolerance}% of {target_duty}% - FAIL")
                all_passed = False
        else:
            cocotb.log.error(f"[TEST]   No PWM samples collected - FAIL")
            all_passed = False
        
        cocotb.log.info(f"[TEST] Waiting for mgmt_gpio to go low...")
        await caravelEnv.wait_mgmt_gpio(0)
    
    cocotb.log.info("[TEST] Waiting for final handshake...")
    await caravelEnv.wait_mgmt_gpio(1)
    
    if all_passed:
        cocotb.log.info("[TEST] All duty cycle sweep tests passed - TEST PASSED")
    else:
        cocotb.log.error("[TEST] Some duty cycle sweep tests failed - TEST FAILED")
    
    cocotb.log.info("[TEST] PWM duty cycle sweep test completed")
