#ifndef HCSR04_H
#define HCSR04_H


#include "gpio.h"

class HcSr04
{
    const GPIO_PIN PIN_TRIG, PIN_ECHO;

	unsigned int value;
	unsigned int lastSuccReading;
	const unsigned int MIN_RANGE;
	const unsigned int MAX_RANGE;

    void InitializeCommunication();

public:
    HcSr04(GPIO_PIN t, GPIO_PIN e);
	int ReadValue();
    int ReadValue(unsigned int& value);

	unsigned int GetValue()const{  return value;  }
	unsigned int GetLastSuccess()const{  return lastSuccReading;  }
};


#endif // HCSR04_H

