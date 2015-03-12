#ifndef GARDENER_H
#define GARDENER_H


#include "status.h"
#include "scheduler.h"

class Gardener : public Status
{
//	enum Mode{  MANUAL, AUTO, SAFE  } mode;

	Scheduler scheduler;

public:
	Gardener();
	int8_t StartLoop();
};


#endif // GARDENER_H

