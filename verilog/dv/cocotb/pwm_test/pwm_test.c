#include <firmware_apis.h>
#include "CF_TMR32.h"

#define PWM0_BASE 0x30000000
#define PWM1_BASE 0x30010000
#define PWM2_BASE 0x30020000
#define PWM3_BASE 0x30030000

#define PWM0 ((CF_TMR32_TYPE_PTR)PWM0_BASE)
#define PWM1 ((CF_TMR32_TYPE_PTR)PWM1_BASE)
#define PWM2 ((CF_TMR32_TYPE_PTR)PWM2_BASE)
#define PWM3 ((CF_TMR32_TYPE_PTR)PWM3_BASE)

void configurePWM(CF_TMR32_TYPE_PTR pwm, uint32_t prescaler, uint32_t reload, uint32_t cmpx) {
    CF_TMR32_setGclkEnable(pwm, 1);
    CF_TMR32_setPR(pwm, prescaler);
    CF_TMR32_setRELOAD(pwm, reload);
    CF_TMR32_setCMPX(pwm, cmpx);
    CF_TMR32_setCMPY(pwm, 0);
    CF_TMR32_setUpCount(pwm);
    CF_TMR32_setPeriodic(pwm);
    CF_TMR32_setPWM0MatchingZeroAction(pwm, CF_TMR32_ACTION_HIGH);
    CF_TMR32_setPWM0MatchingCMPXUpCountAction(pwm, CF_TMR32_ACTION_LOW);
    CF_TMR32_PWM0Enable(pwm);
    CF_TMR32_enable(pwm);
    CF_TMR32_restart(pwm);
}

void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(0, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(1, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(2, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(3, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    
    User_enableIF();
    
    ManagmentGpio_write(1);
    
    configurePWM(PWM0, 9, 100, 50);
    configurePWM(PWM1, 9, 100, 25);
    configurePWM(PWM2, 9, 100, 75);
    configurePWM(PWM3, 9, 100, 90);
    
    return;
}
