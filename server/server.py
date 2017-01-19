import logging

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from gardener import Gardener
from config import Log


wiringpi.wiringPiSetup()
logging.basicConfig(level=Log.LEVEL, filename=Log.FILE)

# START SERVER MAIN LOOP
Gardener().working_loop()
