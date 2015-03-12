#include "log.h"
#include "gardener/gardener.h"
#include <wiringPi.h>


int main(int, char **)
{
	if ( wiringPiSetup() == -1 )
    	return 1;

	piHiPri(99); // might have better performance for reading from dht22?

	Gardener gardener;
	if ( gardener.StartLoop(Gardener::AUTO) != 0 ) {

		// log: gardner AUTO mode failed!  SAFE mode started!
		if ( gardener.StartLoop(Gardener::SAFE) != 0 ) {

			// log: gardener SAFE mode failed!  EMERGENCY SHUT-DOWN activated
			if ( gardener.StartLoop(Gardener::EMERGENCY) != 0 ) {

				// log: gardener EMERGENCY SHUT-DOWN mode failed!  You are doomed! DOOMED!
				return 1;
			}
		}
	}

	return 0;
}

