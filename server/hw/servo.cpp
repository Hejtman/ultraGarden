#include <wiringPi.h>
#include "servo.h"


servo::servo(GPIO_PIN p)
: pwmManager(p), 
  PIN(p)
{
}

int servo::SetValue(uint8_t value)
{
	// initialize all pwm outputs when first use of any
	if(!Initialized())
		Initialize();

	pwmWrite(PIN, value);

	return 0;
}

