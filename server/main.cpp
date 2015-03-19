#include "log.h"
#include "gardener/gardener.h"
#include <wiringPi.h>
#include "extlib/c-log/src/log.h"

int main(int, char **)
{
	if ( wiringPiSetup() == -1 )
    	return 1;

	log_init(LL_DEBUG, "ultra_gardend", "tmp/log");
	LOG_NOTICE("Server started.");

	piHiPri(99); // might have better performance for reading from dht22?

	Gardener gardener;
	if ( gardener.StartLoop(Gardener::AUTO) != 0 ) {

		// TODO log: gardner AUTO mode failed!  SAFE mode started!
		if ( gardener.StartLoop(Gardener::SAFE) != 0 ) {

			// TODO log: gardener SAFE mode failed!  EMERGENCY SHUT-DOWN activated
			if ( gardener.StartLoop(Gardener::EMERGENCY) != 0 ) {

				// TODO log: gardener EMERGENCY SHUT-DOWN mode failed!  You are doomed! DOOMED!
				return 1;
			}
		}
	}

	LOG_NOTICE("Server ended.");
	return 0;
}

