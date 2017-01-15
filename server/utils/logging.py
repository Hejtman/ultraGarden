import logging
import functools


def log_exceptions(func, *args, **kwargs):
    logging.debug("running: " + func.__name__)

    # noinspection PyBroadException
    try:
        return func(*args, **kwargs)
    except:
        logging.exception("Main oops:")


def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
    return wrapper
