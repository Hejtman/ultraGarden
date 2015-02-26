#ifndef LOG_H
#define LOG_H


#ifdef DEBUG
    #define LOG_DEBUG(...) do { \
        fprintf(stderr, "DEBUG %s:%d  ", __FILE__, __LINE__); \
        fprintf(stderr, __VA_ARGS__); \
        fprintf(stderr,"\n"); \
    } while(0)
#else
    #define LOG_DEBUG(...) do {} while (0)
#endif

#define LOG_FAIL(RC) do { \
    fprintf(stderr, "FAIL %s:%d   function '%s' failed with result: %d\n", __FILE__, __LINE__, __PRETTY_FUNCTION__, RC); \
} while(0)

#define FAIL_LOG_RET(EXPR) do { \
    int r = (EXPR); \
    if (r != 0) { \
        fprintf(stderr, "FAIL %s:%d   '%s' ended with: %d\n", __FILE__, __LINE__, #EXPR, r); \
        return r; \
    } \
} while(0)


#define LOG_ERROR(...) do { \
    fprintf(stderr, "ERROR %s:%d  ", __FILE__, __LINE__); \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr,"\n"); \
} while(0)

#define LOG_INFO(...) do { \
    fprintf(stderr, "INFO %s:%d  ", __FILE__, __LINE__); \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr,"\n"); \
} while(0)


#endif // LOG_H
