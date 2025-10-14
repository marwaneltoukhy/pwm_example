from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb

@cocotb.test()
@report_test
async def pwm_four_channel_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10_000_000)
    
    cocotb.log.info("[TEST] Start 4-channel PWM test")
    
    await caravelEnv.release_csb()
    
    cocotb.log.info("[TEST] Waiting for firmware configuration...")
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Configuration complete")
    
    await caravelEnv.wait_cycles(5000)
    
    cocotb.log.info("[TEST] Sampling all 4 PWM outputs for 5000 cycles...")
    
    pwm_high_counts = [0, 0, 0, 0]
    pwm_low_counts = [0, 0, 0, 0]
    pwm_last_values = [None, None, None, None]
    pwm_transitions = [0, 0, 0, 0]
    
    for _ in range(5000):
        for i in range(4):
            gpio_val = caravelEnv.monitor_gpio(i, i).integer
            
            if gpio_val == 1:
                pwm_high_counts[i] += 1
            else:
                pwm_low_counts[i] += 1
            
            if pwm_last_values[i] is not None and pwm_last_values[i] != gpio_val:
                pwm_transitions[i] += 1
            
            pwm_last_values[i] = gpio_val
        
        await caravelEnv.wait_cycles(1)
    
    cocotb.log.info("[TEST] Sampling complete")
    
    expected_duty_cycles = [25, 50, 75, 90]
    tolerance = 2.0
    all_pass = True
    
    for i in range(4):
        total_samples = pwm_high_counts[i] + pwm_low_counts[i]
        duty_cycle = (pwm_high_counts[i] / total_samples * 100) if total_samples > 0 else 0
        
        cocotb.log.info(f"[TEST] PWM{i} Results:")
        cocotb.log.info(f"[TEST]   High count: {pwm_high_counts[i]}, Low count: {pwm_low_counts[i]}")
        cocotb.log.info(f"[TEST]   Duty cycle: {duty_cycle:.1f}% (expected {expected_duty_cycles[i]}%)")
        cocotb.log.info(f"[TEST]   Transitions: {pwm_transitions[i]}")
        
        if pwm_transitions[i] == 0:
            cocotb.log.error(f"[TEST] PWM{i} has no transitions - stuck at {pwm_last_values[i]} - FAIL")
            all_pass = False
        elif abs(duty_cycle - expected_duty_cycles[i]) > tolerance:
            cocotb.log.error(f"[TEST] PWM{i} duty cycle {duty_cycle:.1f}% is not within {tolerance}% of {expected_duty_cycles[i]}% - FAIL")
            all_pass = False
        else:
            cocotb.log.info(f"[TEST] PWM{i} duty cycle {duty_cycle:.1f}% is within {tolerance}% of {expected_duty_cycles[i]}% - PASS")
    
    if all_pass:
        cocotb.log.info("[TEST] All 4 PWM channels passed - TEST PASSED")
    else:
        cocotb.log.error("[TEST] One or more PWM channels failed - TEST FAILED")
    
    cocotb.log.info("[TEST] 4-channel PWM test completed")
