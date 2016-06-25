#include "pwm.h"
#include <wiringPi.h>


bool pwmManager::initialized = false;
std::list<GPIO_PIN> pwmManager::initialize;

pwmManager::pwmManager(GPIO_PIN p)
{
	initialize.push_back(p);
}

void pwmManager::Initialize()
{
	for (std::list<GPIO_PIN>::iterator it = initialize.begin(); it != initialize.end(); ++it)
		pinMode(*it, PWM_OUTPUT);

	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(384); 			// 19200000/384/1024 = clock at 49kHz (21us tick)
	pwmSetRange(1024); 			// range at 1024 ticks (21ms)
	initialized = true;
}

