import logging
import datetime
import threading
from collections import namedtuple
from itertools import chain
from time import sleep

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi

from config import OpenWeatherMapConf
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
        self.fogging_cycle  = (RelaySet(set=(fan.off, fog.on,  pump.off), delay=5 ),  # create some fog
                               RelaySet(set=(fan.on,  fog.on,  pump.off), delay=40),  # deliver fog
                               RelaySet(set=(fan.on,  fog.off, pump.off), delay=15))  # recycle fog
        self.watering_cycle = (RelaySet(set=(fan.off, fog.off, pump.on ), delay=8 ),  # begin pumping for a while
                               RelaySet(set=(fan.off, fog.on,  pump.off), delay=10))  # fan off until water level drops
        self.default_cycle  = (RelaySet(set=(fan.off, fog.off, pump.off), delay=0 ),) # relays config between cycles
        for r in self.relays:
            wiringpi.pinMode(r.pin, wiringpi.GPIO.OUTPUT)

        #self.barrel_temperature = ds18b20('28-011564df1dff', 'barrel')
        #self.balcony_temperature = ds18b20('28-011564aee4ff', 'balcony')
        # FIXME: brno > city (name move to config)
        self.brno_temperature = WeatherSensor('temp', 'Brno', OpenWeatherMapConf)
        self.brno_humidity = WeatherSensor('humidity', 'Brno_humidity', OpenWeatherMapConf)
        self.sensors = (
#                        self.barrel_temperature,
#                        self.balcony_temperature,
                        self.brno_temperature,
                        self.brno_humidity)

        self.last_fogging = None
        self.last_watering = None


    def fogging(self):
        threading.status = "fogging"
        self.last_fogging = datetime.datetime.now()
        logging.info("{} fogging".format(self.last_fogging))  # TODO: write temperature, write after how long?

        for relays_set in chain(self.fogging_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        threading.status = "waiting"


    def watering(self):
        threading.status = "watering"
        self.last_watering = datetime.datetime.now()
        logging.info("{} watering".format(self.last_watering))  # TODO: write temperature, write after how long?

        for relays_set in chain(self.watering_cycle, self.default_cycle):
            for relay, value in zip(self.relays, relays_set.set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relays_set.delay)
        threading.status = "waiting"

    def sensors_refresh(self):
        threading.status = "refresing"
        for s in self.sensors:
            try:
                s.read_value()
            except IOError:
                logging.error("Failed to read data from sensor " + s.name)
        threading.status = "waiting"
