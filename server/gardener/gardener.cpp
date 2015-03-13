#include "gardener.h"
#include <wiringPi.h>


Gardener::Gardener() 
: garden(),
  scheduler(),
  mode(MANUAL)
{
}

int8_t Gardener::StartLoop(Mode m)
{
//	enum TaskId{  CHECK_COMMAND_FILE, CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, REFLECT_LIGHT, PUMPING_CYCLE  };
	switch (mode = m) {
		case AUTO:
//			scheduler.RegisterTask(15*60*1000,		15*60*1000,		&garden, Garden::REFLECT_LIGHT);//gardner?
//			scheduler.RegisterTask(2*60*60*1000,	2*60*60*1000,	&garden, Garden::PUMPING_CYCLE);//gardner?

		case SAFE:
			scheduler.RegisterTask(5*60*1000,		5*60*1000,		&garden, Garden::SWITCH_DUTTY_CYCLE);

		case MANUAL:
		case EMERGENCY:
//			scheduler.RegisterTask(0,				1*1000,			&remote, Remote::CHECK_COMMAND_FILE);
			scheduler.RegisterTask(0, 				10*1000,		&garden, Garden::CHECK_SENSORS);
//			scheduler.RegisterTask(1*60*1000,		1*60*1000,		&reporter, Reporter::SEND_STATUS_FILE);
	}

	// TODO: set all tidegates and all rellys closed by default

	scheduler.StartLoop();

	return 0;
}

