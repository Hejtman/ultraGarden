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
	int ReadValues();
    int ReadValues(float& humidity, float& temprature, uint8_t& lastSuccess);

	void GetValues(float& humidity, float& temprature, uint8_t& lastSuccess) const;
	float GetHumidity()const{  return  lastSuccHumidity;  }
	float GetTemperature()const{  return lastSuccTemprature;  }
	uint8_t GetLastSuccess()const{  return lastSuccReading;  }
};


#endif // DHT22_H

