import logging
import schedule


try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from relays import Relays, RelayWiring
from sensors import Sensors
from hw.ds18b20.ds18b20 import ds18b20


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

        self.last_watering_time = None

    def schedule_watering(self):
        print("schedule watering")
        # FIXME: base calculation on sensor data [minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5]
        # FIXME: remember last run, get next run, run watering immediately if needed
        # TODO: create more oxygen when high temperature
        # TODO: no point in making fog when temperature is up to 26C or below 5C ?
        schedule.clear("WATERING")
        schedule.every(5).seconds.do(self.watering).tag("WATERING")

    def watering(self):
        print("watering")
        logging.info("{} watering".format(self.last_watering_time))  # TODO: write temperature
        self.relays.pumping()
