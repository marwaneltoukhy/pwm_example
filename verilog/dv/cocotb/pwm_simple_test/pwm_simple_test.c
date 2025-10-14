#include <firmware_apis.h>

#define PWM0_BASE_ADDR 0x30000000

#define TMR_REG_OFFSET        0x0000
#define RELOAD_REG_OFFSET     0x0004
#define PR_REG_OFFSET         0x0008
#define CMPX_REG_OFFSET       0x000C
#define CMPY_REG_OFFSET       0x0010
#define CTRL_REG_OFFSET       0x0014
#define CFG_REG_OFFSET        0x0018
#define PWM0CFG_REG_OFFSET    0x001C
#define PWM1CFG_REG_OFFSET    0x0020
#define GCLK_REG_OFFSET       0x0030

#define REG32(addr) *((volatile uint32_t *)(addr))

void main(void)
{
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    
    GPIOs_configure(0, GPIO_MODE_USER_STD_OUTPUT);
    
    GPIOs_loadConfigs();
    
    User_enableIF();
    
    REG32(PWM0_BASE_ADDR + GCLK_REG_OFFSET) = 0x1;
    
    REG32(PWM0_BASE_ADDR + PR_REG_OFFSET) = 9;
    
    REG32(PWM0_BASE_ADDR + RELOAD_REG_OFFSET) = 100;
    
    REG32(PWM0_BASE_ADDR + CMPX_REG_OFFSET) = 50;
    
    REG32(PWM0_BASE_ADDR + CMPY_REG_OFFSET) = 0;
    
    REG32(PWM0_BASE_ADDR + CFG_REG_OFFSET) = 0x3;
    
    REG32(PWM0_BASE_ADDR + PWM0CFG_REG_OFFSET) = 0x042;
    
    REG32(PWM0_BASE_ADDR + CTRL_REG_OFFSET) = 0x3;
    
    ManagmentGpio_write(1);
    
    while(1);
}
