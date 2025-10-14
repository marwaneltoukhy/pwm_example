from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
from cocotb.triggers import ClockCycles

@cocotb.test()
@report_test
async def pwm_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1000000)
    
    cocotb.log.info("[TEST] Start PWM test")
    
    await caravelEnv.release_csb()
    
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Configuration complete")
    
    await ClockCycles(caravelEnv.clk, 10000)
    
    pwm0_state = caravelEnv.monitor_gpio(0, 0).integer
    pwm1_state = caravelEnv.monitor_gpio(1, 1).integer
    pwm2_state = caravelEnv.monitor_gpio(2, 2).integer
    pwm3_state = caravelEnv.monitor_gpio(3, 3).integer
    
    cocotb.log.info(f"[TEST] PWM0 output: {pwm0_state}")
    cocotb.log.info(f"[TEST] PWM1 output: {pwm1_state}")
    cocotb.log.info(f"[TEST] PWM2 output: {pwm2_state}")
    cocotb.log.info(f"[TEST] PWM3 output: {pwm3_state}")
    
    high_count_pwm0 = 0
    low_count_pwm0 = 0
    high_count_pwm1 = 0
    low_count_pwm1 = 0
    
    for i in range(1000):
        pwm0_val = caravelEnv.monitor_gpio(0, 0).integer
        pwm1_val = caravelEnv.monitor_gpio(1, 1).integer
        
        if pwm0_val == 1:
            high_count_pwm0 += 1
        else:
            low_count_pwm0 += 1
            
        if pwm1_val == 1:
            high_count_pwm1 += 1
        else:
            low_count_pwm1 += 1
        
        await ClockCycles(caravelEnv.clk, 1)
    
    cocotb.log.info(f"[TEST] PWM0 high count: {high_count_pwm0}, low count: {low_count_pwm0}")
    cocotb.log.info(f"[TEST] PWM1 high count: {high_count_pwm1}, low count: {low_count_pwm1}")
    
    duty_pwm0 = (high_count_pwm0 / 1000) * 100
    duty_pwm1 = (high_count_pwm1 / 1000) * 100
    
    cocotb.log.info(f"[TEST] PWM0 duty cycle: {duty_pwm0:.1f}%")
    cocotb.log.info(f"[TEST] PWM1 duty cycle: {duty_pwm1:.1f}%")
    
    if 45 <= duty_pwm0 <= 55:
        cocotb.log.info("[TEST] PWM0 duty cycle is approximately 50% - PASS")
    else:
        cocotb.log.error(f"[TEST] PWM0 duty cycle {duty_pwm0:.1f}% is not close to 50% - FAIL")
    
    if 20 <= duty_pwm1 <= 30:
        cocotb.log.info("[TEST] PWM1 duty cycle is approximately 25% - PASS")
    else:
        cocotb.log.error(f"[TEST] PWM1 duty cycle {duty_pwm1:.1f}% is not close to 25% - FAIL")
    
    cocotb.log.info("[TEST] PWM test completed")
