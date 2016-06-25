//#include <iostream>
#include <stdio.h>
#include "lib.h"
#include "../log.h"


int exec(const char* cmd, char* buffer, const int length)
{
	FILE* pipe;
	FAIL_LOG_RET((pipe = popen(cmd, "r")) == NULL);
	FAIL_LOG_RET(feof(pipe));

	if (fgets(buffer, length, pipe)){
		// remove last character
		while (*buffer++ != '\n');
		*(--buffer) = 0;
	}

	pclose(pipe);
	return 0;
}

