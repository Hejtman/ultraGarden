#include "log.h"
#include <sys/file.h>
#include <stdarg.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/stat.h>

Log_Writer WARN_W;
Log_Writer INFO_W;
__thread char Log_Writer::m_buffer[_LOG_BUFFSIZE];

bool log_init(LogLevel l, const char* p_modulename, const char* p_logdir)
{
	if (access (p_logdir, 0) == -1)
	{
		if (mkdir (p_logdir, S_IREAD | S_IWRITE ) < 0)
			fprintf(stderr, "create folder failed\n");
	}
	char _location_str[_LOG_PATH_LEN];
	snprintf(_location_str, _LOG_PATH_LEN, "%s/%s.access", p_logdir, p_modulename);	
	INFO_W.loginit(l, _location_str);
	snprintf(_location_str, _LOG_PATH_LEN, "%s/%s.error", p_logdir, p_modulename);

	if(l > LL_WARNING)
		WARN_W.loginit(l, _location_str);
	else
		WARN_W.loginit(LL_WARNING, _location_str);
	return true;
}

Log_Writer::Log_Writer()
: m_system_level(LL_NOTICE),
  fp(NULL,[](FILE* f){
	if (f){
		fflush(f);
		fclose(f);
	}
  }),
  m_issync(false),
  m_isappend(true),
  m_mutex()
{
	m_filelocation[0] ='\0';
	pthread_mutex_init(&m_mutex, NULL);
}

Log_Writer::~Log_Writer(){
}

const char* Log_Writer::logLevelToString(LogLevel l) {
        switch ( l ) {
			case LL_DEBUG:
				return "DEBUG";
			case LL_TRACE:
				return "TRACE";
			case LL_NOTICE:
				return "NOTICE";
			case LL_WARNING:
				return "WARN" ;
			case LL_ERROR:
				return "ERROR";
			default:
				return "UNKNOWN";
        }
}
	
bool Log_Writer::checklevel(LogLevel l)
{
	if(l >= m_system_level)
		return true;
	else
		return false;
}

bool Log_Writer::loginit(LogLevel l, const  char *filelocation, bool append, bool issync)
{
	if ( fp.get() )
		return false;
    m_system_level = l;
    m_isappend = append; 
    m_issync = issync; 
	if(strlen(filelocation) >= (sizeof(m_filelocation) -1))
	{
		fprintf(stderr, "the path of log file is too long:%d limit:%d\n", strlen(filelocation), sizeof(m_filelocation) -1);
		exit(0);
	}
	strncpy(m_filelocation, filelocation, sizeof(m_filelocation));
	m_filelocation[sizeof(m_filelocation) -1] = '\0';
	
	if('\0' == m_filelocation[0])
	{
		fp.reset(stdout);
		fprintf(stderr, "now all the running-information are going to put to stderr\n");
		return true;
	}
	
	fp.reset(fopen(m_filelocation, append ? "a":"w"));

	if(fp.get() == NULL)
	{
		fprintf(stderr, "cannot open log file,file location is %s\n", m_filelocation);
		exit(0);
	}
	//setvbuf (fp, io_cached_buf, _IOLBF, sizeof(io_cached_buf)); //buf set _IONBF  _IOLBF  _IOFBF
	setvbuf (fp.get(),  (char *)NULL, _IOLBF, 0);
	fprintf(stderr, "now all the running-information are going to the file %s\n", m_filelocation);
	return true;
}

int Log_Writer::premakestr(char* m_buffer, LogLevel l)
{
    time_t now;
	now = time(&now);;
	struct tm vtm; 
    localtime_r(&now, &vtm);
    return snprintf(m_buffer, _LOG_BUFFSIZE, "%s: %02d-%02d %02d:%02d:%02d ", logLevelToString(l),
            vtm.tm_mon + 1, vtm.tm_mday, vtm.tm_hour, vtm.tm_min, vtm.tm_sec);
}

bool Log_Writer::log(LogLevel l, char* logformat,...)
{
	if (!checklevel(l))
		return false;
	int _size;
	int prestrlen = 0;
	
	char * star = m_buffer;
	prestrlen = premakestr(star, l);
	star += prestrlen;
	
	va_list args;
	va_start(args, logformat);
	_size = vsnprintf(star, _LOG_BUFFSIZE - prestrlen, logformat, args);
	va_end(args);
	
	if(fp.get() == NULL)
		fprintf(stderr, "%s", m_buffer);
	else
		_write(m_buffer, prestrlen + _size);
	return true;
}

bool Log_Writer::_write(char *_pbuffer, int len)
{
	if(0 != access(m_filelocation, W_OK))
	{	
		pthread_mutex_lock(&m_mutex);
		if(0 != access(m_filelocation, W_OK))
		{
			fp.release();
			loginit(m_system_level, m_filelocation, m_isappend, m_issync);
		}
		pthread_mutex_unlock(&m_mutex);
	}

	if(1 == fwrite(_pbuffer, len, 1, fp.get())) //only write 1 item
	{
		if(m_issync)
          	fflush(fp.get());
		*_pbuffer='\0';
    }
    else 
	{
        int x = errno;
	    fprintf(stderr, "Failed to write to logfile. errno:%s    message:%s", strerror(x), _pbuffer);
	    return false;
	}
	return true;
}

LogLevel Log_Writer::get_level()
{
	return m_system_level; 
}

