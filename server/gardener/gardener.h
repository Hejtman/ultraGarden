#ifndef GARDENER_H
#define GARDENER_H


#include "garden.h"
#include "scheduler.h"

class Gardener
{
	Garden garden;

public:
	enum Mode{  MANUAL, AUTO, SAFE, EMERGENCY  };

private:
	Scheduler	scheduler;
	Mode		mode;

public:

	Gardener();
	int8_t StartLoop(Mode m);
};


#endif // GARDENER_H

