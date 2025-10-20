from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
from cocotb.triggers import RisingEdge

@cocotb.test()
@report_test
async def pwm_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10_000_000)
    
    await caravelEnv.release_csb()
    
    await caravelEnv.wait_mgmt_gpio(1)
    
    cocotb.log.info("[TEST] Firmware completed configuration, checking 6 PWMs (io[13:8])")
    
    pwm_high_seen = [False] * 6
    pwm_low_seen = [False] * 6
    check_cycles = 50000
    
    for cycle in range(check_cycles):
        await RisingEdge(caravelEnv.clk)
        
        io_str = caravelEnv.monitor_gpio(13, 8).binstr
        
        try:
            for i in range(6):
                pwm_val = io_str[5-i]
                if pwm_val == '1':
                    pwm_high_seen[i] = True
                elif pwm_val == '0':
                    pwm_low_seen[i] = True
                    
        except (ValueError, IndexError):
            pass
        
        if all(pwm_high_seen) and all(pwm_low_seen):
            cocotb.log.info(f"[TEST] All 6 PWMs toggling after {cycle} cycles")
            break
    
    cocotb.log.info(f"[TEST] PWM high seen (PWM0-5): {pwm_high_seen}")
    cocotb.log.info(f"[TEST] PWM low seen (PWM0-5): {pwm_low_seen}")
    
    if not (all(pwm_high_seen) and all(pwm_low_seen)):
        cocotb.log.error("[TEST] ERROR: Not all 6 PWM outputs toggled properly")
        assert False, "PWM test failed - not all outputs toggling"
    
    cocotb.log.info("[TEST] SUCCESS: All 6 PWM outputs (3 timers) are functional and toggling")