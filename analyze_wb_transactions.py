#!/usr/bin/env python3
"""Analyze Wishbone transactions in VCD file"""

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

print(f"\nAnalyzing Wishbone transactions...")
print(f"Time window: looking at cyc transitions\n")

# Find rising edges of wbs_cyc
transactions = []
for i in range(len(wbs_cyc.tv) - 1):
    t, v = wbs_cyc.tv[i]
    t_next, v_next = wbs_cyc.tv[i + 1]
    
    if v == '0' and v_next == '1':
        # Rising edge of cyc - start of transaction
        # Sample other signals at this time
        stb_val = wbs_stb[t_next]
        we_val = wbs_we[t_next]
        adr_val = wbs_adr[t_next]
        dat_val = wbs_dat_i[t_next]
        ack_val = wbs_ack[t_next]
        
        transactions.append({
            'time': t_next,
            'stb': stb_val,
            'we': we_val,
            'adr': adr_val,
            'dat': dat_val,
            'ack': ack_val
        })

print(f"Found {len(transactions)} Wishbone transactions\n")

# Print first 20 transactions
for i, txn in enumerate(transactions[:20]):
    t = txn['time']
    adr = txn['adr']
    we = txn['we']
    dat = txn['dat']
    ack = txn['ack']
    
    # Try to parse address as hex
    try:
        if 'x' not in adr and 'z' not in adr:
            adr_int = int(adr, 2)
            adr_hex = f"0x{adr_int:08x}"
        else:
            adr_hex = adr
    except:
        adr_hex = adr
    
    # Try to parse data as hex
    try:
        if 'x' not in dat and 'z' not in dat:
            dat_int = int(dat, 2)
            dat_hex = f"0x{dat_int:08x}"
        else:
            dat_hex = dat
    except:
        dat_hex = dat
    
    rw = "WRITE" if we == '1' else "READ"
    print(f"[{i}] {t}ps: {rw} addr={adr_hex} data={dat_hex} ack={ack}")

print(f"\n... (showing first 20 of {len(transactions)} total)")
