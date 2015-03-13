#ifndef STATUS_H
#define STATUS_H


#include "../hw/bh1750.h"
#include "../hw/dht22.h"
#include "../hw/relay.h"
#include "../hw/tidegate.h"
#include "scheduler.h"

class Garden : public SchedulerWakeUp
{
// state:       // Fogging, Airing, Idling

	relay		barrelFogRelay;
	relay		barrelFunRelay;
	TideGate	barrelTideGate;
	dht22		barrelHumidSensor;

	relay		pumpRelay;
	TideGate	pumpTideGate;
	dht22   	pumpHumidSensor;

	dht22		outerHumidSensor;
	bh1750		outerLightSensor;

public:
	Garden();

	enum {  CHECK_SENSORS, SWITCH_DUTTY_CYCLE  };
	void SchedulerWakeUpCall(const uint8_t id);

	void CheckSensors();
	void SwitchDutyCycle();
};


#endif // STATUS_H

