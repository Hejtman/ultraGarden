#ifndef RELAY_H
#define RELAY_H


#include "gpio.h"
#include <stdint.h>

class Relay
{
    const GPIO_PIN PIN;

public:
    Relay(GPIO_PIN p);

    void TurnOn();
    void TurnOff();
};


#endif // RELAY_H
