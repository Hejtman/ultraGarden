#ifndef AI_H
#define AI_H


#include "status.h"
#include "scheduler.h"

class AI : public Status
{
//	enum Mode{  MANUAL, AUTO, SAFE  } mode;

	Scheduler scheduler;

public:
	AI();
	int8_t StartLoop();
};


#endif // AI_H

