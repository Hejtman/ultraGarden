#ifndef STATUS_H
#define STATUS_H


#include "../hw/bh1750.h"
#include "../hw/dht22.h"
#include "../hw/relay.h"
#include "../hw/tidegate.h"
#include "scheduler.h"
#include "watchdog.h"

class Garden : public SchedulerWakeUp
{
	WatchDog		watchDog;
// state:       // Fogging, Airing, Idling
	relay			barrelFogRelay;
	relay			barrelFunRelay;
	TideGate		barrelTideGate;
	dht22			barrelHumidSensor;
	WatchDog::Color	barrelHumidSensorStatus;

	relay			pumpRelay;
	TideGate		pumpTideGate;
	dht22   		pumpHumidSensor;
	WatchDog::Color	pumpHumidSensorStatus;

	dht22			outerHumidSensor;
	WatchDog::Color	outerHumidSensorStatus;
	bh1750			outerLightSensor;
	WatchDog::Color	outerLightSensorStatus;

	void CheckSensors();
	void SendStatusFile();
	void SwitchDutyCycle();

public:
	const unsigned int checkSensorOccurrence;
	const unsigned int sendStatusFileOccurrence;
	const unsigned int switchDutyCycleOccurrence;

	Garden();

	enum {  CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE  };
	void SchedulerWakeUpCall(const uint8_t id);
};


#endif // STATUS_H

