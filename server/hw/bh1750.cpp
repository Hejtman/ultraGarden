/************************************************************
*   BH1750 Light sensor connected with Raspberry Pi         *
*   Connection:                                             *
*       VCC-3.3v or 5V                                      *
*       GND-GND                                             *
*       SCL-SCL                                             *
*       SDA-SDA                                             *
*       ADD-NC or GND                                       *
************************************************************/
#include <stdio.h>
#include <unistd.h>
#include "bh1750.h"
#include "../log.h"


bh1750::bh1750(const uint8_t address)
 : i2c(),
   ADDRESS(address)
{}

int bh1750::ReadValue(uint16_t& value)
{
    FAIL_LOG_RET( i2c.SetAddress(ADDRESS) );
    FAIL_LOG_RET( i2c.Write(BH1750_POWER_ON) );
    FAIL_LOG_RET( i2c.Write(BH1750_ONE_TIME_LOW_RES_MODE) );

    char buf[2];
    read(i2c.GetFd(), buf, 2);
    value = 256*buf[0] + buf[1];

    return 0;
}

