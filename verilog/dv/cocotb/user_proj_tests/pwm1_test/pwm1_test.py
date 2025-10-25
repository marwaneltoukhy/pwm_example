from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
from cocotb.triggers import ClockCycles

@cocotb.test()
@report_test
async def pwm1_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=500000)
    
    cocotb.log.info("[TEST] Starting pwm1_test")
    
    await caravelEnv.release_csb()
    await caravelEnv.wait_mgmt_gpio(1)
    
    cocotb.log.info("[TEST] Firmware configuration complete")
    
    await ClockCycles(caravelEnv.clk, 10000)
    
    pwm_ch0_high = 0
    pwm_ch0_low = 0
    pwm_ch1_high = 0
    pwm_ch1_low = 0
    
    for i in range(4000):
        await ClockCycles(caravelEnv.clk, 1)
        
        ch0_val = caravelEnv.monitor_gpio(10, 10).integer
        ch1_val = caravelEnv.monitor_gpio(11, 11).integer
        
        if ch0_val == 1:
            pwm_ch0_high += 1
        else:
            pwm_ch0_low += 1
            
        if ch1_val == 1:
            pwm_ch1_high += 1
        else:
            pwm_ch1_low += 1
    
    duty_ch0 = (pwm_ch0_high / (pwm_ch0_high + pwm_ch0_low)) * 100
    duty_ch1 = (pwm_ch1_high / (pwm_ch1_high + pwm_ch1_low)) * 100
    
    cocotb.log.info(f"[TEST] PWM1 Channel 0: {pwm_ch0_high} high, {pwm_ch0_low} low, duty={duty_ch0:.2f}%")
    cocotb.log.info(f"[TEST] PWM1 Channel 1: {pwm_ch1_high} high, {pwm_ch1_low} low, duty={duty_ch1:.2f}%")
    
    if pwm_ch0_high > 100 and pwm_ch0_low > 100:
        cocotb.log.info("[TEST] PWM1 Channel 0 is toggling - PASS")
    else:
        cocotb.log.error("[TEST] PWM1 Channel 0 is NOT toggling - FAIL")
        
    if pwm_ch1_high > 100 and pwm_ch1_low > 100:
        cocotb.log.info("[TEST] PWM1 Channel 1 is toggling - PASS")
    else:
        cocotb.log.error("[TEST] PWM1 Channel 1 is NOT toggling - FAIL")
    
    cocotb.log.info("[TEST] pwm1_test complete")
