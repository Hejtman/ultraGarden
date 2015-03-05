#ifndef DHT22_H
#define DHT22_H


#include "gpio.h"

class dht22
{
    const GPIO_PIN PIN;

	uint8_t lastSuccReading;
	float lastSuccHumidity;
	float lastSuccTemprature;

    void InitializeCommunication();
public:
    dht22(GPIO_PIN p);
    int ReadValue(float& humidity, float& temprature, uint8_t& lastSuccess);
};


#endif // DHT22_H

