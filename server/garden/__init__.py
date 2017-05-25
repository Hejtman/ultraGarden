import logging
from datetime import datetime, timedelta
from collections import namedtuple
from itertools import chain
from time import sleep

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi

import config
from utils.weather import WeatherSensor
from garden.hw.ds18b20 import ds18b20


RelayWiring = namedtuple('RelayWiring', 'pin off on')
RelaySet = namedtuple('RelaySet', 'set delay')

OLDEST_DATE = datetime(1, 1, 1)
ZERO_PERIOD = timedelta(minutes=0)


class Garden:
    """
    Controls HW I/O
     * sensors: temperature (TODO: water level, light density, ...)
     * relays: pump, fan, fogger
    """
    def __init__(self):
        # WIRING
        wiringpi.wiringPiSetup()

        self.fog = fog = RelayWiring(pin=28, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW)    # by default on
        self.fan = fan = RelayWiring(pin=27, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW)    # by default on
        self.pump = pump = RelayWiring(pin=29, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)  # by default off

        self.relays = (fan, fog, pump)
        self.default_cycle = (RelaySet(set=(fan.off, fog.off, pump.off), delay=0),)   # relays config between cycles
        self.fogging_cycle = (RelaySet(set=(fan.off, fog.on,  pump.off), delay=5),    # create some fog
                              RelaySet(set=(fan.on,  fog.on,  pump.off), delay=50),   # deliver fog
                              RelaySet(set=(fan.on,  fog.off, pump.off), delay=5))    # recycle fog
        self.watering_cycle = (RelaySet(set=(fan.off, fog.off, pump.on), delay=8),    # begin pumping for a while
                               RelaySet(set=(fan.off, fog.off, pump.off), delay=10))  # fan off until water level drops
        for r in self.relays:
            wiringpi.pinMode(r.pin, wiringpi.GPIO.OUTPUT)

        # self.barrel_temperature = ds18b20('28-011564df1dff', 'barrel')
        # self.balcony_temperature = ds18b20('28-011564aee4ff', 'balcony')
        self.city_temperature = WeatherSensor('temp', config.City, config.OpenWeatherMap)
        self.city_humidity = WeatherSensor('humidity', config.City + '_humidity', config.OpenWeatherMap)
        self.sensors = (
                        # self.barrel_temperature,
                        # self.balcony_temperature,
                        self.city_temperature,
                        self.city_humidity)

        self.status = "idling"
        self.last_change = OLDEST_DATE

        self.__last_job_run = {
            "FOGGING": OLDEST_DATE,
            "WATERING": OLDEST_DATE,
        }
        self.__job_run_count = {
            "FOGGING": 0,
            "WATERING": 0,
        }

        self.__start_time = datetime.now()

    def fogging(self):
        # FIXME: decorator?
        # TODO: DEBUG LOGS
        self.__job_run_count["FOGGING"] += 1
        self.status = "fogging"
        self.__last_job_run["FOGGING"] = self.last_change = datetime.now()

        for relays_set in chain(self.fogging_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        self.status = "idling"
        self.last_change = datetime.now()

    def watering(self):
        # FIXME: decorator?
        self.__job_run_count["WATERING"] += 1
        self.status = "watering"
        self.__last_job_run["WATERING"] = self.last_change = datetime.now()

        for relays_set in chain(self.watering_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        self.status = "idling"
        self.last_change = datetime.now()

    def sensors_refresh(self):
        # FIXME: decorator?
        self.status = "refreshing"
        self.last_change = datetime.now()

        for s in self.sensors:
            try:
                s.read_value()
            except IOError:
                logging.error("Failed to read data from sensor " + s.name)

        self.status = "idling"
        self.last_change = datetime.now()

    # encapsulation
    def get_last_job_run(self, job_id):
        return self.__last_job_run[job_id]

    def get_job_run_count(self, job_id):
        return self.__job_run_count[job_id]

    def get_start_time(self):
        return self.__start_time
