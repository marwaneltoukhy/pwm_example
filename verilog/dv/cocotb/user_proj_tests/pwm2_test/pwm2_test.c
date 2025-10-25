#include <firmware_apis.h>
#include "CF_TMR32.h"
#include "CF_TMR32.c"

#define PWM2_BASE 0x30020000
#define PWM2 ((CF_TMR32_TYPE_PTR)PWM2_BASE)


void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(12, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(13, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    CF_TMR32_configureExamplePWM(PWM2);
    CF_TMR32_enable(PWM2);
    
    return;
}
