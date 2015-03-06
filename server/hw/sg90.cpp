#include <wiringPi.h>
#include <stdint.h>
#include "sg90.h"


sg90::sg90(GPIO_PIN p)
: pwmManager(p), 
  PIN(p)
{
}

int sg90::SetValue(uint8_t value)
{
	// initialize all pwm outputs when first use of any
	if(!Initialized())
		Initialize();

	pwmWrite(PIN, value);

	return 0;
}

