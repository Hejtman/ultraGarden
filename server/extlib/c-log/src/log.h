#ifndef   _MACRO_LogModule
#define   _MACRO_LogModule
#include <stdio.h>
#include <pthread.h>
#include <memory>
#include "macro_define.h"

#define   _LOG_BUFFSIZE  1024*1024*4
#define   _SYS_BUFFSIZE  1024*1024*8
#define	  _LOG_PATH_LEN  250
#define   _LOG_MODULE_LEN 32

typedef  enum LogLevel {  
	LL_DEBUG = 1,
	LL_TRACE = 2,
	LL_NOTICE = 3, 
	LL_WARNING = 4, 
	LL_ERROR = 5,
}LogLevel;

/**
 * LogLevel
 * p_modulename
 * p_logdir
 * */
bool log_init(LogLevel l, const char* p_modulename, const char* p_logdir);

/**
*	Log_Writer
*/
class Log_Writer
{
	enum LogLevel m_system_level;
	std::unique_ptr<FILE, void (*)(FILE*)> fp;
	bool m_issync;
	bool m_isappend;
	char m_filelocation[_LOG_PATH_LEN];
	pthread_mutex_t m_mutex;
	static __thread char m_buffer[_LOG_BUFFSIZE];

	const char* logLevelToString(LogLevel l);
	bool checklevel(LogLevel l);
	int premakestr(char* m_buffer, LogLevel l);
	bool _write(char *_pbuffer, int len);

	public:
		Log_Writer();
		~Log_Writer();

		bool loginit(LogLevel l, const  char *filelocation, bool append = true, bool issync = false);
		bool log(LogLevel l,char *logformat,...);
		LogLevel get_level();
		bool logclose();
		//The __thread specifier may be applied to any global, file-scoped static, function-scoped static, 
		//or static data member of a class. It may not be applied to block-scoped automatic or non-static data member
		//in the log  scence,It's safe!!!!
};

extern Log_Writer WARN_W;
extern Log_Writer INFO_W;

#endif
