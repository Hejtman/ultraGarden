#ifndef BH1750_H
#define BH1750_H


#include "i2c.h"

class bh1750
{
I2C i2c;
const uint8_t ADDRESS;

enum {
    BH1750_POWER_DOWN                 = 0x00,   // No active state
    BH1750_POWER_ON                   = 0x01,   // Wating for measurment command
    BH1750_CONTINUOUS_HIGH_RES_MODE   = 0x10,   // Start measurement at 1lx resolution. Measurement time is approx 120ms.
    BH1750_CONTINUOUS_HIGH_RES_MODE_2 = 0x11,   // Start measurement at 0.5lx resolution. Measurement time is approx 120ms.
    BH1750_CONTINUOUS_LOW_RES_MODE    = 0x13,   // Start measurement at 4lx resolution. Measurement time is approx 16ms.

    // Device is automatically set to Power Down after measurement.
    BH1750_ONE_TIME_HIGH_RES_MODE_2   = 0X21,   // Start measurement at 0.5lx resolution. Measurement time is approx 120ms.
    BH1750_ONE_TIME_LOW_RES_MODE      = 0x23    // Start measurement at 1lx resolution. Measurement time is approx 120ms.
};

public:
    bh1750(const uint8_t address);

    int ReadValue(uint16_t& value);
};


#endif // BH1750_H
