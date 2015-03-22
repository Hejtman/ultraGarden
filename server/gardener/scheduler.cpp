#include "scheduler.h"
#include <wiringPi.h>
#include <stdlib.h>
#include "../log.h"


SchedulerWakeUp::~SchedulerWakeUp(){}


Scheduler::Scheduler()
: run(true),
  tasks()
{
}


void Scheduler::StartLoop()
{
	LOG_DEBUG("Loop started.");

	// doTask if time is right or sleep to next action (TODO: signal waking up)
	while(run){
		const unsigned int t = millis();

		if ( !tasks.empty() ){
			std::list<Scheduler::Task>::iterator nt = NextTask();
			if (nt->time > t)
				delay(nt->time - t);
			else
				Do(nt);
		} else {
			LOG_ERROR("Empty scheduler queue!  Sleeping 0.1s");
			delay(100);
		}
	}
}


void Scheduler::StopLoop()
{
	run = false;

	LOG_DEBUG("Loop stopped.");
}


std::list<Scheduler::Task>::iterator Scheduler::NextTask()
{
	std::list<Task>::iterator it = tasks.begin();
	std::list<Task>::iterator next = tasks.begin();
	
	for(++it; it != tasks.end(); ++it) {
	   	//FIXME after 49days uint wraps and this will always return one task
		if (next->time  >  it->time)
			next = it;
	}

	return next;
}


void Scheduler::RegisterTask(const unsigned int time, const unsigned int reoccurrence, SchedulerWakeUp* wup, const uint8_t id_start, const unsigned int duration, const uint8_t id_stop)
{
	tasks.push_back( Task{time, reoccurrence, wup, id_start, duration, id_stop} );
}

void Scheduler::CleanUp()
{
	tasks.clear();
}

void Scheduler::Do(std::list<Scheduler::Task>::iterator task)
{
	LOG_DEBUG("Task %d started", task->id_start);
	const unsigned int t = millis();

	// fire start task and prepare stop task or next re-occurrence if necessary
	task->wup->SchedulerWakeUpCall(task->id_start);

	if (task->duration)
		tasks.push_back( Task{t + task->duration, 0, task->wup, task->id_stop, 0, 0} );

	if (task->reoccurrence) {

		// ignore missed occurrences
		// uint wrapps after 49days
		do
			task->time += task->reoccurrence;
		while(t > task->time && task->time > task->reoccurrence);
	} else {
		tasks.erase(task);
	}
}

