#ifndef LIB_H
#define LIB_H

#include <stdint.h>
#include <vector>
#include <stdio.h>
#include <memory>

void UploadFile2FTP(const char* filePath, const char* url);
void secs2time(unsigned int sec, unsigned int& number, char& suffix);


class CpuMonitor
{
	std::unique_ptr<FILE, void (*)(FILE*)> fp;
	std::vector<unsigned long long int> total_tick_old, idle_old;

	int ReadFields(unsigned long long int *fields);

public:
	CpuMonitor();

	int GetCpuUsage(const uint8_t cpus_max, float* loads);
};


#endif // LIB_H

