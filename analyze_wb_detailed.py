#!/usr/bin/env python3
"""Detailed Wishbone transaction analysis"""

from vcdvcd import VCDVCD

vcd_file = '/workspace/pwm_example/verilog/dv/cocotb/sim/pwm_simple_run5/RTL-pwm_simple_test/waves.vcd'

print(f"Loading VCD: {vcd_file}")
vcd = VCDVCD(vcd_file)

# Get Wishbone signals
wbs_cyc = vcd['caravel_top.uut.chip_core.mprj.wbs_cyc_i']
wbs_stb = vcd['caravel_top.uut.chip_core.mprj.wbs_stb_i']
wbs_we = vcd['caravel_top.uut.chip_core.mprj.wbs_we_i']
wbs_adr = vcd['caravel_top.uut.chip_core.mprj.wbs_adr_i[31:0]']
wbs_dat_i = vcd['caravel_top.uut.chip_core.mprj.wbs_dat_i[31:0]']
wbs_ack = vcd['caravel_top.uut.chip_core.mprj.wbs_ack_o']

print(f"\nLooking at first 10 WB transactions...\n")

# Find rising edges of wbs_cyc (transaction starts)
count = 0
for i in range(len(wbs_cyc.tv) - 1):
    t, v = wbs_cyc.tv[i]
    t_next, v_next = wbs_cyc.tv[i + 1]
    
    if v == '0' and v_next == '1':
        if count >= 10:
            break
        count += 1
        
        # Sample signals at cycle start
        stb_val = wbs_stb[t_next]
        we_val = wbs_we[t_next]
        adr_val = wbs_adr[t_next]
        dat_val = wbs_dat_i[t_next]
        
        # Find ACK response (look ahead a bit)
        ack_time = None
        for j in range(len(wbs_ack.tv)):
            ack_t, ack_v = wbs_ack.tv[j]
            if ack_t > t_next and ack_v == '1':
                ack_time = ack_t
                break
        
        # Parse address
        try:
            if 'x' not in adr_val and 'z' not in adr_val:
                adr_int = int(adr_val, 2)
                adr_hex = f"0x{adr_int:08x}"
            else:
                adr_hex = adr_val
        except:
            adr_hex = adr_val
        
        # Parse data
        try:
            if 'x' not in dat_val and 'z' not in dat_val:
                dat_int = int(dat_val, 2)
                dat_hex = f"0x{dat_int:08x}"
            else:
                dat_hex = dat_val
        except:
            dat_hex = dat_val
        
        rw = "WR" if we_val == '1' else "RD"
        ack_str = f"ACK@{ack_time}ps" if ack_time else "NO_ACK"
        print(f"[{count}] {t_next}ps: {rw} {adr_hex} = {dat_hex} -> {ack_str}")

# Now check PWM output signals
print(f"\n\nChecking PWM outputs (io_out[3:0])...")
io_out = vcd['caravel_top.uut.chip_core.mprj_io_one[7:0]']

print(f"\nio_out transitions (showing interesting times):")
for t, v in io_out.tv:
    if t > 1700000000 and t < 1950000000:  # After mgmt_gpio=1
        print(f"  {t}ps: {v}")
        break
else:
    print("  No transitions in sampling window")
    # Show last value
    print(f"  Last value: {io_out.tv[-1]}")
