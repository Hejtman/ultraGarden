#include "garden.h"
#include "../lib/lib.h"
#include "../config.h" // define: OS_USER, FTP_USER, FTP_PASSWORD as const char[]
#include <stdio.h>
#include <wiringPi.h>
#include <sys/sysinfo.h>
#include "../log.h"


const uint8_t BH1750FVI_I2C_ADDRESS = 0x23;  // sudo i2cdetect -y 1
const char STATUS_FILE[] = "tmp/status.php";
const char ALERT_STYLE[] = "background-color:red; opacity:1;";

Garden::Garden()
: watchDog(),
  dutyCycle(IDLING),
  dutyCycleTiming{	1*60*1000,	1*60*1000,	1*60*1000	},
  dutyCycleNames{	"FOGGING",	"IDLING",	"AIRING"	},
  dutyStartTime(0),
  barrelFogRelay(GPIO_3),
  barrelFunRelay(GPIO_2),
  barrelTideGate(GPIO_1, 90, 40),
  barrelHumidSensor(GPIO_6),
  barrelHumidSensorStatus(WatchDog::ALERT),
  barrelWatterLevel(GPIO_27, GPIO_0),
  pumpRelay(GPIO_4),
  pumpTideGate(GPIO_23,  85, 40),
  pumpHumidSensor(GPIO_25),
  pumpHumidSensorStatus(WatchDog::ALERT),
  outerHumidSensor(GPIO_5),
  outerHumidSensorStatus(WatchDog::ALERT),
  outerLightSensor(BH1750FVI_I2C_ADDRESS),
  outerLightSensorStatus(WatchDog::ALERT),
  cpuMonitor(),
  checkSensorOccurrence(10*1000),
  sendStatusFileOccurrence(1*60*1000),
  switchDutyCycleOccurrence(10*1000),
  pumpingCycleOccurrence(3*60*60*1000),
  pumpingCycleDuration(15*1000)
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

		case PUMPING_CYCLE_START:
			StartPumpingCycle();
			break;

		case PUMPING_CYCLE_STOP:
			StopPumpingCycle();
			break;
	}
}

void Garden::CheckSensors()
{
	LOG_DEBUG("Checking sensors.");

	barrelHumidSensorStatus = barrelHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( barrelHumidSensor.GetLastSuccess() );
	pumpHumidSensorStatus = pumpHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( pumpHumidSensor.GetLastSuccess() );
	outerHumidSensorStatus = outerHumidSensor.ReadValues() ?  WatchDog::ALERT : watchDog.GetHumidStatus( outerHumidSensor.GetLastSuccess() );
	outerLightSensorStatus = outerLightSensor.ReadValue() ?  WatchDog::ALERT : WatchDog::OK;
	barrelWatterLevel.ReadValue(); //TODO watchdog

	/* TODO: WATCHDOG for sensors
	switch (DutyCycle) {
		case FOGGING: is barel & pump humidity going up?
	} */
}

void Garden::SendStatusFile()
{
	LOG_DEBUG("Sending status file");

	FILE* pFile = fopen(STATUS_FILE,"w");

	if (pFile) {
		const unsigned int t = millis();
		unsigned int uptime, rpiUptime;
		char uptimeSuffix, rpiUptimeSuffix;
		secs2time(t/1000, uptime, uptimeSuffix);

		struct sysinfo info;
		sysinfo(&info);
		secs2time(info.uptime, rpiUptime, rpiUptimeSuffix);

		fprintf(pFile,
			"<?php\n"
			"	const REFRESHINTERVAL = %u;\n"
			"\n"
			"	$pi_status = new text(\"left: 25px; top:25px;\", \n"
			"		'<table>\n"
			"			<tr           ><th colspan=\"2\">	UltraGarden server 				</th></tr>\n"
			"			<tr           ><td>	State:	</td><td>	%s (%us / %us)			</td></tr>\n"
			"			<tr           ><td>	Uptime:	</td><td>	%u%c / %u%c				</td></tr>\n",
			sendStatusFileOccurrence / 1000, // millis > sec
			dutyCycleNames[dutyCycle], (t-dutyStartTime)/1000, dutyCycleTiming[dutyCycle]/1000,
			uptime, uptimeSuffix, rpiUptime, rpiUptimeSuffix
			);

		WriteCPUStatusLine(pFile);

		const int BUFFER_SIZE = 128;
		char line[BUFFER_SIZE];
		char diskInfo[3][16] = { 0 };
		FILE* apipe = popen("df -h /", "r");
		while( fgets(line, BUFFER_SIZE, apipe) ) {
			if (sscanf(line, "/%*s	%s	%*s	%s	%s", diskInfo[0], diskInfo[1], diskInfo[2]))
				break;
		}
		pclose(apipe);

		char os[10]={0}, osVer[10]={0}, krnlVer[15]={0}, ip[15]={0};
		exec("sed -nr 's/^NAME=\"(.*)\"$/\\1/p' /etc/os-release", os, 10);
		exec("sed -nr 's/^VERSION_ID=\"(.*)\"$/\\1/p' /etc/os-release", osVer, 10);
		exec("sed -nr 's/Linux version ([^ ]*) .*/\\1/p' /proc/version", krnlVer, 15);
		exec("ifconfig | sed -nr 's/.*inet addr:([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)  B.*/\\1/p'", ip, 15);
		fprintf(pFile,
			"			<tr           ><td>	Memory:	</td><td>	%luMB / %luMB			</td></tr>\n"
			"			<tr           ><td>	Storage:</td><td>	%s / %s (%s)			</td></tr>\n"
			"			<tr id=\"alert\"><td> Network:</td><td>	%s			</td></tr>\n"
//TODO wifi signal quality
			"			<tr           ><td>	OS:	</td><td>	%s %s	(%s)		</td></tr>\n"
			"		</table>');\n"
			"\n",
			info.freeram/(1024*1024), info.totalram/(1024*1024),
			diskInfo[1], diskInfo[0], diskInfo[2],
			ip,
			os, osVer, krnlVer
			);

		fprintf(pFile,
			"	$pump_tidegate = new image(\"pump_tidegate_\", \"%s\", \".gif\");\n"
			"	$barrel_tidegate = new image(\"barrel_tidegate_\", \"%s\", \".gif\");\n"
			"\n",
			(pumpTideGate.IsOpen() ? "opened" : "closed"), 
			(barrelTideGate.IsOpen() ? "opened" : "closed")
			);

		fprintf(pFile,//TODO
//			"	$pump = new text(\"left: 1303px; top:552px; %s\", \"<b>WAITING<br>last: %us<br>next: %us</b>\");\""
//			"	$pump = new text(\"left: 1303px; top:552px; %s\", \"<b>PUMPING<br>time: %us<br>eta: %us</b>\");\""
			"	$pump = new text(\"left: 400px; top:574px; %s\", \"<b>%s<br>last: %us<br>next: %us</b>\");\n"
			"\n",
			"", "WAITING" /*PUMPING*/, 0, 0
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
			"	$barrel_wlevel = new text(\"left: 655px; top:230px;\", \"<b>%umm (X d)<br>today: -AAmm<br>yrday: -BBmm</b>\");\n" // TODO
			"\n"
			"	$outer_light = new text(\"left: 950px; top:571px; %s\", \"<b>%d Lux</b>\");\n"
			"?>\n",
			barrelWatterLevel.GetValue(),
			outerLightSensorStatus == WatchDog::ALERT ?  ALERT_STYLE : "",
			outerLightSensor.GetValue()
			);

		fclose(pFile);

		UploadFile2FTP(STATUS_FILE, "ftp://" FTP_USER ":" FTP_PASSWORD "@ftp.malina.moxo.cz/ultraGarden/balcony1/status.php");
	}
}

void Garden::WriteCPUStatusLine(FILE* pFile)
{
	float cpuLoad[5] = {0};
	uint8_t cpus;
	cpuMonitor.GetCpuUsage(5, cpuLoad, cpus);

	char temp[10] = {0};
	exec("perl -e 'm/(\\d+)/; $x=$1; s/\\d+//; printf(\"%.1f\", ($x/1000))' -p /sys/class/thermal/thermal_zone0/temp 2>/dev/null", temp, 10);

	fprintf(pFile,
			"			<tr           ><td>	CPU:	</td><td>%d MHz &nbsp; %.2f%%	&nbsp; %s°C</td></tr>\n",
			cpuMonitor.GetCpuClock(0) / 1000, cpuLoad[0], temp
		);

	if (cpus > 1){
		fprintf(pFile,"			<tr           ><td> CORES:	</td><td>");
		for (int i = 1  ;  i < cpus  ;  ){
			fprintf(pFile, "%d%%",(int)cpuLoad[i]);
			if (++i < cpus)
				fprintf(pFile, "	");
		}
		fprintf(pFile, "</td></tr>\n");
	}
}

void Garden::SwitchDutyCycle()
{
	const unsigned int t = millis();
	LOG_DEBUGF("Duty cycle (%s: %dms)", dutyCycleNames[dutyCycle], t - dutyStartTime);

	if (dutyStartTime == 0)
		StartFogging();
	else if (t - dutyStartTime >= dutyCycleTiming[dutyCycle]) {
		switch(dutyCycle)
		{
			case FOGGING:	StartIdling();	break;
			case IDLING:	StartAiring();	break;
			case AIRING:	StartFogging();	break;
		}
	}
}

void Garden::StartFogging()
{
	LOG_DEBUG("Starting fogging.");

	pumpTideGate.Close();
	barrelTideGate.Close();
	barrelFogRelay.TurnOn();
	barrelFunRelay.TurnOn();

	dutyStartTime = millis();
	dutyCycle = FOGGING;
}

void Garden::StartIdling()
{
	LOG_DEBUG("Starting idling.");

	pumpTideGate.Close();
	barrelTideGate.Close();
	barrelFogRelay.TurnOff();
	barrelFunRelay.TurnOff();

	dutyStartTime = millis();
	dutyCycle = IDLING;
}

void Garden::StartAiring()
{
	LOG_DEBUG("Starting airing.");

	pumpTideGate.Open();
	barrelTideGate.Open();
	barrelFogRelay.TurnOff();
	barrelFunRelay.TurnOn();

	dutyStartTime = millis();
	dutyCycle = AIRING;
}

void Garden::StartPumpingCycle()
{
	LOG_DEBUG("Pumping started.");

	pumpRelay.TurnOn();
}

void Garden::StopPumpingCycle()
{
	LOG_DEBUG("Pumping stopped.");

	pumpRelay.TurnOff();
}

// TODO: server restart every 49 days? (WiringPi initialie) + Time2Restart

