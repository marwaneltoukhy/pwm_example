#include <firmware_apis.h>
#include <CF_TMR32.h>

#define PWM0_BASE_ADDR ((CF_TMR32_TYPE_PTR)0x30000000)
#define PWM1_BASE_ADDR ((CF_TMR32_TYPE_PTR)0x30010000)
#define PWM2_BASE_ADDR ((CF_TMR32_TYPE_PTR)0x30020000)
#define PWM3_BASE_ADDR ((CF_TMR32_TYPE_PTR)0x30030000)

void configure_pwm_channel(CF_TMR32_TYPE_PTR base_addr, uint32_t cmpx_value) {
    CF_TMR32_setGclkEnable(base_addr, 1);
    CF_TMR32_setPR(base_addr, 9);
    CF_TMR32_setRELOAD(base_addr, 100);
    CF_TMR32_setCMPX(base_addr, cmpx_value);
    CF_TMR32_setCMPY(base_addr, 200);
    CF_TMR32_setUpCount(base_addr);
    CF_TMR32_setPeriodic(base_addr);
    CF_TMR32_setPWM0MatchingZeroAction(base_addr, CF_TMR32_ACTION_HIGH);
    CF_TMR32_setPWM0MatchingCMPXUpCountAction(base_addr, CF_TMR32_ACTION_LOW);
    CF_TMR32_setPWM0MatchingRELOADAction(base_addr, CF_TMR32_ACTION_LOW);
    CF_TMR32_PWM0Enable(base_addr);
    CF_TMR32_enable(base_addr);
    CF_TMR32_restart(base_addr);
}

void main(void) {
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    enableHkSpi(0);
    
    GPIOs_configure(0, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(1, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(2, GPIO_MODE_USER_STD_OUTPUT);
    GPIOs_configure(3, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    
    User_enableIF();
    
    configure_pwm_channel(PWM0_BASE_ADDR, 25);
    configure_pwm_channel(PWM1_BASE_ADDR, 50);
    configure_pwm_channel(PWM2_BASE_ADDR, 75);
    configure_pwm_channel(PWM3_BASE_ADDR, 90);
    
    ManagmentGpio_write(1);
    
    while(1);
}
