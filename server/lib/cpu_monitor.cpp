#include <stdio.h>
#include <unistd.h>
#include <vector>
 

class CpuMonitor
{
	std::vector<unsigned long long int> total_tick_old, idle_old;
	unsigned int time_old;

	int ReadFields(FILE *fp, unsigned long long int *fields);

public:
	CpuMonitor();

	int GetCpuUsage();
};


CpuMonitor::CpuMonitor() : time_old(0) 
{
}

int CpuMonitor::ReadFields(FILE *fp, unsigned long long int *fields)
{
	const int BUF_MAX = 1024;
	char buffer[BUF_MAX];

	if (!fgets (buffer, BUF_MAX, fp))
		perror ("Error");
	// line starts with c and a string. This is to handle cpu, cpu[0-9]+
	const int retval = sscanf(buffer, "c%*s %Lu %Lu %Lu %Lu %Lu %Lu %Lu %Lu %Lu %Lu", 
			&fields[0], &fields[1], &fields[2], &fields[3], &fields[4], &fields[5], &fields[6], &fields[7], &fields[8], &fields[9]);
	
	if (retval == 0)
		return -1;
	if (retval < 4) { // Atleast 4 fields is to be read
		fprintf (stderr, "Error reading /proc/stat cpu field\n");
		return 1;
	}
	return 0;
}

int CpuMonitor::GetCpuUsage()
{
	// TODO LOG, keep fp open, dynamic closing fp
	FILE* fp = fopen("/proc/stat", "r");
	if (fp == NULL)
		return 1;

	const int MAX_FILDS = 10;
	unsigned long long int fields[MAX_FILDS], total_tick, idle;
	for (unsigned int cpu = 0  ;  ReadFields(fp, fields) == 0  ;  ++cpu)
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

			double percent_usage = ((del_total_tick - del_idle) / (double) del_total_tick) * 100;
			if (cpu == 0)
				printf ("%3.2lf%%: ", percent_usage);
			else
				printf ("%3.2lf%% ", percent_usage);

			total_tick_old[cpu] = total_tick;
			idle_old[cpu] = idle;
		}
	}

	fclose(fp);
	return 0;
}
/*
int main (void)
{
	CpuMonitor monitor;

	monitor.GetCpuUsage();
	sleep(1);
	printf("\n");
	monitor.GetCpuUsage();
	return 0;
}
*/
