#include "gardener.h"
#include <wiringPi.h>
#include <stdio.h> //micros


void ff()
{
	printf("%u f\n", micros());///////
}
extern void SendStatusFile();


Gardener::Gardener() 
: Garden(),
  scheduler(),
  mode(MANUAL)
{
}

int8_t Gardener::StartLoop(Mode m)
{
	switch (mode = m) {
		case AUTO:
			scheduler.RegisterTask(REFLECT_LIGHT, 		15*60*1000,		15*60*1000,		&ff);
			scheduler.RegisterTask(PUMPING_CYCLE, 		2*60*60*1000,	2*60*60*1000,	&ff);

		case SAFE:
			scheduler.RegisterTask(SWITCH_DUTTY_CYCLE,	5*60*1000,		5*60*1000,		&ff);

		case MANUAL:
		case EMERGENCY:
			scheduler.RegisterTask(CHECK_COMMAND_FILE,	0,				1*1000,			&ff);
//			scheduler.RegisterTask(CHECK_SENSORS, 		0, 				10*1000,		&CheckSensors);
			scheduler.RegisterTask2(this);
			scheduler.RegisterTask(SEND_STATUS_FILE, 	1*60*1000,		1*60*1000,		&SendStatusFile);
	}

	// TODO: set all tidegates and all rellys closed by default

	scheduler.StartLoop();

	return 0;
}

