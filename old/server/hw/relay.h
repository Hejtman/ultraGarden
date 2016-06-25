#ifndef RELAY_H
#define RELAY_H


#include "gpio.h"
#include <stdint.h>

class relay
{
    const GPIO_PIN PIN;

public:
    relay(GPIO_PIN p);

    void TurnOn();
    void TurnOff();
};


#endif // RELAY_H
