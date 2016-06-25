#ifndef SERVO_H
#define SERVO_H


#include "pwm.h"
#include <stdint.h>

class servo : pwmManager
{
    const GPIO_PIN PIN;

public:
    servo(GPIO_PIN p);
    int SetValue(uint8_t value);
};


#endif // SERVO_H
