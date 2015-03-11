#include "log.h"
#include "ai/ai.h"
#include <wiringPi.h>


int main(int, char **)
{
	if ( wiringPiSetup() == -1 )
    	return 1;

	piHiPri(99); // might have better performance for reading from dht22?

	AI ai();

//	ai.StartLoop(/*mode*/); // if fail re-start with failure mode?

	return 0;
}

