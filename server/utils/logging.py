import logging


def log_exceptions(func, *args, **kwargs):
    logging.debug("running: " + func.__name__)

    # noinspection PyBroadException
    try:
        return func(*args, **kwargs)
    except:
        logging.exception("Main oops:")
