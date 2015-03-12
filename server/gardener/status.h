#ifndef STATUS_H
#define STATUS_H


#include "../hw/bh1750.h"
#include "../hw/dht22.h"
#include "../hw/relay.h"
#include "../hw/tidegate.h"

class Status
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
//	sensors
	Status();	
};


#endif // STATUS_H

