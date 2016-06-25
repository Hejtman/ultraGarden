#ifndef DHT11_H
#define DHT11_H


#include "gpio.h"

class dht11
{
    const GPIO_PIN PIN;
    const uint8_t MAXERRORS;

    void InitializeCommunication();
public:
    dht11(GPIO_PIN p, uint8_t e);
    int ReadValue(uint8_t& humidity, uint8_t& temprature, uint8_t& errors);
};


#endif // DHT11_H

