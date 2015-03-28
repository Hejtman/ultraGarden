#ifndef STATUS_H
#define STATUS_H


#include "../hw/bh1750.h"
#include "../hw/dht22.h"
#include "../hw/hcsr04.h"
#include "../hw/relay.h"
#include "../hw/tidegate.h"
#include "../lib/lib.h"
#include "scheduler.h"
#include "watchdog.h"

class Garden : public SchedulerWakeUp
{
	WatchDog		watchDog;
	enum DutyCycle { FOGGING, IDLING, AIRING  } dutyCycle;
  	unsigned int	dutyCycleTiming[3];
	const char		dutyCycleNames[3][10];
	unsigned int	dutyStartTime;

	relay			barrelFogRelay;
	relay			barrelFunRelay;
	TideGate		barrelTideGate;
	dht22			barrelHumidSensor;
	WatchDog::Color	barrelHumidSensorStatus;
	HcSr04			barrelWatterLevel;

	relay			pumpRelay;
	TideGate		pumpTideGate;
	dht22   		pumpHumidSensor;
	WatchDog::Color	pumpHumidSensorStatus;

	dht22			outerHumidSensor;
	WatchDog::Color	outerHumidSensorStatus;
	bh1750			outerLightSensor;
	WatchDog::Color	outerLightSensorStatus;

	CpuMonitor		cpuMonitor;

	void CheckSensors();
	void SendStatusFile();
	void SwitchDutyCycle();
	void StartFogging();
	void StartIdling();
	void StartAiring();
	void StartPumpingCycle();
	void StopPumpingCycle();

public:
	const unsigned int checkSensorOccurrence;
	const unsigned int sendStatusFileOccurrence;
	const unsigned int switchDutyCycleOccurrence;
	const unsigned int pumpingCycleOccurrence;
	const unsigned int pumpingCycleDuration;

	Garden();

	enum {  CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, PUMPING_CYCLE_START, PUMPING_CYCLE_STOP  };
	void SchedulerWakeUpCall(const uint8_t id);
};


#endif // STATUS_H

