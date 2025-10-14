#include <firmware_apis.h>
#include <CF_TMR32.h>

#define PWM0_BASE_ADDR ((CF_TMR32_TYPE_PTR)0x30000000)

void delay(int cycles) {
    for (int i = 0; i < cycles; i++) {
        asm("nop");
    }
}

void main() {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(0, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_loadConfigs();
    User_enableIF();
    
    CF_TMR32_setGclkEnable(PWM0_BASE_ADDR, 1);
    
    ManagmentGpio_write(1);
    
    uint32_t test_cases[] = {0, 1, 99, 100};
    
    for(int i = 0; i < 4; i++) {
        CF_TMR32_disable(PWM0_BASE_ADDR);
        
        CF_TMR32_setPR(PWM0_BASE_ADDR, 9);
        CF_TMR32_setRELOAD(PWM0_BASE_ADDR, 100);
        CF_TMR32_setCMPX(PWM0_BASE_ADDR, test_cases[i]);
        CF_TMR32_setCMPY(PWM0_BASE_ADDR, 200);
        
        CF_TMR32_setUpCount(PWM0_BASE_ADDR);
        CF_TMR32_setPeriodic(PWM0_BASE_ADDR);
        
        CF_TMR32_setPWM0MatchingZeroAction(PWM0_BASE_ADDR, CF_TMR32_ACTION_HIGH);
        CF_TMR32_setPWM0MatchingCMPXUpCountAction(PWM0_BASE_ADDR, CF_TMR32_ACTION_LOW);
        CF_TMR32_setPWM0MatchingRELOADAction(PWM0_BASE_ADDR, CF_TMR32_ACTION_LOW);
        
        CF_TMR32_PWM0Enable(PWM0_BASE_ADDR);
        
        CF_TMR32_restart(PWM0_BASE_ADDR);
        CF_TMR32_enable(PWM0_BASE_ADDR);
        
        ManagmentGpio_write(0);
        delay(500);
        ManagmentGpio_write(1);
        delay(500);
    }
    
    while(1);
}
