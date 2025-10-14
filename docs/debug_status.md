# PWM Project Debug Status Report

## Current Issue
All PWM outputs remain at logic 0 during testing, despite apparently correct configuration.

## What Has Been Done

### 1. Project Setup ✅
- Copied Caravel user project template
- Created comprehensive documentation (register_map.md, pad_map.md, integration_notes.md)
- Linked CF_TMR32 IP v2.1.0-nc (note: original design used v2.0.0, which is no longer available)

### 2. Design Review ✅
- Verified user_project_wrapper.v matches original design structure
- Added missing assignments for s_wb_err_0 through s_wb_err_3 (tied to 0)
- Confirmed PWM outputs wired to io_out[0:3]
- Confirmed io_oeb[7:0] = 8'b0 (outputs enabled)

### 3. Wishbone Protocol Fixes ✅
- **Fixed Critical Bug**: wb_bus_splitter.v was gating `cyc_i` based on address selection
  - This violated Wishbone B4 protocol
  - Changed to route `cyc_i` to ALL slaves unconditionally
  - Only `stb_i` is now gated based on address

### 4. Test Development ✅
- Created pwm_test.c using CF_TMR32 firmware API
- Created pwm_test.py with self-checking functionality
- Test configures 4 PWM channels with different duty cycles:
  - PWM0: 50% duty cycle (prescaler=9, reload=100, cmpx=50)
  - PWM1: 25% duty cycle (prescaler=9, reload=100, cmpx=25)
  - PWM2: 75% duty cycle (prescaler=9, reload=100, cmpx=75)
  - PWM3: 90% duty cycle (prescaler=9, reload=100, cmpx=90)

### 5. Firmware Improvements ✅
- Moved ManagmentGpio_write(1) after PWM configuration
- Ensures test doesn't start sampling before configuration completes
- Using CF_TMR32 API functions for configuration

## Test Results

### pwm_run8 (Latest)
- **Status**: FAIL
- **Configuration completes at**: 5880100ns
- **All PWM outputs**: Remain at logic 0
- **Expected**: PWM0=50%, PWM1=25%, PWM2=75%, PWM3=90%
- **Actual**: PWM0=0%, PWM1=0%, PWM2=0%, PWM3=0%

## Key Observations

1. **Firmware executes successfully**
   - ManagementGpio toggles correctly
   - Configuration sequence completes
   
2. **Wishbone protocol now correct**
   - cyc_i routed to all slaves
   - stb_i gated based on address selection
   
3. **GPIO configuration appears correct**
   - io_oeb[7:0] = 0 (outputs enabled)
   - GPIOs configured as USER_STD_OUTPUT

4. **Version Mismatch**
   - Original design used CF_TMR32 v2.0.0
   - Current system only has CF_TMR32 v2.1.0-nc
   - This may indicate API changes or behavioral differences

## Potential Root Causes

1. **IP Version Incompatibility**
   - v2.1.0-nc may have different register maps or configuration requirements
   - Firmware APIs may have changed between versions

2. **Clock Gating**
   - GCLK register needs to be set, but maybe clock isn't propagating?
   - Need to verify clock reaches CF_TMR32 modules in waveform

3. **Address Decoding**
   - CF_TMR32_WB uses adr_i[15:0] for register selection
   - Bus splitter uses adr_i[31:16] for peripheral selection
   - Need to verify actual Wishbone transactions in waveform

4. **Configuration Sequence**
   - Maybe the order of register writes matters?
   - Maybe some registers need delays between writes?

5. **GPIO Mux Selection**
   - Need to verify GPIO pads are actually in USER mode
   - Need to verify mux selects user project outputs

## Next Steps

1. **Examine VCD Waveform** (/workspace/pwm_example/verilog/dv/cocotb/sim/pwm_run8/RTL-pwm_test/waves.vcd)
   - Verify Wishbone transactions reach CF_TMR32 modules
   - Check if ack_o is being asserted
   - Verify clock propagation to CF_TMR32
   - Check internal CF_TMR32 signals (counter, enable flags, pwm output)
   - Verify GPIO mux selection

2. **Compare CF_TMR32 Versions**
   - Check if there are documented changes between v2.0.0 and v2.1.0-nc
   - Look at firmware API differences
   - Check if register maps changed

3. **Simplify Test**
   - Create minimal test that just writes/reads one register
   - Verify basic Wishbone connectivity before complex PWM configuration

4. **Consult User**
   - Report current status
   - Ask if they have access to v2.0.0 of CF_TMR32
   - Ask if they know of any specific changes in v2.1.0-nc

## Files Modified

1. `/workspace/pwm_example/verilog/rtl/wb_bus_splitter.v` - Fixed Wishbone protocol
2. `/workspace/pwm_example/verilog/rtl/user_project_wrapper.v` - Added s_wb_err tie-offs
3. `/workspace/pwm_example/verilog/dv/cocotb/pwm_test/pwm_test.c` - Firmware timing fix
4. `/workspace/pwm_example/verilog/dv/cocotb/pwm_test/pwm_test.py` - Test implementation
5. `/workspace/pwm_example/ip/dependencies.json` - Updated to v2.1.0-nc

## Waveform Location
/workspace/pwm_example/verilog/dv/cocotb/sim/pwm_run8/RTL-pwm_test/waves.vcd
