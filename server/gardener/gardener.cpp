#include "gardener.h"
#include <wiringPi.h>
#include <stdlib.h>//
#include <stdio.h>//
#include <unistd.h>//
#include <sys/ioctl.h>//


enum taskId{CHECK_COMMAND_FILE, CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, REFLECT_LIGHT, PUMPING_CYCLE};
void f()
{
	printf("%u f\n", micros());///////
}
extern void SendStatusFile();


Gardener::Gardener() 
: Status(),
  scheduler()
{

}

int8_t Gardener::StartLoop(/*mode*/)
{
	// if / switch mode
	scheduler.RegisterTask(CHECK_COMMAND_FILE,	0,				1*1000,			&f);
	scheduler.RegisterTask(CHECK_SENSORS, 		0, 				10*1000,		&f);
	scheduler.RegisterTask(SEND_STATUS_FILE, 	1*60*1000,		1*60*1000,		&SendStatusFile);
	scheduler.RegisterTask(SWITCH_DUTTY_CYCLE,	5*60*1000,		5*60*1000,		&f);
	scheduler.RegisterTask(REFLECT_LIGHT, 		15*60*1000,		15*60*1000,		&f);
	scheduler.RegisterTask(PUMPING_CYCLE, 		2*60*60*1000,	2*60*60*1000,	&f);

	scheduler.StartLoop();

	return 0;
}

