#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include "i2c.h"
#include "../log.h"


int I2CManager::Initialize()
{
    // Open port for reading and writing
    if ((fd = open("/dev/i2c-1", O_RDWR)) < 0) {
        return -1;
    }

    return 0;
}

int I2CManager::Uninitialize()
{
    if (fd != 0)
        return close(fd);

    return 0;
}

void I2CManager::AddDevice()
{
    ++devices;
}

void I2CManager::RemoveDevice()
{
    if (--devices == 0)
        Uninitialize();
}

int I2CManager::GetFd()
{
    if (fd <= 0) {
        Initialize();
    }

    return fd;
}

int I2C::SetAddress(const uint8_t address)
{
    if (currentAddress == address)
        return 0;

    FAIL_LOG_RET( ioctl(GetFd(), I2C_SLAVE, address) );
    currentAddress = address;
    return 0;
}

int I2C::Write(const uint8_t value)
{
    FAIL_LOG_RET( i2c_smbus_write_byte(GetFd(), value) );
    return 0;
}


int I2CManager::fd = 0;
int I2CManager::devices = 0;
uint8_t I2C::currentAddress = 0;


