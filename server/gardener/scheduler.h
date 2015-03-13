#ifndef SCHEDULER_H
#define SCHEDULER_H


#include <vector>
#include <stdint.h>

class SchedulerWakeUp
{
public:
	virtual void SchedulerWakeUpCall(const uint8_t id) = 0;
	virtual ~SchedulerWakeUp() = 0;
};

class Scheduler
{
	struct Task{
		unsigned int time;
		const unsigned int reoccurrence;
		SchedulerWakeUp* wup;
		const uint8_t id;
		
		void doTask();
	};

	bool run;
	std::vector<Task> tasks;

public:
	Scheduler();

	void StartLoop();
	void StopLoop();

	Task* NextTask();

	void RegisterTask(const unsigned int time, const unsigned int reoccurrence, SchedulerWakeUp* wup, const uint8_t id = 0);
};


#endif // SCHEDULER_H

