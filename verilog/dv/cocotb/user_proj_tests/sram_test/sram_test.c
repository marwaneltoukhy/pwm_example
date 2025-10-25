#define USER_ADDR_SPACE_C_HEADER_FILE  // TODO disable using the other file until tag is updated and https://github.com/efabless/caravel_mgmt_soc_litex/pull/137 is merged

#include <firmware_apis.h>
#include "custom_user_space.h"
#include "ram_info.h"

#define SRAM0_BASE_OFFSET 0x10000
#define SRAM1_BASE_OFFSET 0x14000
#define SRAM2_BASE_OFFSET 0x18000

void test_sram(int sram_base_offset, int gpio_indicator) {
    volatile int shifting;
    volatile int data_used;
    int start_address[3] = {0, (RAM_NUM_WORDS*4 /10), (RAM_NUM_WORDS*9 /10)};
    int end_address[3] = {(RAM_NUM_WORDS /10), (RAM_NUM_WORDS*5 /10), RAM_NUM_WORDS};
    
    for (int k = 0; k < 3; k++){
        for (int i = start_address[k]; i < end_address[k]; i++){
            shifting = 0xFFFFFFFF - (0x1 << (i%32));
            data_used = 0x55555555 & shifting;
            USER_writeWord(data_used, sram_base_offset + i);
        }
        for (int i = start_address[k]; i < end_address[k]; i++){
            shifting = 0xFFFFFFFF - (0x1 << (i%32));
            data_used = 0x55555555 & shifting;
            int data = USER_readWord(sram_base_offset + i);
            if (data_used != data) {
                GPIOs_writeHigh(0b01);
                ManagmentGpio_write(1);
                return;
            }
        }
    }
    
    // GPIOs_writeHigh(gpio_indicator);
}

void main(){
    GPIOs_configure(32,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(33,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_loadConfigs();
    User_enableIF(1);
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    GPIOs_writeHigh(0b10);
    
    test_sram(SRAM0_BASE_OFFSET, 0b10);
    
    test_sram(SRAM1_BASE_OFFSET, 0b10);
    
    test_sram(SRAM2_BASE_OFFSET, 0b10);
    
    ManagmentGpio_write(1);
}
