import logging

from config import Log
from gardener import Gardener


logging.basicConfig(level=Log.LEVEL, filename=Log.FILE)

# START SERVER MAIN LOOP
Gardener().working_loop()
