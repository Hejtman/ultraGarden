import logging

from config import Log
from gardener import Gardener


logging.basicConfig(level=Log.LEVEL, filename=Log.FILE)
logging.info("UltraGarden started.")

Gardener().working_loop()

logging.info("UltraGarden stopped.")
