#ifndef LOG_H
#define LOG_H


#include "extlib/c-log/src/log.h"

#define FAIL_LOG(RC) do { \
    int r = (EXPR); \
    if (r != 0) { \
		LOG_ERROR("'%s' ended with: %d\n", #EXPR, r); \
        return r; \
    } \
} while(0)

#define FAIL_LOG_RET(EXPR) do { \
    int r = (EXPR); \
    if (r != 0) { \
		LOG_ERROR("'%s' ended with: %d\n", #EXPR, r); \
        return r; \
    } \
} while(0)


#endif // LOG_H

