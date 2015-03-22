#include "gardener/gardener.h"
#include <wiringPi.h>
#include "extlib/c-log/src/log.h"

int main(int, char **)
{
	log_init(LL_DEBUG, "ultra_gardend", "tmp/log");
	if ( wiringPiSetup() == -1 )
    	return 1;

	LOG_NOTICE("Server started.");
	piHiPri(99); // less interruptions during reading from devices (e.g. dht22)

	Gardener gardener;
	if ( gardener.StartLoop(Gardener::AUTO) != 0 ) {

		LOG_ERROR("AUTO mode failed!  SAFE mode started!");
		if ( gardener.StartLoop(Gardener::SAFE) != 0 ) {

			LOG_ERROR("SAFE mode failed!  EMERGENCY SHUT-DOWN activated!");
			if ( gardener.StartLoop(Gardener::EMERGENCY) != 0 ) {

				LOG_ERROR("EMERGENCY SHUT-DOWN mode failed!  You are doomed! DOOMED!");
				return 1;
			}
		}
	}

	LOG_NOTICE("Server finished.");
	return 0;
}

