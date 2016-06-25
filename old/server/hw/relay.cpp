#include "relay.h"
#include <wiringPi.h>


relay::relay(GPIO_PIN p)
: PIN(p) 
{}

void relay::TurnOn()
{
    pinMode( PIN, OUTPUT );
}

void relay::TurnOff()
{
    pinMode( PIN, INPUT );
}

