#include "log.h"
#include "hw/bh1750.h"
#include "hw/dht22.h"
#include "hw/dht11.h"
#include "hw/relay.h"
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>


const uint8_t BH1750FVI_I2C_ADDRESS = 0x23;  // sudo i2cdetect -y 1
const uint8_t IGNORE_FAILED_READINGS = 10;

int main(int, char **)
{
    // GPIO wiering -----------------------------
//    relay  fogRelay(GPIO_0);
//    relay  pumpRelay(GPIO_1);
//    dht11  tankHumidSensor(GPIO_2, MAXERRORS);
//    dht11   pumpHumidSensor(GPIO_5, IGNORE_FAILED_READINGS);
//    dht11   outerHumidSensor(GPIO_5, IGNORE_FAILED_READINGS);
	dht22	outerHumidSensor(GPIO_5);

//    bh1750 lightSensor1(BH1750FVI_I2C_ADDRESS);
    //-------------------------------------------

	if ( wiringPiSetup() == -1 )
    	return 1;

    ////////// state, while(1){   sleep;    change(state);}
    ////////// switch (state){  write_sensore values to web;  }
    // gitHub
    // servo
//////////////////////////////////

//pinMode(1, PWM_OUTPUT);/////////// Initialize?
//pwmSetMode(PWM_MODE_MS);////////// manager?
//pwmSetClock(384); //clock at 50kHz (20us tick)
//pwmSetRange(1000); //range at 1000 ticks (20ms)

/*pwmWrite(1, 90);////////////////// SetPosition(int number);
sleep(1);
pwmWrite(1, 180); 
sleep(1);
pwmWrite(1, 45); 
sleep(1);*/
//////////////////////////////////

/*
        while(1)
        {
        fogRelay.TurnOn();
        sleep(1);
        fogRelay.TurnOff();
        sleep(1);
        }

*/
    for(int i=0 ; i<100 ; ++i) {
//        uint16_t value = 0;
//        lightSensor1.ReadValue(value);
//        printf("lux: %u\n", value);

        float humidity=0, temprature=0;
		uint8_t lastSuccess=0;
        outerHumidSensor.ReadValue(humidity, temprature, lastSuccess);
        printf("Humidity: %.1f%%\nTemprature: %.1f*C\nFails: %u\n", humidity, temprature, lastSuccess);

/*        uint8_t humidity=0, temprature=0;
		uint8_t lastSuccess=0;
        outerHumidSensor.ReadValue(humidity, temprature, lastSuccess);
        printf("Humidity: %d%%\nTemprature: %df*C\nFails: %u\n", humidity, temprature, lastSuccess);
*/
		sleep(2);
    }

	 return(0);
}

