#include <firmware_apis.h>
#include "CF_TMR32.h"
#include "CF_TMR32.c"

#define PWM3_BASE 0x30030000
#define PWM3 ((CF_TMR32_TYPE_PTR)PWM3_BASE)


void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(14, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(15, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    CF_TMR32_configureExamplePWM(PWM3);
    CF_TMR32_enable(PWM3);
    
    return;
}
