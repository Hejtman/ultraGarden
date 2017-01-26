import logging

from gardener import Gardener
from config import Log


logging.basicConfig(level=Log.LEVEL, filename=Log.FILE)

# START SERVER MAIN LOOP
Gardener().working_loop()
