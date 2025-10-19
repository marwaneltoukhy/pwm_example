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

    USER_writeWord(disable, 0x14L / 4);
    USER_writeWord(reload, 0x04L / 4);
    USER_writeWord(prescale, 0x08L / 4);
    USER_writeWord(config, 0x18L / 4);
    USER_writeWord(p0_ticks, 0x0cL / 4);
    USER_writeWord(cmpy_value, 0x10L / 4);
    USER_writeWord(match, 0x1cL / 4);
    USER_writeWord(match, 0x20L / 4);
    USER_writeWord(enable, 0x14L / 4);

    USER_writeWord(disable, 0x10000 / 4 + 0x14L / 4);
    USER_writeWord(reload, 0x10000 / 4 + 0x04L / 4);
    USER_writeWord(prescale, 0x10000 / 4 + 0x08L / 4);
    USER_writeWord(config, 0x10000 / 4 + 0x18L / 4);
    USER_writeWord(p1_ticks, 0x10000 / 4 + 0x0cL / 4);
    USER_writeWord(cmpy_value, 0x10000 / 4 + 0x10L / 4);
    USER_writeWord(match, 0x10000 / 4 + 0x1cL / 4);
    USER_writeWord(match, 0x10000 / 4 + 0x20L / 4);
    USER_writeWord(enable, 0x10000 / 4 + 0x14L / 4);

    USER_writeWord(disable, 0x20000 / 4 + 0x14L / 4);
    USER_writeWord(reload, 0x20000 / 4 + 0x04L / 4);
    USER_writeWord(prescale, 0x20000 / 4 + 0x08L / 4);
    USER_writeWord(config, 0x20000 / 4 + 0x18L / 4);
    USER_writeWord(p2_ticks, 0x20000 / 4 + 0x0cL / 4);
    USER_writeWord(cmpy_value, 0x20000 / 4 + 0x10L / 4);
    USER_writeWord(match, 0x20000 / 4 + 0x1cL / 4);
    USER_writeWord(match, 0x20000 / 4 + 0x20L / 4);
    USER_writeWord(enable, 0x20000 / 4 + 0x14L / 4);

    USER_writeWord(disable, 0x30000 / 4 + 0x14L / 4);
    USER_writeWord(reload, 0x30000 / 4 + 0x04L / 4);
    USER_writeWord(prescale, 0x30000 / 4 + 0x08L / 4);
    USER_writeWord(config, 0x30000 / 4 + 0x18L / 4);
    USER_writeWord(p3_ticks, 0x30000 / 4 + 0x0cL / 4);
    USER_writeWord(cmpy_value, 0x30000 / 4 + 0x10L / 4);
    USER_writeWord(match, 0x30000 / 4 + 0x1cL / 4);
    USER_writeWord(match, 0x30000 / 4 + 0x20L / 4);
    USER_writeWord(enable, 0x30000 / 4 + 0x14L / 4);
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
    dummyDelay(_DELAY_VALUE);
    
    ManagmentGpio_write(1);
    config_pwm_ticks(6000, 6000, 6000, 6000);
    dummyDelay(_DELAY_VALUE);
    
    ManagmentGpio_write(0);
    config_pwm_ticks(18000, 18000, 18000, 18000);
    dummyDelay(_DELAY_VALUE);
    
    ManagmentGpio_write(1);
    config_pwm_ticks(30000, 30000, 30000, 30000);
    dummyDelay(_DELAY_VALUE);
    
    ManagmentGpio_write(0);
}
