#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "dht22.h"

const uint8_t HALFWAVES = 85;
const uint8_t MAXZEROLENGTH = 16;


dht22::dht22(GPIO_PIN p)
: PIN(p),
  lastSuccReading(0),
  lastSuccHumidity(0),
  lastSuccTemprature(0)
{
}

void dht22::InitializeCommunication()
{
    pinMode( PIN, OUTPUT );
    digitalWrite( PIN, LOW );
    delay( 18 );
    digitalWrite( PIN, HIGH );
    delayMicroseconds( 40 );
    pinMode( PIN, INPUT );
	pullUpDnControl( PIN, PUD_UP );
}

int dht22::ReadValue(float& humidity, float& temprature, uint8_t& lastSuccess)
{
	InitializeCommunication();

	uint8_t bit = 0;
	uint8_t byte = 0;
	uint8_t laststate = HIGH;
	uint8_t data[5] = {0,0,0,0,0};

	for(uint8_t i = 0 ; i < HALFWAVES ; ++i) {
		uint8_t signaLength = 0;
		while (digitalRead(PIN) == laststate && ++signaLength != 255) {
			delayMicroseconds( 1 );
		}
		laststate = digitalRead( PIN );

		// ignore first 2 waves and measure only HIGH part of waves as that means ONE or ZERO
		if ((i >= 4) && (laststate == LOW)) {
			data[byte] <<= 1;
			if (signaLength > MAXZEROLENGTH)
				data[byte] |= 1;
			byte = ++bit/8;
			delayMicroseconds( 10 );
		}
	}

	// calculate values, checksum
	if ( (bit >= 39) && (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)) ) {
		lastSuccHumidity = humidity = float(256 * data[0] + data[1]) / 10;
		lastSuccTemprature = temprature = float(256 * (data[2] & 0x7F) + data[3]) / 10;
		if (data[2] & 0x80)
			lastSuccTemprature = temprature *= -1;

		lastSuccess = lastSuccReading = 0;
		return 0;
	} else {
		// reading failed, return latest good values
		humidity = lastSuccHumidity;
		temprature = lastSuccTemprature;
		lastSuccess = ++lastSuccReading;
		return 1;
	}
}

