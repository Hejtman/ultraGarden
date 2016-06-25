#ifndef GARDENER_H
#define GARDENER_H


#include "remote.h"
#include "garden.h"
#include "../lib/scheduler.h"

class Gardener
{
	Garden		garden;
	Remote		remote;
	Scheduler	scheduler;

public:
	enum Mode{  MANUAL, AUTO, SAFE, EMERGENCY  } mode;

	Gardener();
	int8_t StartLoop(Mode m);
	void StopLoop(){  scheduler.StopLoop();  }
};


#endif // GARDENER_H

