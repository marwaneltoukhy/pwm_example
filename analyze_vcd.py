#!/usr/bin/env python3
"""
Analyze VCD waveform to debug PWM issue.
"""

import sys

def parse_vcd_signals(vcd_file, signals_of_interest):
    """
    Parse VCD file and extract specific signals.
    signals_of_interest is a dict like {'name': 'hierarchical.path'}
    """
    import gzip
    
    # Try to open as gzip first
    try:
        f = gzip.open(vcd_file, 'rt')
        f.read(1)
        f.close()
        f = gzip.open(vcd_file, 'rt')
    except:
        f = open(vcd_file, 'r')
    
    # Parse header to find signal codes
    signal_codes = {}
    in_scope = []
    
    for line in f:
        line = line.strip()
        
        if line.startswith('$scope'):
            parts = line.split()
            in_scope.append(parts[2])
        elif line.startswith('$upscope'):
            if in_scope:
                in_scope.pop()
        elif line.startswith('$var'):
            parts = line.split()
            code = parts[3]
            name = parts[4]
            full_name = '.'.join(in_scope) + '.' + name
            
            # Check if this is a signal we care about
            for sig_name, sig_path in signals_of_interest.items():
                if sig_path in full_name:
                    signal_codes[sig_name] = code
                    print(f"Found signal '{sig_name}' with code '{code}' at '{full_name}'")
        elif line.startswith('$enddefinitions'):
            break
    
    f.close()
    print(f"\nFound {len(signal_codes)} of {len(signals_of_interest)} signals")
    return signal_codes


def extract_signal_values(vcd_file, signal_codes, start_time=0, end_time=None, max_samples=100):
    """
    Extract signal values from VCD file.
    """
    import gzip
    
    try:
        f = gzip.open(vcd_file, 'rt')
        f.read(1)
        f.close()
        f = gzip.open(vcd_file, 'rt')
    except:
        f = open(vcd_file, 'r')
    
    # Skip to $enddefinitions
    for line in f:
        if line.strip().startswith('$enddefinitions'):
            break
    
    current_time = 0
    values = {name: [] for name in signal_codes.keys()}
    
    for line in f:
        line = line.strip()
        
        if line.startswith('#'):
            # Timestamp
            current_time = int(line[1:])
            
            if end_time and current_time > end_time:
                break
        else:
            # Value change
            if len(line) > 0:
                # Format: <value><code> or b<binary><code>
                if line[0] == 'b':
                    # Binary value
                    parts = line.split()
                    value = parts[0][1:]  # Remove 'b'
                    code = parts[1]
                else:
                    # Single bit value
                    value = line[0]
                    code = line[1:]
                
                # Check if this is a signal we care about
                for sig_name, sig_code in signal_codes.items():
                    if code == sig_code:
                        if current_time >= start_time:
                            values[sig_name].append((current_time, value))
                            if len(values[sig_name]) >= max_samples:
                                break
    
    f.close()
    return values


if __name__ == '__main__':
    vcd_file = '/workspace/pwm_example/verilog/dv/cocotb/sim/pwm_simple_run5/RTL-pwm_simple_test/waves.vcd'
    
    # Signals to check (in order of signal path)
    # Hierarchy: caravel_top.uut.chip_core.mprj.*
    signals = {
        # Wishbone master side (from caravel to user_project)
        'wbs_cyc_i': 'mprj.wbs_cyc_i',
        'wbs_stb_i': 'mprj.wbs_stb_i',
        'wbs_adr_i': 'mprj.wbs_adr_i',
        'wbs_dat_i': 'mprj.wbs_dat_i',
        'wbs_we_i': 'mprj.wbs_we_i',
        'wbs_ack_o': 'mprj.wbs_ack_o',
        
        # Bus splitter slave 0 (to CF_TMR32_WB #0)
        's_wb_cyc_0': 'bus_splitter_inst.s_wb_cyc_0',
        's_wb_stb_0': 'bus_splitter_inst.s_wb_stb_0',
        's_wb_adr_0': 'bus_splitter_inst.s_wb_adr_0',
        's_wb_dat_w_0': 'bus_splitter_inst.s_wb_dat_w_0',
        's_wb_we_0': 'bus_splitter_inst.s_wb_we_0',
        's_wb_ack_0': 'bus_splitter_inst.s_wb_ack_0',
        
        # CF_TMR32_WB #0 internal signals
        'pwm0_ack': 'pwm_timer_0.ack_o',
        'pwm0_gclk': 'pwm_timer_0.GCLK_REG',
        'pwm0_ctrl': 'pwm_timer_0.CTRL_REG',
        'pwm0_tmr_en': 'pwm_timer_0.instance_to_wrap.tmr_en',
        'pwm0_tmr_start': 'pwm_timer_0.instance_to_wrap.tmr_start',
        'pwm0_pwm0_en': 'pwm_timer_0.instance_to_wrap.pwm0_en',
        'pwm0_tmr': 'pwm_timer_0.instance_to_wrap.tmr',
        'pwm0_out': 'pwm_timer_0.pwm0',
        
        # Output to GPIO (check top-level GPIO signals)
        'gpio0': 'caravel_top.gpio0',
    }
    
    print("Searching for signals in VCD file...")
    signal_codes = parse_vcd_signals(vcd_file, signals)
    
    print("\nExtracting signal values after reset (~50000ns onwards)...")
    start_time = 50000    # Start after reset
    end_time = 200000     # Look at first 150us of simulation
    
    values = extract_signal_values(vcd_file, signal_codes, start_time, end_time, max_samples=50)
    
    print("\n=== Signal Activity Analysis ===")
    for sig_name, sig_values in values.items():
        print(f"\n{sig_name}:")
        if len(sig_values) == 0:
            print("  No changes detected in time window")
        else:
            for time, value in sig_values[:20]:  # Show first 20 changes
                print(f"  {time}ns: {value}")
