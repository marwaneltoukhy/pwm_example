#include <firmware_apis.h>

#define PWM0_BASE_ADDR 0x30000000
#define REG32(addr) *((volatile uint32_t *)(addr))

void main(void)
{
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    GPIOs_configure(0, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    
    User_enableIF();
    
    REG32(PWM0_BASE_ADDR + 0x30) = 0x1;
    
    uint32_t gclk_readback = REG32(PWM0_BASE_ADDR + 0x30);
    
    if (gclk_readback == 0x1) {
        ManagmentGpio_write(1);
    }
    
    while(1);
}
