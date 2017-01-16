import logging
import datetime

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from garden.relays import Relays, RelayWiring
from garden.sensors import Sensors
from garden.hw.ds18b20.ds18b20 import ds18b20
# from utils.communication import send_mail
# GMailAccount


class Garden:
    def __init__(self):
        # WIRING
        self.relays = Relays(
            fog=RelayWiring(pin=23, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW),  # by default on
            fan=RelayWiring(pin=24, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW),  # by default on
            pump=RelayWiring(pin=25, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)  # by default off
        )

        self.sensors = Sensors(barrel_temperature=ds18b20("28-011564df1dff", "barrel"),
                               balcony_temperature=ds18b20("28-011564aee4ff", "balcony"))

        self.last_watering_time = datetime.datetime.now() - datetime.timedelta(days=365)

    def check_watering(self):
        print("check watering")
        # FIXME: base calculation on sensor data [minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5]
        # TODO: create more oxygen when high temperature
        # TODO: no point in making fog when temperature is up to 26C or below 5C ?
        if datetime.datetime.now() - self.last_watering_time > datetime.timedelta(minutes=20):
            self.watering()

    def watering(self):
        print("watering")
        logging.info("{} watering".format(self.last_watering_time))  # TODO: write temperature
        self.relays.pumping()
        self.last_watering_time = datetime.datetime.now()
