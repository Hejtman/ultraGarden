#ifndef I2C_H
#define I2C_H


#include <stdint.h>
#include "i2c-dev.h"

// Responsible for Initialization I2C bus when first time in use
// and Uninitialization last device removed.
class I2CManager
{
    static int fd;
    static int devices;

    static int Initialize();
    static int Uninitialize();

public:
    virtual ~I2CManager(){};

    static void AddDevice();
    static void RemoveDevice();

    static int GetFd();
};


// Responsible for I2C bus comunication
class I2C : public I2CManager
{
static uint8_t currentAddress;

I2C(const I2C&);

public:
    I2C(){  AddDevice();  };
    ~I2C(){  RemoveDevice();  };

    int SetAddress(const uint8_t address);
    int Write(const uint8_t value);
};


#endif // I2C_H

