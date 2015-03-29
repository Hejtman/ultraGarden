#include "lib.h"
#include "../log.h"
#include <fstream>


CpuMonitor::CpuMonitor()
: fp(fopen("/proc/stat", "r"), [](FILE *f){ fclose(f); }),
  total_tick_old(),
  idle_old()
{
}

int CpuMonitor::ReadFields(unsigned long long int *fields)
{
	const int BUF_MAX = 1024;
	char buffer[BUF_MAX];

	FAIL_LOG(fgets(buffer, BUF_MAX, fp.get()) == NULL);
	// line starts with c and a string. This is to handle cpu, cpu[0-9]+
	const int retval = sscanf(buffer, "c%*s %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu",
			&fields[0], &fields[1], &fields[2], &fields[3], &fields[4], &fields[5], &fields[6], &fields[7], &fields[8], &fields[9]);

	if (retval == 0)
		return -1;
	if (retval < 4) { // Atleast 4 fields is to be read
		LOG_ERROR("Error while reading /proc/stat cpu field.");
		return 1;
	}
	return 0;
}

int CpuMonitor::GetCpuUsage(const uint8_t cpus_max, float* loads, uint8_t& cpus)
{
	const int MAX_FILDS = 10;
	unsigned long long int fields[MAX_FILDS], total_tick, idle;
	unsigned int cpu = 0;
	for (  ;  cpu < cpus_max  &&  ReadFields(fields) == 0  ;  ++cpu)
	{
		total_tick = 0;
		for (int i = 0  ;  i < MAX_FILDS  ;  ++i)
			total_tick += fields[i];
	
		idle = fields[3];

		// no results for first measurement
		if (total_tick_old.size() == cpu) {
			total_tick_old.push_back(total_tick);
			idle_old.push_back(idle);
		} else {
			unsigned long long int del_total_tick = total_tick - total_tick_old[cpu];
			unsigned long long int del_idle = idle - idle_old[cpu];

			loads[cpu] = ((del_total_tick - del_idle) / (float) del_total_tick) * 100;

			total_tick_old[cpu] = total_tick;
			idle_old[cpu] = idle;
		}
	}
	cpus = cpu;
	fp.reset(fopen("/proc/stat", "r"));
	return 0;
}

int CpuMonitor::GetCpuClock(const uint8_t) const
{
	// FIXME 0 > core
	std::unique_ptr<FILE, void (*)(FILE*)> fx(fopen("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq", "r"), [](FILE *f){ fclose(f); });

	int clock = 0;
	const int BUF_MAX = 16;
	char buffer[BUF_MAX];

	FAIL_LOG(fgets(buffer, BUF_MAX, fx.get()) == NULL);
	FAIL_LOG(sscanf(buffer, "%d",&clock) != 1);
	return clock;
}

