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
	scheduler.CleanUp();

//	enum TaskId{  CHECK_COMMAND_FILE, CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, REFLECT_LIGHT, PUMPING_CYCLE  };
	switch (mode = m) {
		case AUTO:
//			scheduler.RegisterTask(15*60*1000,		15*60*1000,		&garden, Garden::REFLECT_LIGHT);//gardner?
			scheduler.RegisterTask(garden.pumpingCycleOccurrence,	garden.pumpingCycleOccurrence,	&garden, Garden::PUMPING_CYCLE_START, 
					garden.pumpingCycleDuration, Garden::PUMPING_CYCLE_STOP);

		case SAFE:
			scheduler.RegisterTask(2,	garden.switchDutyCycleOccurrence,	&garden, Garden::SWITCH_DUTTY_CYCLE);

		case MANUAL:
		case EMERGENCY:
//			scheduler.RegisterTask(0,				1*1000,			&remote, Remote::CHECK_COMMAND_FILE);
			scheduler.RegisterTask(0, 	garden.checkSensorOccurrence,		&garden, Garden::CHECK_SENSORS);
			scheduler.RegisterTask(1,	garden.sendStatusFileOccurrence,	&garden, Garden::SEND_STATUS_FILE);
	}

	// TODO: set all tidegates and all rellys closed by default

	scheduler.StartLoop();

	return 0;
}

