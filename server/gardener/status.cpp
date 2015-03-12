#include "status.h"


const uint8_t BH1750FVI_I2C_ADDRESS = 0x23;  // sudo i2cdetect -y 1
const uint8_t IGNORE_FAILED_READINGS = 10;

Status::Status()

: barrelFogRelay(GPIO_0),
  barrelFunRelay(GPIO_0),
  barrelTideGate(GPIO_1, 90, 40),
  barrelHumidSensor(GPIO_2),
  pumpRelay(GPIO_0),
  pumpTideGate(GPIO_23,  85, 40),
  pumpHumidSensor(GPIO_5),
  outerHumidSensor(GPIO_5),
  outerLightSensor(BH1750FVI_I2C_ADDRESS)
{

}

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

