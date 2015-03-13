#ifndef WATCHDOG_H
#define WATCHDOG_H


#include <stdint.h>

class WatchDog
{

public:
	enum Color {  OK, ALERT  };
		
	Color GetHumidStatus(const uint8_t lastSuccess) const;
};

#endif // WATCHDOG_H

