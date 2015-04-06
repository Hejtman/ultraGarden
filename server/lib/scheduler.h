#ifndef SCHEDULER_H
#define SCHEDULER_H


#include <list>
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
		const uint8_t id_start;
		const unsigned duration;
		const uint8_t id_stop;
	};

	bool run;
	std::list<Task> tasks;
	
	void Do(std::list<Scheduler::Task>::iterator task);

public:
	Scheduler();

	void StartLoop();
	void StopLoop();

	std::list<Scheduler::Task>::iterator NextTask();

	void RegisterTask(const unsigned int time, const unsigned int reoccurrence, SchedulerWakeUp* wup, const uint8_t id_start = 0, 
			const unsigned int duration = 0, const uint8_t id_stop = 0);
	void CleanUp();
};


#endif // SCHEDULER_H

