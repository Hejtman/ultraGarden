#include "scheduler.h"
#include <wiringPi.h>
#include <stdlib.h>


SchedulerWakeUp::~SchedulerWakeUp(){}


Scheduler::Scheduler()
: run(true),
  tasks()
{
}


void Scheduler::StartLoop()
{
	// doTask if time is right or sleep to next action (TODO: signal waking up)
	while(run){
		const unsigned int t = millis();

		Task* nt = NextTask();
		if (nt){
			if (nt->time > t)
				delay(nt->time - t);
			else
				nt->doTask();
		} else {
			// TODO: log empty scheduler
			delay(100);
		}
	}
}


void Scheduler::StopLoop()
{
	run = false;
}


Scheduler::Task* Scheduler::NextTask()
{
	if (tasks.empty())
		return NULL;

	std::vector<Task>::iterator it = tasks.begin();
	Task* next = &(*it);
	
	for(++it; it != tasks.end(); ++it) {
	   	//FIXME after 49days uint wraps and this will always return one task
		if (next->time > it->time)
			next = &(*it);
	}

	return next;
}


void Scheduler::RegisterTask(const unsigned int time, const unsigned int reoccurrence, SchedulerWakeUp* wup, const uint8_t id)
{
	tasks.push_back( Task{time, reoccurrence, wup, id} );
}

void Scheduler::Task::doTask()
{
	// fire task and prepare next re-occurrence
	wup->SchedulerWakeUpCall(id);

	if (reoccurrence) {
		const unsigned int t = millis();

		// ignore missed occurrences
		// uint wrapps after 49days
		do
			time += reoccurrence;
		while(t > time && time > reoccurrence);
	} else {
		// TODO: remove this task from vector
		// TODO: vector > list
	}
}

