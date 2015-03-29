#ifndef REMOTE_H
#define REMOTE_H


#include <stdint.h>

class Remote
{

public:
	Remote();

	enum {  CHECK_COMMAND_FILE  };
	void SchedulerWakeUpCall(const uint8_t id);
};

#endif // REMOTE_H

