import logging
import datetime
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
                              RelaySet(set=(fan.on,  fog.on,  pump.off), delay=40),   # deliver fog
                              RelaySet(set=(fan.on,  fog.off, pump.off), delay=15))   # recycle fog
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
        self.last_change = None

        self.last_fogging = None
        self.next_fogging = None
        self.interval_fogging = None

        self.last_watering = None
        self.next_watering = None
        self.interval_watering = None

    def fogging(self):
        # FIXME: decorator?
        self.status = "fogging"
        self.last_fogging = self.last_change = datetime.datetime.now()

        for relays_set in chain(self.fogging_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        self.status = "idling"
        self.last_change = datetime.datetime.now()

    def watering(self):
        # FIXME: decorator?
        self.status = "watering"
        self.last_watering = self.last_change = datetime.datetime.now()

        for relays_set in chain(self.watering_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        self.status = "idling"
        self.last_change = datetime.datetime.now()

    def sensors_refresh(self):
        # FIXME: decorator?
        self.status = "refreshing"
        self.last_change = datetime.datetime.now()

        for s in self.sensors:
            try:
                s.read_value()
            except IOError:
                logging.error("Failed to read data from sensor " + s.name)

        self.status = "idling"
        self.last_change = datetime.datetime.now()
