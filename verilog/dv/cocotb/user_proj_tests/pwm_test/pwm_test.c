#include <firmware_apis.h>
#include <CF_TMR32.h>
#include <CF_TMR32.c>

#define TMR0_BASE_ADDRESS 0x30000000
#define TMR1_BASE_ADDRESS 0x30010000
#define TMR2_BASE_ADDRESS 0x30020000
#define TMR3_BASE_ADDRESS 0x30030000

void main(void)
{
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);

    enableHkSpi(0);

    GPIOs_configureAll(GPIO_MODE_USER_STD_OUT_MONITORED);
    
    GPIOs_configure(8, GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(9, GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(10, GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(11, GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(12, GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(13, GPIO_MODE_USER_STD_OUT_MONITORED);
    
    GPIOs_loadConfigs();

    User_enableIF();

    ManagmentGpio_write(1);

    CF_TMR32_TYPE_PTR tmr0 = (CF_TMR32_TYPE_PTR)TMR0_BASE_ADDRESS;
    CF_TMR32_TYPE_PTR tmr1 = (CF_TMR32_TYPE_PTR)TMR1_BASE_ADDRESS;
    CF_TMR32_TYPE_PTR tmr2 = (CF_TMR32_TYPE_PTR)TMR2_BASE_ADDRESS;

    CF_TMR32_configureExamplePWM(tmr0);
    CF_TMR32_enable(tmr0);

    CF_TMR32_configureExamplePWM(tmr1);
    CF_TMR32_enable(tmr1);

    CF_TMR32_configureExamplePWM(tmr2);
    CF_TMR32_enable(tmr2);

    return;
}