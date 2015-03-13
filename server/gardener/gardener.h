#ifndef GARDENER_H
#define GARDENER_H


#include "garden.h"
#include "scheduler.h"

class Gardener : public Garden
{
public:
	enum Mode{  MANUAL, AUTO, SAFE, EMERGENCY  };
	enum TaskId{  CHECK_COMMAND_FILE, CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, REFLECT_LIGHT, PUMPING_CYCLE  };

private:
	Scheduler	scheduler;
	Mode		mode;

public:

	Gardener();
	int8_t StartLoop(Mode m);
};


#endif // GARDENER_H

