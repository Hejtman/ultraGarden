#include "garden.h"
#include "../config.h" // OS_USER, FTP_USER, FTP_PASSWORD
#include <stdio.h>
#include <wiringPi.h>//


extern void UploadFile2FTP(const char* filePath, const char* url);

const uint8_t BH1750FVI_I2C_ADDRESS = 0x23;  // sudo i2cdetect -y 1
const char STATUS_FILE[] = "status.php";
const char ALERT_STYLE[] = "background-color:red; opacity:1;";

Garden::Garden()

: watchDog(),
  barrelFogRelay(GPIO_0),
  barrelFunRelay(GPIO_0),
  barrelTideGate(GPIO_1, 90, 40),
  barrelHumidSensor(GPIO_2),
  barrelHumidSensorStatus(WatchDog::ALERT),
  pumpRelay(GPIO_0),
  pumpTideGate(GPIO_23,  85, 40),
  pumpHumidSensor(GPIO_5),
  pumpHumidSensorStatus(WatchDog::ALERT),
  outerHumidSensor(GPIO_5),
  outerHumidSensorStatus(WatchDog::ALERT),
  outerLightSensor(BH1750FVI_I2C_ADDRESS),
  outerLightSensorStatus(WatchDog::ALERT),
  checkSensorOccurrence(10*1000),
  sendStatusFileOccurrence(1*60*1000),
  switchDutyCycleOccurrence(5*60*1000)

{

}

void Garden::SchedulerWakeUpCall(const uint8_t id)
{
	switch (id) {
		case CHECK_SENSORS:
			CheckSensors();
			break;

		case SEND_STATUS_FILE:
			SendStatusFile();
			break;

		case SWITCH_DUTTY_CYCLE:
			SwitchDutyCycle();
			break;
	}
}

void Garden::CheckSensors()
{
	printf("%d\tCheckSensors\n", millis()); // debug log

	barrelHumidSensorStatus = barrelHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( barrelHumidSensor.GetLastSuccess() );
	pumpHumidSensorStatus = pumpHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( pumpHumidSensor.GetLastSuccess() );
	outerHumidSensorStatus = outerHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( outerHumidSensor.GetLastSuccess() );
	outerLightSensorStatus = outerLightSensor.ReadValue() ?  WatchDog::ALERT : WatchDog::OK;

	/* TODO: WATCHDOG for sensors
	switch (DutyCycle) {
		case FOGGING: is barel & pump humidity going up?
	} */
}

void Garden::SendStatusFile()
{
	printf("%d\tSendStatusFile\n", millis()); // debug log

	FILE* pFile = fopen(STATUS_FILE,"w");

	if (pFile) {
		fprintf(pFile,
			"<?php\n"
			"	const REFRESHINTERVAL = %u;\n"
			"\n"
			"	$pi_status = new text(\"left: 25px; top:25px;\", \n"
			"		'<table>\n"
			"			<tr           ><th colspan=\"2\">	UltraGarden server 				</th></tr>\n"
			"			<tr           ><td>	State:	</td><td>	Fogging (XXs)			</td></tr>\n" //TODO
			"			<tr           ><td>	&nbsp;	</td><td>							</td></tr>\n"
			"			<tr           ><td>	CPU:	</td><td>	XXX MHz  XX%%  XX�		</td></tr>\n" //TODO
			"			<tr           ><td>	Memory:	</td><td>	XXXMB / XXXMB			</td></tr>\n" //TODO
			"			<tr           ><td>	Video:	</td><td>	XXXXxXXXX (XX.XX fps)	</td></tr>\n" //TODO
			"			<tr id=\"alert\"><td> Network:</td><td>	192.168.0.104			</td></tr>\n" //TODO
			"			<tr           ><td>	Storage:</td><td>	XXXXGB / XXXXGB (XX%%)	</td></tr>\n" //TODO
			"			<tr           ><td>	Kernel:	</td><td>	X.XX.X					</td></tr>\n" //TODO
			"			<tr           ><td>	Uptime:	</td><td>	XX Days					</td></tr>\n" //TODO
			"		</table>');\n"
			"\n",
			sendStatusFileOccurrence / 1000 // millis > sec
			);

		fprintf(pFile,
			"	$pump_tidegate = new image(\"pump_tidegate_\", \"%s\", \".gif\");\n"
			"	$barrel_tidegate = new image(\"barrel_tidegate_\", \"%s\", \".gif\");\n"
			"\n",
			(pumpTideGate.IsOpen() ? "opened" : "closed"), 
			(barrelTideGate.IsOpen() ? "opened" : "closed")
			);

		fprintf(pFile,
			"	$pump_dht  = new text(\"left: 168px; top:584px; %s\", \"<b>%.1f%%<br>%.1f°C<br>%u</b>\");\n"
			"	$barrel_dht = new text(\"left: 690px; top:170px; %s\", \"<b>%.1f%%<br>%.1f°C<br>%u</b>\");\n"
			"	$outer_dht = new text(\"left: 1103px; top:552px; %s\", \"<b>%.1f%%<br>%.1f°C<br>%u</b>\");\n"
			"\n",
			pumpHumidSensorStatus == WatchDog::ALERT ?  ALERT_STYLE : "", 
			pumpHumidSensor.GetHumidity(), 
			pumpHumidSensor.GetTemperature(), 
			pumpHumidSensor.GetLastSuccess(),
			barrelHumidSensorStatus == WatchDog::ALERT ?  ALERT_STYLE : "", 
			barrelHumidSensor.GetHumidity(), 
			barrelHumidSensor.GetTemperature(), 
			barrelHumidSensor.GetLastSuccess(),
			outerHumidSensorStatus == WatchDog::ALERT ?  ALERT_STYLE : "", 
			outerHumidSensor.GetHumidity(), 
			outerHumidSensor.GetTemperature(), 
			outerHumidSensor.GetLastSuccess()
			);

		fprintf(pFile,
			"	$barrel_wlevel = new text(\"left: 655px; top:230px;\", \"<b>XX.Xcm (5 d)<br>today: -AA.Acm<br>yrday: -BB.Bcm</b>\");\n" //TODO
			"\n"
			"	$outer_light = new text(\"left: 950px; top:571px; %s\", \"<b>%d Lux</b>\");\n"
			"?>\n",
			outerLightSensorStatus == WatchDog::ALERT ?  ALERT_STYLE : "",
			outerLightSensor.GetValue()
			);

		fclose(pFile);

		UploadFile2FTP(STATUS_FILE, "ftp://" FTP_USER ":" FTP_PASSWORD "@ftp.malina.moxo.cz/ultraGarden/balcony1/status.php");
	}
	// TODO ErrorHandling
}

void Garden::SwitchDutyCycle()
{
	printf("%d\tSwitchDutyCycle\n", millis()); // debug log
}

