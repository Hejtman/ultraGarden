#include "log.h"
#include "hw/bh1750.h"
#include "hw/dht22.h"
#include "hw/relay.h"
#include "hw/tidegate.h"
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "scheduler.h"

enum taskId{CHECK_COMMAND_FILE, CHECK_SENSORS, SEND_STATUS_FILE, SWITCH_DUTTY_CYCLE, REFLECT_LIGHT, PUMPING_CYCLE};
void f()
{
	printf("%u f\n", micros());///////
}
extern void SendStatusFile();

const uint8_t BH1750FVI_I2C_ADDRESS = 0x23;  // sudo i2cdetect -y 1
const uint8_t IGNORE_FAILED_READINGS = 10;

int main(int, char **)
{
//    relay  fogRelay(GPIO_0);
//    relay  pumpRelay(GPIO_1);
//    dht11  tankHumidSensor(GPIO_2, MAXERRORS);
//    dht11   pumpHumidSensor(GPIO_5, IGNORE_FAILED_READINGS);
//    dht11   outerHumidSensor(GPIO_5, IGNORE_FAILED_READINGS);
	dht22		outerHumidSensor(GPIO_5);
	TideGate	barrelTideGate(GPIO_1, 90, 40); // final settings
	TideGate	pumpTideGate(GPIO_23, 90, 40);////

	Scheduler scheduler;
	scheduler.RegisterTask(CHECK_COMMAND_FILE,	0,				1*1000,			&f);
	scheduler.RegisterTask(CHECK_SENSORS, 		0, 				10*1000,		&f);
	scheduler.RegisterTask(SEND_STATUS_FILE, 	1*60*1000,		1*60*1000,		&SendStatusFile);
	scheduler.RegisterTask(SWITCH_DUTTY_CYCLE,	5*60*1000,		5*60*1000,		&f);
	scheduler.RegisterTask(REFLECT_LIGHT, 		15*60*1000,		15*60*1000,		&f);
	scheduler.RegisterTask(PUMPING_CYCLE, 		2*60*60*1000,	2*60*60*1000,	&f);

//    bh1750 lightSensor1(BH1750FVI_I2C_ADDRESS);
    //-------------------------------------------

	if ( wiringPiSetup() == -1 )
    	return 1;

	piHiPri(99); // might have better performance for reading from dht22?

	scheduler.StartLoop();

/*
sleep(5);
barrelTideGate.Open();	sleep(1);
pumpTideGate.Open();	sleep(1);

barrelTideGate.Close();	sleep(1);
pumpTideGate.Close();	sleep(1);

*/
/*
        while(1)
        {
        fogRelay.TurnOn();
        sleep(1);
        fogRelay.TurnOff();
        sleep(1);
        }

*/

/*    for(int i=0 ; i<100 ; ++i) {
//        uint16_t value = 0;
//        lightSensor1.ReadValue(value);
//        printf("lux: %u\n", value);

        float humidity=0, temprature=0;
		uint8_t lastSuccess=0;
        outerHumidSensor.ReadValue(humidity, temprature, lastSuccess);
        printf("Humidity: %.1f%%\nTemprature: %.1f*C\nFails: %u\n", humidity, temprature, lastSuccess);

		sleep(2);
    }
*/
	 return(0);
}

