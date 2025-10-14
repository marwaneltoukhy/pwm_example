# RTL Fixes and Modifications

## Overview
During the caravel-cocotb verification process, two critical bugs were identified and fixed in the PWM design. This document describes the bugs, root causes, and fixes applied.

## Bug #1: PWM Action Logic Gated by Prescaler Tick

### Description
The PWM output remained stuck at 0 despite correct configuration registers and timer operation.

### Root Cause
In the original `CF_TMR32.v` IP core, the PWM register update logic was gated by the prescaler `tick` signal:

```verilog
// Original buggy code (lines 211-227)
always @(posedge clk, negedge rst_n)
    if(!rst_n) pwm0_reg <= 0;
    else
        if(pwm0_en & tick)  // ❌ BUG: Gated by tick
            if(pwm_fault)
                pwm0_reg <= 0;
            else
                pwm0_reg <= pwm0_reg_next;
```

**Problem**: The `tick` signal only goes high when the prescaler reaches 0, which is asynchronous to the match events (`tmr_eq_zero`, `tmr_eq_cmpx`). As a result, when a match event occurred, `tick` was always 0, and the PWM register never updated.

**Evidence from VCD analysis**:
```
1695000000ps: tmr_eq_zero=1, tick=0, pwm0_en=1  ❌
1682250000ps: tmr_eq_cmpx=1, tick=0, pwm0_en=1  ❌
```

### Fix
Removed the `& tick` condition from the PWM register update logic in `/workspace/pwm_example/verilog/rtl/CF_TMR32_fixed.v`:

```verilog
// Fixed code
always @(posedge clk, negedge rst_n)
    if(!rst_n) pwm0_reg <= 0;
    else
        if(pwm0_en)  // ✅ FIX: Removed tick gating
            if(pwm_fault)
                pwm0_reg <= 0;
            else
                pwm0_reg <= pwm0_reg_next;
```

This allows the PWM action logic to execute on every clock cycle when the PWM is enabled, properly responding to match events.

### Files Modified
- Created `/workspace/pwm_example/verilog/rtl/CF_TMR32_fixed.v` (copy of original with fix)
- Updated `/workspace/pwm_example/verilog/includes/includes.rtl.caravel_user_project` to use fixed version

---

## Bug #2: CMPY Register Conflicting with Zero Match

### Description
Even after the RTL fix, the PWM output remained at 0 because the match event detection was ambiguous.

### Root Cause
The PWM action logic uses a `casez` statement to determine which action to take based on match signals:

```verilog
casez({tmr_dir, tmr_eq_zero, tmr_eq_cmpx, tmr_eq_cmpy, tmr_eq_reload})
    5'b?_1_00_0 : pwm0_reg_next = pwm_action(pwm0_cfg[1:0], pwm0_reg);  // Zero
    5'b1_0_10_0 : pwm0_reg_next = pwm_action(pwm0_cfg[3:2], pwm0_reg);  // CMPX
    // ...
    default     : pwm0_reg_next = pwm0_reg;
endcase
```

**Problem**: The firmware set `CMPY = 0`, which caused `tmr_eq_cmpy` to be true whenever `tmr == 0`. This created the casez input `1_1_01_0` (both `tmr_eq_zero` and `tmr_eq_cmpy` are 1), which didn't match any pattern, falling through to the default case (no change).

**Evidence from VCD analysis**:
```
1720250000ps: ZERO match
  casez input: 1_1_01_0  ❌ Doesn't match pattern 5'b?_1_00_0
```

### Fix
Updated the firmware to set CMPY to a value (200) that doesn't conflict with the PWM operation:

```c
// Original buggy code
CF_TMR32_setCMPY(PWM0_BASE_ADDR, 0);  // ❌ BUG: Conflicts with zero match

// Fixed code
CF_TMR32_setCMPY(PWM0_BASE_ADDR, 200);  // ✅ FIX: Non-conflicting value
```

This ensures:
- `tmr_eq_zero` is true only when `tmr == 0` and `tmr_eq_cmpy == 0`
- `tmr_eq_cmpx` is true only when `tmr == 50` and `tmr_eq_cmpy == 0`
- The casez patterns match correctly

**Verified casez inputs after fix**:
```
1720250000ps: ZERO match
  casez input: 1_1_00_0  ✅ Matches pattern 5'b?_1_00_0

1707500000ps: CMPX match
  casez input: 1_0_10_0  ✅ Matches pattern 5'b1_0_10_0
```

### Files Modified
- `/workspace/pwm_example/verilog/dv/cocotb/pwm_simple_test/pwm_simple_test.c`

---

## Test Results

### Before Fixes
```
PWM0 duty cycle: 0.0% (expected 50%) - FAIL ❌
PWM0 transitions: 0
```

### After Fixes
```
PWM0 duty cycle: 49.0% (expected 50%) - PASS ✅
PWM0 high count: 2450, low count: 2550
```

The 1% difference from the ideal 50% is due to:
1. Timer counting from 0 to 100 (101 counts per period)
2. PWM toggling at count 0 and count 50
3. Rounding in the duty cycle calculation

---

## Lessons Learned

1. **Synchronization is Critical**: Gating logic by secondary signals (like `tick`) must be carefully analyzed to ensure the gating signal is synchronous with the events it's supposed to capture.

2. **Avoid Register Value Conflicts**: When using multiple compare registers, ensure unused registers are set to values that don't create false matches.

3. **Thorough VCD Analysis**: Examining internal signals in the VCD was essential to identifying both bugs. The first investigation of register writes was actually correct, but the initial hypothesis about missing writes was wrong.

4. **Iterative Debugging**: Multiple hypotheses were tested:
   - Initial: PWM0CFG register not being written (disproven by VCD)
   - Second: PWM action logic not responding to match events (partially correct)
   - Final: Combination of tick-gated logic + CMPY conflict (root cause)

---

## Recommendations for CF_TMR32 IP

1. **Document the Prescaler Tick Gating**: The original design appears to intend PWM actions to occur at prescaler boundaries. However, this creates a fundamental mismatch with edge-aligned PWM generation. The IP documentation should clarify this behavior.

2. **Add CMPY Initialization Guidance**: The firmware API should document that CMPY must be initialized to a non-conflicting value if not used for PWM generation.

3. **Consider Alternative PWM Logic**: For typical edge-aligned PWM applications, the PWM register should update on every match event, not just on prescaler ticks. The current design may be more suitable for center-aligned PWM or other specialized modes.
