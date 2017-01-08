import logging
from time import sleep
from datetime import datetime

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from utils.logging import log_exceptions as _
from relays import Relays, RelayWiring
from sensors import Sensors
from hw.ds18b20.ds18b20 import ds18b20
from config import SensorData, GMailAccount, sms_gateway, log_level
from utils.communication import send_mail


class Garden:
    def __init__(self):
        # WIRING
        self.relays = Relays(
            fog=RelayWiring(pin=28, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW),  # by default on
            fan=RelayWiring(pin=29, off=wiringpi.GPIO.HIGH, on=wiringpi.GPIO.LOW),  # by default on
            pump=RelayWiring(pin=26, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)  # by default off
        )

        # fixme named tuple?
        self.sensors = Sensors(barrel_temperature=ds18b20("28-011564df1dff", "barrel"),
                               balcony_temperature=ds18b20("28-011564aee4ff", "balcony"))

        self.last_pumping_time = None

    def start(self):
        # noinspection PyBroadException
        try:
            self.relays.pumping()
            self.last_pumping_time = datetime.now()
        except:
            logging.exception("Watering failed!")

    def check_pumping(self, sensors, now):
        # FIXME: base calculation on sensor data [minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5]
        next_pumping_time = self.last_pumping_time + datetime.timedelta(minutes=10)
        if now >= next_pumping_time:
            # noinspection PyBroadException
            try:
                self.relays.pumping()
                self.last_pumping_time = now
                logging.info("{} watering".format(self.last_pumping_time))
            except:
                logging.exception("Watering failed!")


# MAIN INIT
wiringpi.wiringPiSetup()
logging.basicConfig(level=log_level, filename='/tmp/ultra_garden.log')


# START SERVER
if __name__ == '__main__':
    garden = Garden()
    garden.start()

    while True:
        now = datetime.now()
        record = _(garden.sensors.read_sensors_data)   # FIXME: each garden function should cought all its exceptions

        if now.minute % 10 == 0:
            _(garden.sensors.write_sensors_data, record, SensorData.full_file)

        garden.check_pumping(now, garden.last_pumping_time, garden.sensors)

        if now.minute == 0:
            month_of_records_count = 24*7*4
            _(garden.sensors.write_sensors_data, record, SensorData.short_file, max_records=month_of_records_count)

        if sms_gateway and (now.hour, now.minute) == (12, 00):
            # TODO: send water level info
            _(send_mail, GMailAccount.address, GMailAccount.password, sms_gateway, "I am alive")

        _(sleep(60-datetime.now().second))


# TODO: create more oxygen when high temperature
# TODO: no point in making fog when temperature is up to 26C or below 5C ?
