#ifndef  _MACRO_DEFINE
#define  _MACRO_DEFINE
//============basic===================
//#pragma GCC diagnostic ignored "-Wwrite-strings"

#define LOG_ERROR(msg) \
    do{ WARN_W.log(LL_ERROR,   "[%s:%d][%s] " msg "\n", __FILE__, __LINE__, __FUNCTION__); } while (0)

#define LOG_ERRORF(log_fmt, ...) \
    do{ WARN_W.log(LL_ERROR,   "[%s:%d][%s] " log_fmt "\n", __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__); } while (0)

#define LOG_WARN(msg) \
    do{ WARN_W.log(LL_WARNING,   "[%s:%d][%s] " msg "\n", __FILE__, __LINE__, __FUNCTION__); } while (0)

#define LOG_WARNF(log_fmt, ...) \
    do{ WARN_W.log(LL_WARNING,   "[%s:%d][%s] " log_fmt "\n", __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__); } while (0)

#define LOG_NOTICE(msg) \
    do{ INFO_W.log(LL_NOTICE,   "[%s:%d][%s] " msg "\n", __FILE__, __LINE__, __FUNCTION__); } while (0)

#define LOG_NOTICEF(log_fmt, ...) \
    do{ INFO_W.log(LL_NOTICE,   "[%s:%d][%s] " log_fmt "\n", __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__); } while (0)

#define LOG_TRACE(msg) \
    do{ INFO_W.log(LL_TRACE,   "[%s:%d][%s] " msg "\n", __FILE__, __LINE__, __FUNCTION__); } while (0)

#define LOG_TRACEF(log_fmt, ...) \
    do{ INFO_W.log(LL_TRACE,   "[%s:%d][%s] " log_fmt "\n", __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__); } while (0)

#define LOG_DEBUG(msg) \
    do{ INFO_W.log(LL_DEBUG,   "[%s:%d][%s] " msg "\n", __FILE__, __LINE__, __FUNCTION__); } while (0)

#define LOG_DEBUGF(log_fmt, ...) \
    do{ INFO_W.log(LL_DEBUG,   "[%s:%d][%s] " log_fmt "\n", __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__); } while (0)

#endif


