# PWM Servo Test Flow Diagram

## High-Level Test Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CARAVEL TEST ENVIRONMENT                      │
│                                                                  │
│  ┌────────────────────────┐         ┌──────────────────────┐   │
│  │  Management SoC        │         │  Python Testbench    │   │
│  │  (Runs Firmware)       │         │  (cocotb)            │   │
│  │                        │         │                      │   │
│  │  pwm_servo_test.c      │◄───────►│  pwm_servo_test.py   │   │
│  │                        │  GPIO   │                      │   │
│  │  - Configure GPIOs     │ Handshake│ - Monitor GPIO      │   │
│  │  - Write PWM registers │         │ - Measure PWM        │   │
│  │  - Control test phases │         │ - Verify outputs     │   │
│  └────────────┬───────────┘         └──────────┬───────────┘   │
│               │                                 │               │
│               │ Wishbone Bus                    │ Monitor       │
│               ▼                                 ▼               │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              USER PROJECT WRAPPER                      │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐│    │
│  │  │ PWM      │  │ PWM      │  │ PWM      │  │ PWM    ││    │
│  │  │ Timer 0  │  │ Timer 1  │  │ Timer 2  │  │ Timer 3││    │
│  │  │0x3000_   │  │0x3001_   │  │0x3002_   │  │0x3003_ ││    │
│  │  │0000      │  │0000      │  │0000      │  │0000    ││    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬───┘│    │
│  │       │             │             │             │     │    │
│  │       ▼             ▼             ▼             ▼     │    │
│  │    io_out[0]    io_out[1]    io_out[2]    io_out[3] │    │
│  └────────┬─────────────┬─────────────┬─────────────┬───┘    │
│           │             │             │             │         │
└───────────┼─────────────┼─────────────┼─────────────┼─────────┘
            │             │             │             │
            ▼             ▼             ▼             ▼
         PWM0          PWM1          PWM2          PWM3
      (to servo 0)  (to servo 1)  (to servo 2)  (to servo 3)
```

## Detailed Test Sequence

```
FIRMWARE (C)                 TESTBENCH (Python)              HARDWARE
═══════════                 ══════════════════              ═════════

Initialize GPIO
ManagmentGpio_write(0)
enableHkSpi(0)
Configure GPIOs
Load Configs
User_enableIF()
                                                            
ManagmentGpio_write(1) ────► wait_mgmt_gpio(1) ──────────► GPIO=1
  ║                            "Config complete"
  ║
  ║ PHASE 1: Neutral Position (18000 ticks)
  ║
ManagmentGpio_write(0) ────► wait_mgmt_gpio(0) ──────────► GPIO=0
config_pwm_ticks(18000)                                     
  ║                                                         PWM outputs
  ║                                                         start @ 1500us
  ║                                                            ║
  ║                          ClockCycles(10000)               ║
  ║                          measure_pwm_pulse(PWM0) ◄───────╣
  ║                          measure_pwm_pulse(PWM1) ◄───────╣
  ║                          measure_pwm_pulse(PWM2) ◄───────╣
  ║                          measure_pwm_pulse(PWM3) ◄───────╣
  ║                          verify_pwm_range()
  ║                          "PASSED: 16000-20000"
delay_cyc(800000)
  ║
  ║ PHASE 2: Minimum Position (6000 ticks)
  ║
ManagmentGpio_write(1) ────► wait_mgmt_gpio(1) ──────────► GPIO=1
config_pwm_ticks(6000)                                      
  ║                                                         PWM outputs
  ║                                                         change to 500us
  ║                                                            ║
  ║                          ClockCycles(10000)               ║
  ║                          measure_pwm_pulse(PWM0) ◄───────╣
  ║                          measure_pwm_pulse(PWM1) ◄───────╣
  ║                          measure_pwm_pulse(PWM2) ◄───────╣
  ║                          measure_pwm_pulse(PWM3) ◄───────╣
  ║                          verify_pwm_range()
  ║                          "PASSED: 4000-8000"
delay_cyc(800000)
  ║
  ║ PHASE 3: Neutral Position Again (18000 ticks)
  ║
ManagmentGpio_write(0) ────► wait_mgmt_gpio(0) ──────────► GPIO=0
config_pwm_ticks(18000)                                     
  ║                                                         PWM outputs
  ║                                                         return to 1500us
  ║                                                            ║
  ║                          ClockCycles(10000)               ║
  ║                          measure_pwm_pulse(PWM0) ◄───────╣
  ║                          measure_pwm_pulse(PWM1) ◄───────╣
  ║                          measure_pwm_pulse(PWM2) ◄───────╣
  ║                          measure_pwm_pulse(PWM3) ◄───────╣
  ║                          verify_pwm_range()
  ║                          "PASSED: 16000-20000"
delay_cyc(800000)
  ║
  ║ PHASE 4: Maximum Position (30000 ticks)
  ║
ManagmentGpio_write(1) ────► wait_mgmt_gpio(1) ──────────► GPIO=1
config_pwm_ticks(30000)                                     
  ║                                                         PWM outputs
  ║                                                         change to 2500us
  ║                                                            ║
  ║                          ClockCycles(10000)               ║
  ║                          measure_pwm_pulse(PWM0) ◄───────╣
  ║                          measure_pwm_pulse(PWM1) ◄───────╣
  ║                          measure_pwm_pulse(PWM2) ◄───────╣
  ║                          measure_pwm_pulse(PWM3) ◄───────╣
  ║                          verify_pwm_range()
  ║                          "PASSED: 28000-32000"
delay_cyc(800000)
  ║
ManagmentGpio_write(0) ────► 
  ║                          Test Summary
  ║                          "16/16 checks PASSED"
DONE                         "Test PASSED"
```

## PWM Signal Timing Diagram

```
Clock (12 MHz):  83.33 ns period
════════════════════════════════════════════════════════════════════

PWM Period: 20 ms (50 Hz)
┌───────────────────────────────────────────────────┐
│                                                    │
│            240000 clock cycles                     │
│                                                    │
└───────────────────────────────────────────────────┘


PHASE 1 & 3: Neutral Position (18000 ticks = 1500 μs)
────────────────────────────────────────────────────
     ┌──────────────────┐                              ┌────
     │                  │                              │
     │   18000 cycles   │      222000 cycles           │
     │     1500 μs      │        18.5 ms               │
─────┘                  └──────────────────────────────┘
     │                  │
     │◄────measured────►│


PHASE 2: Minimum Position (6000 ticks = 500 μs)
────────────────────────────────────────────────
     ┌──────┐                                          ┌────
     │      │                                          │
     │ 6000 │           234000 cycles                  │
     │cycles│             19.5 ms                      │
─────┘      └──────────────────────────────────────────┘
     │      │
     │◄meas►│


PHASE 4: Maximum Position (30000 ticks = 2500 μs)
────────────────────────────────────────────────────
     ┌──────────────────────────────┐                  ┌────
     │                              │                  │
     │       30000 cycles           │   210000 cycles  │
     │         2500 μs              │      17.5 ms     │
─────┘                              └──────────────────┘
     │                              │
     │◄──────────measured──────────►│
```

## Wishbone Bus Transaction Flow

```
Firmware Write to PWM Register Example: config_pwm_ticks(18000)
═══════════════════════════════════════════════════════════════

Step 1: Write RELOAD Register (0x30000004 = 240000)
────────────────────────────────────────────────────
Clock    : ─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─
           ┌─┘ └─┘ └─┘ └─┘ └─┘ └─
wbs_cyc_i: ────┐___________________
           ────┘
wbs_stb_i: ────┐___________________
           ────┘
wbs_we_i : ────┐___________________
           ────┘
wbs_adr_i: ────< 0x30000004 >──────
           ────────────────────────
wbs_dat_i: ────< 240000 >──────────
           ────────────────────────
wbs_ack_o: ────────┐_______________
           ────────┘


Step 2: Write CMPX Register (0x3000000C = 18000)
─────────────────────────────────────────────────
Clock    : ─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─
           ┌─┘ └─┘ └─┘ └─┘ └─┘ └─
wbs_cyc_i: ────┐___________________
           ────┘
wbs_stb_i: ────┐___________________
           ────┘
wbs_we_i : ────┐___________________
           ────┘
wbs_adr_i: ────< 0x3000000C >──────
           ────────────────────────
wbs_dat_i: ────< 18000 >───────────
           ────────────────────────
wbs_ack_o: ────────┐_______________
           ────────┘
```

## Measurement Algorithm Flow

```
measure_pwm_pulse(pin) Function
═══════════════════════════════════

START
  │
  ▼
Wait for Rising Edge ──┐
  │                    │
  │◄──────────────────┘ (timeout after 500k cycles)
  │
  ▼
Found Rising Edge?
  │
  ├─NO──► Return 0 (timeout)
  │
  YES
  │
  ▼
high_time = 0
  │
  ▼
Count Clock Cycles ────┐
high_time++            │
  │                    │
  ▼                    │
Falling Edge? ─NO─────►┘
  │
  YES
  │
  ▼
Return high_time
  │
  ▼
END

Example:
  Rising edge at cycle 1000
  Falling edge at cycle 19000
  → high_time = 18000 cycles
  → 18000 × 83.33ns = 1500 μs ✓
```

## Verification Logic Flow

```
verify_pwm_range(pin, name, min, max, samples=3)
═══════════════════════════════════════════════════

START
  │
  ▼
pulse_widths = []
  │
  ▼
FOR i in range(3): ────────┐
  │                         │
  ▼                         │
  pulse_width = measure()   │
  │                         │
  ▼                         │
  pulse_widths.append()     │
  │                         │
  └────────────────────────►┘
  │
  ▼
Calculate Average
avg = sum(pulse_widths) / 3
  │
  ▼
Check Range
min <= avg <= max?
  │
  ├─YES──► Log "PASSED"
  │         Return True
  │
  └─NO───► Log "FAILED"
            Return False

Example: Neutral Position Check
  Sample 1: 18050 cycles
  Sample 2: 17980 cycles
  Sample 3: 18020 cycles
  Average: 18017 cycles
  Expected: 16000-20000 cycles
  Result: PASSED ✓
```

## Error Handling

```
Timeout Detection
═════════════════

Firmware Side:
  - USER_writeWord() timeout → firmware hangs
  - Monitor with firmware timeout watchdog

Python Side:
  - test_configure(timeout_cycles=30000000)
  - measure_pwm_pulse(timeout_cycles=500000)
  - Explicit timeout checking in all async functions


No Pulse Detection
══════════════════

If measure_pwm_pulse() returns 0:
  │
  ▼
Log Warning: "Timeout waiting for PWM edge"
  │
  ▼
Skip this sample
  │
  ▼
Continue with next sample
  │
  ▼
If all samples timeout:
  │
  ▼
Report FAILED with error message


Out of Range Detection
═══════════════════════

If pulse_width < expected_min OR pulse_width > expected_max:
  │
  ▼
Log ERROR: "Pulse width FAILED - out of range"
  │
  ▼
Log actual value vs expected range
  │
  ▼
Return False
  │
  ▼
Final summary shows failed checks
```

## Resource Usage

```
Simulation Resources
════════════════════

Memory:
  RTL Simulation:  ~500 MB
  GL Simulation:   ~2-4 GB

Time:
  RTL Simulation:  ~5-10 minutes
  GL Simulation:   ~30-60 minutes

Waveform Size:
  Full dump:       ~200-500 MB
  Selective:       ~50-100 MB

CPU Cores:
  Single-threaded: 1 core
  Multi-threaded:  Can use 2-4 cores
```

## Summary

This test provides:
- ✅ Synchronized firmware-testbench execution
- ✅ Self-checking PWM pulse width verification
- ✅ Comprehensive error handling and logging
- ✅ Multiple measurement samples for robustness
- ✅ Clear pass/fail criteria
- ✅ Detailed phase-by-phase verification
- ✅ Production-ready test structure
