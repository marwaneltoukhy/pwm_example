# SPDX-FileCopyrightText: 2023 Efabless Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0

from caravel_cocotb.caravel_interfaces import test_configure, report_test
import cocotb
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge
import logging

@cocotb.test()
@report_test
async def pwm_servo_test(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=30000000)
    
    cocotb.log.info("[TEST] Starting PWM Servo Test")
    
    await caravelEnv.release_csb()
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Firmware configuration complete")
    
    async def measure_pwm_pulse(pin_num, timeout_cycles=300000):
        await RisingEdge(caravelEnv.clk)
        for _ in range(timeout_cycles):
            pin_val = caravelEnv.monitor_gpio(pin_num, pin_num).integer
            if pin_val == 1:
                break
            await RisingEdge(caravelEnv.clk)
        else:
            cocotb.log.warning(f"Timeout waiting for PWM{pin_num} rising edge")
            return 0
        
        high_time = 0
        for _ in range(timeout_cycles):
            pin_val = caravelEnv.monitor_gpio(pin_num, pin_num).integer
            if pin_val == 0:
                break
            high_time += 1
            await RisingEdge(caravelEnv.clk)
        else:
            cocotb.log.warning(f"Timeout waiting for PWM{pin_num} falling edge")
            return 0
        
        return high_time
    
    async def verify_pwm_range(pin_num, pwm_name, expected_min, expected_max):
        await measure_pwm_pulse(pin_num)
        
        pulse_width = await measure_pwm_pulse(pin_num)
        if pulse_width > 0:
            cocotb.log.info(f"[TEST] {pwm_name} pulse width: {pulse_width} cycles")
            cocotb.log.info(f"[TEST] Expected range: {expected_min} - {expected_max} cycles")
            
            if expected_min <= pulse_width <= expected_max:
                cocotb.log.info(f"[TEST] {pwm_name} pulse width PASSED")
                return True
            else:
                cocotb.log.error(f"[TEST] {pwm_name} pulse width FAILED - out of range")
                return False
        else:
            cocotb.log.error(f"[TEST] {pwm_name} no valid pulse measurements")
            return False
    
    cocotb.log.info("[TEST] Phase 1: Testing neutral position (18000 ticks ~1500us)")
    await caravelEnv.wait_mgmt_gpio(0)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result1 = await verify_pwm_range(0, "PWM0", 16000, 20000)
    result2 = await verify_pwm_range(1, "PWM1", 16000, 20000)
    
    cocotb.log.info("[TEST] Phase 2: Testing minimum position (6000 ticks ~500us)")
    await caravelEnv.wait_mgmt_gpio(1)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result3 = await verify_pwm_range(0, "PWM0", 4000, 8000)
    result4 = await verify_pwm_range(1, "PWM1", 4000, 8000)
    
    cocotb.log.info("[TEST] Phase 3: Testing neutral position again (18000 ticks ~1500us)")
    await caravelEnv.wait_mgmt_gpio(0)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result5 = await verify_pwm_range(0, "PWM0", 16000, 20000)
    result6 = await verify_pwm_range(1, "PWM1", 16000, 20000)
    
    cocotb.log.info("[TEST] Phase 4: Testing maximum position (30000 ticks ~2500us)")
    await caravelEnv.wait_mgmt_gpio(1)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result7 = await verify_pwm_range(0, "PWM0", 28000, 32000)
    result8 = await verify_pwm_range(1, "PWM1", 28000, 32000)
    
    all_results = [result1, result2, result3, result4, result5, result6, result7, result8]
    
    passed = sum(all_results)
    total = len(all_results)
    
    cocotb.log.info(f"[TEST] Test Summary: {passed}/{total} checks passed")
    
    if all(all_results):
        cocotb.log.info("[TEST] PWM Servo Test PASSED")
    else:
        cocotb.log.error("[TEST] PWM Servo Test FAILED")
