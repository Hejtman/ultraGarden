#ifndef REMOTE_H
#define REMOTE_H


#include <stdint.h>
#include "../lib/scheduler.h"

class Gardener;
class Remote : public SchedulerWakeUp
{
	Gardener& gardener;

public:
	Remote(Gardener& g);

	const int checkCommandFileOccurrence;
	enum {  CHECK_COMMAND_FILE  };
	void SchedulerWakeUpCall(const uint8_t id);
	void CheckCommandFile();
};

#endif // REMOTE_H

