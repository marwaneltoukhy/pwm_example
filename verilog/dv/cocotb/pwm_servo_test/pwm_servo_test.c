// SPDX-FileCopyrightText: 2023 Efabless Corporation

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <firmware_apis.h>

#define CSR_PWM0_BASE 0x30000000L
#define CSR_PWM1_BASE 0x30010000L
#define CSR_PWM2_BASE 0x30020000L
#define CSR_PWM3_BASE 0x30030000L

void config_pwm_ticks(int p0_ticks, int p1_ticks, int p2_ticks, int p3_ticks)
{
    const int reload = 240000;
    const int prescale = 0;
    const int config = 0b110;
    const int cmpy_value = 2400000;
    const int disable = 0b0000;
    const int enable = 0b1101;
    const int match  = 0b000010000110;

    USER_writeWord(CSR_PWM0_BASE + 0x14L, disable);
    USER_writeWord(CSR_PWM0_BASE + 0x04L, reload);
    USER_writeWord(CSR_PWM0_BASE + 0x08L, prescale);
    USER_writeWord(CSR_PWM0_BASE + 0x18L, config);
    USER_writeWord(CSR_PWM0_BASE + 0x0cL, p0_ticks);
    USER_writeWord(CSR_PWM0_BASE + 0x10L, cmpy_value);
    USER_writeWord(CSR_PWM0_BASE + 0x1cL, match);
    USER_writeWord(CSR_PWM0_BASE + 0x20L, match);
    USER_writeWord(CSR_PWM0_BASE + 0x14L, enable);

    USER_writeWord(CSR_PWM1_BASE + 0x14L, disable);
    USER_writeWord(CSR_PWM1_BASE + 0x04L, reload);
    USER_writeWord(CSR_PWM1_BASE + 0x08L, prescale);
    USER_writeWord(CSR_PWM1_BASE + 0x18L, config);
    USER_writeWord(CSR_PWM1_BASE + 0x0cL, p1_ticks);
    USER_writeWord(CSR_PWM1_BASE + 0x10L, cmpy_value);
    USER_writeWord(CSR_PWM1_BASE + 0x1cL, match);
    USER_writeWord(CSR_PWM1_BASE + 0x20L, match);
    USER_writeWord(CSR_PWM1_BASE + 0x14L, enable);

    USER_writeWord(CSR_PWM2_BASE + 0x14L, disable);
    USER_writeWord(CSR_PWM2_BASE + 0x04L, reload);
    USER_writeWord(CSR_PWM2_BASE + 0x08L, prescale);
    USER_writeWord(CSR_PWM2_BASE + 0x18L, config);
    USER_writeWord(CSR_PWM2_BASE + 0x0cL, p2_ticks);
    USER_writeWord(CSR_PWM2_BASE + 0x10L, cmpy_value);
    USER_writeWord(CSR_PWM2_BASE + 0x1cL, match);
    USER_writeWord(CSR_PWM2_BASE + 0x20L, match);
    USER_writeWord(CSR_PWM2_BASE + 0x14L, enable);

    USER_writeWord(CSR_PWM3_BASE + 0x14L, disable);
    USER_writeWord(CSR_PWM3_BASE + 0x04L, reload);
    USER_writeWord(CSR_PWM3_BASE + 0x08L, prescale);
    USER_writeWord(CSR_PWM3_BASE + 0x18L, config);
    USER_writeWord(CSR_PWM3_BASE + 0x0cL, p3_ticks);
    USER_writeWord(CSR_PWM3_BASE + 0x10L, cmpy_value);
    USER_writeWord(CSR_PWM3_BASE + 0x1cL, match);
    USER_writeWord(CSR_PWM3_BASE + 0x20L, match);
    USER_writeWord(CSR_PWM3_BASE + 0x14L, enable);
}

void main()
{
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configureAll(GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_loadConfigs();
    
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    const int _DELAY_VALUE = 800000;
    
    ManagmentGpio_write(0);
    config_pwm_ticks(18000, 18000, 18000, 18000);
    delay_cyc(_DELAY_VALUE);
    
    ManagmentGpio_write(1);
    config_pwm_ticks(6000, 6000, 6000, 6000);
    delay_cyc(_DELAY_VALUE);
    
    ManagmentGpio_write(0);
    config_pwm_ticks(18000, 18000, 18000, 18000);
    delay_cyc(_DELAY_VALUE);
    
    ManagmentGpio_write(1);
    config_pwm_ticks(30000, 30000, 30000, 30000);
    delay_cyc(_DELAY_VALUE);
    
    ManagmentGpio_write(0);
}
