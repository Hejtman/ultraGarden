#include "remote.h"
#include "../log.h"
#include "gardener.h"


Remote::Remote(Gardener& g) 
: gardener(g),
  checkCommandFileOccurrence(1*1000)
{

}

void Remote::SchedulerWakeUpCall(const uint8_t id)
{
	switch(id)
	{
		case CHECK_COMMAND_FILE:	CheckCommandFile();	break;
		default:
			LOG_ERROR("This shuld not happen!");
	}
}

void Remote::CheckCommandFile()
{
	const char CMD_FILE[] = "tmp/cmdfile";
	FILE* fp = fopen(CMD_FILE, "r");

	if (fp) {
		char line[256];
		bool empty = true;
		while(fgets(line, 256, fp) != NULL) {

			switch(saxHash2((const char*)line)) {
				case saxHash2("GARDENER_STOP_LOOP"):  gardener.StopLoop();    break;
				default:
					LOG_ERRORF("Parsing failed: '%s'", line);
			}
			empty = false;
		}
		fclose(fp);

		if (!empty){
			fp = fopen(CMD_FILE, "w");
			fclose(fp);
		}
	} else {
		LOG_ERRORF("Error opening file: '%s'", CMD_FILE);
	}
}

