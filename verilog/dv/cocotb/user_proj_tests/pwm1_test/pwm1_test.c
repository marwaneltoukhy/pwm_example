#include <firmware_apis.h>
#include "CF_TMR32.h"
#include "CF_TMR32.c"

#define PWM1_BASE 0x30010000
#define PWM1 ((CF_TMR32_TYPE_PTR)PWM1_BASE)


void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(10, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(11, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    CF_TMR32_configureExamplePWM(PWM1);
    CF_TMR32_enable(PWM1);
    
    return;
}
