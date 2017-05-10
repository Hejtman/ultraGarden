import logging
from logging import handlers

from config import Log
from gardener import Gardener


file_handler = logging.handlers.WatchedFileHandler(filename=Log.FILE)
logging.basicConfig(level=Log.LEVEL, handlers=(file_handler,))
logging.info("UltraGarden started.")

Gardener().working_loop()

logging.info("UltraGarden stopped.")
