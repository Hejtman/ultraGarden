#include "watchdog.h"


const uint8_t HUMID_ALERT_LEVEL = 11;

WatchDog::Color WatchDog::GetHumidStatus(const uint8_t lastSuccess) const
{
	if (lastSuccess < HUMID_ALERT_LEVEL)
		return OK;

	return ALERT;
}

