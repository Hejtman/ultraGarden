#ifndef SG90_H
#define SG90_H


#include "pwm.h"

class sg90 : pwmManager
{
    const GPIO_PIN PIN;

public:
    sg90(GPIO_PIN p);
    int SetValue(uint8_t value);
};


#endif // SG90_H
