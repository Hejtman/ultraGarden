#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "hcsr04.h"


HcSr04::HcSr04(GPIO_PIN t, GPIO_PIN e)
: PIN_TRIG(t),
  PIN_ECHO(e),
  value(0),
  lastSuccReading(0xFFFFFFFF),
  MIN_RANGE(2*58),	// 2cm
  MAX_RANGE(450*58)	// 450cm
{
}

void HcSr04::InitializeCommunication()
{
	pinMode( PIN_TRIG, OUTPUT );
	pinMode( PIN_ECHO, INPUT );
	pullUpDnControl( PIN_ECHO, PUD_DOWN );

	digitalWrite( PIN_TRIG, LOW );
 	delayMicroseconds(2);
	digitalWrite( PIN_TRIG, HIGH );
 	delayMicroseconds(12);
	digitalWrite( PIN_TRIG, LOW );
}

int HcSr04::ReadValue()
{
	InitializeCommunication();

	// wait for hcrs04 to start communication
	for (unsigned int i = 0  ;  digitalRead(PIN_ECHO) == LOW  &&  i < MAX_RANGE  ;  ++i) {
 		delayMicroseconds(1);
	}

	// 58us for each cm, calculate in millimeters
	unsigned int startTime = micros();
	for (unsigned int i = 0  ;  digitalRead(PIN_ECHO) == HIGH  &&  i < MAX_RANGE  ;  ++i) {
 		delayMicroseconds(1);
	}
	value = (micros() - startTime) / 5.8;

	return (value > MIN_RANGE/10 && value < MAX_RANGE/10) ?  0 : 1;
}

int HcSr04::ReadValue(unsigned int& v)
{
	int rv = ReadValue();
	v = GetValue();
	return rv;
}

