#include <firmware_apis.h>
#include "CF_TMR32.h"
#include "CF_TMR32.c"

#define PWM0_BASE 0x30000000
#define PWM0 ((CF_TMR32_TYPE_PTR)PWM0_BASE)


void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(8, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(9, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    CF_TMR32_configureExamplePWM(PWM0);
    CF_TMR32_enable(PWM0);
    
    return;
}
