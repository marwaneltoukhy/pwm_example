from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb

@cocotb.test()
@report_test
async def pwm_simple_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10_000_000)
    
    await caravelEnv.release_csb()
    
    cocotb.log.info("[TEST] Start simple PWM test")
    
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Configuration complete")
    
    await cocotb.triggers.ClockCycles(caravelEnv.clk, 5000)
    
    pwm0_high_count = 0
    pwm0_low_count = 0
    
    cocotb.log.info("[TEST] Sampling PWM0 output for 5000 cycles...")
    
    for i in range(5000):
        await cocotb.triggers.ClockCycles(caravelEnv.clk, 1)
        pwm0_val = dut.uut.mprj.pwm0_0.value.integer
        
        if pwm0_val == 1:
            pwm0_high_count += 1
        else:
            pwm0_low_count += 1
    
    cocotb.log.info(f"[TEST] PWM0 output: {dut.uut.mprj.pwm0_0.value}")
    cocotb.log.info(f"[TEST] io_out[0]: {dut.uut.mprj.io_out[0].value}")
    cocotb.log.info(f"[TEST] io_oeb[0]: {dut.uut.mprj.io_oeb[0].value}")
    cocotb.log.info(f"[TEST] PWM0 high count: {pwm0_high_count}, low count: {pwm0_low_count}")
    
    if pwm0_high_count + pwm0_low_count > 0:
        duty_cycle = (pwm0_high_count / (pwm0_high_count + pwm0_low_count)) * 100
        cocotb.log.info(f"[TEST] PWM0 duty cycle: {duty_cycle:.1f}%")
        
        if abs(duty_cycle - 50.0) > 10.0:
            cocotb.log.error(f"[TEST] PWM0 duty cycle {duty_cycle:.1f}% is not close to 50% - FAIL")
        else:
            cocotb.log.info(f"[TEST] PWM0 duty cycle {duty_cycle:.1f}% is close to 50% - PASS")
    else:
        cocotb.log.error("[TEST] No PWM samples collected - FAIL")
    
    cocotb.log.info("[TEST] Simple PWM test completed")
