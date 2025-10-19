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
    
    async def verify_pwm_range(pin_num, pwm_name, expected_min, expected_max, num_samples=2):
        await measure_pwm_pulse(pin_num)
        
        pulse_widths = []
        for i in range(num_samples):
            pulse_width = await measure_pwm_pulse(pin_num)
            if pulse_width > 0:
                pulse_widths.append(pulse_width)
                cocotb.log.info(f"[TEST] {pwm_name} pulse width sample {i+1}: {pulse_width} cycles")
        
        if pulse_widths:
            avg_pulse_width = sum(pulse_widths) / len(pulse_widths)
            cocotb.log.info(f"[TEST] {pwm_name} average pulse width: {avg_pulse_width:.0f} cycles")
            cocotb.log.info(f"[TEST] Expected range: {expected_min} - {expected_max} cycles")
            
            if expected_min <= avg_pulse_width <= expected_max:
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
    result3 = await verify_pwm_range(2, "PWM2", 16000, 20000)
    result4 = await verify_pwm_range(3, "PWM3", 16000, 20000)
    
    cocotb.log.info("[TEST] Phase 2: Testing minimum position (6000 ticks ~500us)")
    await caravelEnv.wait_mgmt_gpio(1)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result5 = await verify_pwm_range(0, "PWM0", 4000, 8000)
    result6 = await verify_pwm_range(1, "PWM1", 4000, 8000)
    result7 = await verify_pwm_range(2, "PWM2", 4000, 8000)
    result8 = await verify_pwm_range(3, "PWM3", 4000, 8000)
    
    cocotb.log.info("[TEST] Phase 3: Testing neutral position again (18000 ticks ~1500us)")
    await caravelEnv.wait_mgmt_gpio(0)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result9 = await verify_pwm_range(0, "PWM0", 16000, 20000)
    result10 = await verify_pwm_range(1, "PWM1", 16000, 20000)
    result11 = await verify_pwm_range(2, "PWM2", 16000, 20000)
    result12 = await verify_pwm_range(3, "PWM3", 16000, 20000)
    
    cocotb.log.info("[TEST] Phase 4: Testing maximum position (30000 ticks ~2500us)")
    await caravelEnv.wait_mgmt_gpio(1)
    await ClockCycles(caravelEnv.clk, 10000)
    
    result13 = await verify_pwm_range(0, "PWM0", 28000, 32000)
    result14 = await verify_pwm_range(1, "PWM1", 28000, 32000)
    result15 = await verify_pwm_range(2, "PWM2", 28000, 32000)
    result16 = await verify_pwm_range(3, "PWM3", 28000, 32000)
    
    all_results = [result1, result2, result3, result4, result5, result6, result7, result8,
                   result9, result10, result11, result12, result13, result14, result15, result16]
    
    passed = sum(all_results)
    total = len(all_results)
    
    cocotb.log.info(f"[TEST] Test Summary: {passed}/{total} checks passed")
    
    if all(all_results):
        cocotb.log.info("[TEST] PWM Servo Test PASSED")
    else:
        cocotb.log.error("[TEST] PWM Servo Test FAILED")
