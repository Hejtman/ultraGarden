#ifndef PWM_H
#define PWM_H


#include "gpio.h"
#include <list>

class pwmManager
{
	static std::list<GPIO_PIN> initialize;
	static bool initialized;

public:
	pwmManager(GPIO_PIN p);

	bool Initialized(){   return initialized;   }
	void Initialize();
};


#endif // PWM_H
