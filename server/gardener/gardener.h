#ifndef GARDENER_H
#define GARDENER_H


#include "remote.h"
#include "garden.h"
#include "scheduler.h"

class Gardener : public SchedulerWakeUp
{
	Garden		garden;
	Remote		remote;
	Scheduler	scheduler;

	enum {  CHECK_COMMAND_FILE  };

	void CheckCommandFile();
	void SchedulerWakeUpCall(const uint8_t id);

public:
	enum Mode{  MANUAL, AUTO, SAFE, EMERGENCY  } mode;

	Gardener();
	int8_t StartLoop(Mode m);
};


#endif // GARDENER_H

