#include "relay.h"
#include <wiringPi.h>


Relay::Relay(GPIO_PIN p)
: PIN(p) 
{}

void Relay::TurnOn()
{
	pinMode(PIN, OUTPUT);
	digitalWrite(PIN, HIGH);
}

void Relay::TurnOff()
{
	digitalWrite(PIN, LOW);
}

