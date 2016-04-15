#include "gardener/gardener.h"
#include <wiringPi.h>
#include "extlib/c-log/src/log.h"

const GPIO_PIN FOG_RELE = GPIO_29;
const GPIO_PIN FUN_RELE = GPIO_26;



int main(int, char **)
{
	log_init(LL_DEBUG, "ultra_gardend", "tmp/log");
	if ( wiringPiSetup() == -1 )
    	return 1;

	LOG_NOTICE("Server started.");
	piHiPri(99); // less interruptions during reading from devices (e.g. dht22)

	// handle exceptions here
//	Gardener gardener;
while(1){
	Relay relay1((GPIO_PIN)29);
	relay1.TurnOn();
	usleep(1000000);
	relay1.TurnOff();
	usleep(1000000);
}


	// FIXME: for loop here
/*	if (gardener.StartLoop(Gardener::AUTO)) 
	{
		LOG_ERROR("AUTO mode failed!  SAFE mode started!");
		if (gardener.StartLoop(Gardener::SAFE))
		{
			LOG_ERROR("SAFE mode failed!  EMERGENCY SHUT-DOWN activated!");
			if (gardener.StartLoop(Gardener::EMERGENCY)) 
			{
				LOG_ERROR("EMERGENCY mode failed!");
				return 1;
			}
		}
	}
*/
	LOG_NOTICE("Server finished.");
	return 0;
}

