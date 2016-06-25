#ifndef TIDEGATE_H
#define TIDEGATE_H


#include "servo.h"

class TideGate : servo
{
	const uint8_t OPEN;
	const uint8_t CLOSED;
	uint8_t state;

public:
	TideGate(GPIO_PIN p, uint8_t open, uint8_t closed);

	void Open();
	void Close();
	bool IsOpen(){  return state == OPEN;  }
};

#endif // TIDEGATE_H

