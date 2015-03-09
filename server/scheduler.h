#ifndef SCHEDULER_H
#define SCHEDULER_H


#include <vector>
#include <stdint.h>

class Scheduler
{
	struct Task{
		const unsigned int id;
		unsigned int time;
		const unsigned int reoccurrence;
		void (*f)();
		
		void doTask();
	};

	bool run;
	std::vector<Task> tasks;

public:
	Scheduler();

	void StartLoop();
	void StopLoop();

	Task* NextTask();

	void RegisterTask(const unsigned int id, const unsigned int time, const unsigned int reoccurrence, void (*f)());
};


#endif // SCHEDULER_H

