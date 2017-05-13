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
        self.brno_temperature = WeatherSensor('temp', config.City, config.OpenWeatherMap)
        self.brno_humidity = WeatherSensor('humidity', config.City + '_humidity', config.OpenWeatherMap)
        self.sensors = (
                        # self.barrel_temperature,
                        # self.balcony_temperature,
                        self.brno_temperature,
                        self.brno_humidity)

        self.status = "idling"
        self.last_change = OLDEST_DATE

        self.__last_fogging = OLDEST_DATE
        self.next_fogging = OLDEST_DATE
        self.fogging_period = ZERO_PERIOD

        self.__last_watering = OLDEST_DATE
        self.next_watering = OLDEST_DATE
        self.watering_period = ZERO_PERIOD

    def fogging(self):
        print(str(datetime.now()) + " fogging")
        # FIXME: decorator?
        # TODO: DEBUG LOGS
        self.status = "fogging"
        self.__last_fogging = self.last_change = datetime.now()
        self.next_fogging = datetime.now() + self.fogging_period

        for relays_set in chain(self.fogging_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        self.status = "idling"
        self.last_change = datetime.now()

    def watering(self):
        # FIXME: decorator?
        self.status = "watering"
        self.__last_watering = self.last_change = datetime.now()
        self.next_watering = datetime.now() + self.watering_period

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

    def get_last_fogging(self):
        return self.__last_fogging

    def get_last_watering(self):
        return self.__last_watering
