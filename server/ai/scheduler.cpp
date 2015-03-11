#include "scheduler.h"
#include <wiringPi.h>


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

		if (nt->time > t)
			delayMicroseconds(nt->time - t);
		else
			nt->doTask();
	}
}


void Scheduler::StopLoop()
{
	run = false;
}


Scheduler::Task* Scheduler::NextTask()
{
	std::vector<Task>::iterator it = tasks.begin();
	Task* next = &(*it);
	
	for(++it; it != tasks.end(); ++it) {
	   	//FIXME after 49days uint wraps and this will always return one task
		if (next->time > it->time)
			next = &(*it);
	}

	return next;
}


void Scheduler::RegisterTask(const unsigned int id, const unsigned int time, const unsigned int reoccurrence, void (*f)())
{
	tasks.push_back( Task{id, time, reoccurrence, f} );
}


void Scheduler::Task::doTask()
{
	// fire task and prepare next re-occurrence
	f();

	const unsigned int t = millis();

	// ignore missed occurrences
	// uint wrapps after 49days
	do
		time += reoccurrence;
	while(t > time && time > reoccurrence);
}

