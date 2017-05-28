import logging
from logging import handlers

from config import Log
from gardener import Gardener


logging_params = {
    'format': '%(asctime)-15s %(message)s',
    'handlers': (
        logging.handlers.WatchedFileHandler(filename=Log.FILE),
    ),
    'level': Log.LEVEL
}

logging.basicConfig(**logging_params)
logging.info("UltraGarden started.")

Gardener().working_loop()

logging.info("UltraGarden stopped.")
