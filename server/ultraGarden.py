import logging
from time import sleep
from datetime import datetime

import wiringpi     # local emulator version imported when global not found

# from hw.releTest import releTest
from relays import Relays
from sensors import Sensors
from hw.ds18b20.ds18b20 import ds18b20
from config import gmail_account, sms_gateway
from utils.communication import send_mail


# files
SENSOR_DATA_SHORT_FILE = "/var/www/html/sensors_data_short"
SENSOR_DATA_FULL_FILE = "/var/www/html/sensors_data_full"

# MAIN
wiringpi.wiringPiSetup()
logging.basicConfig(level=logging.DEBUG, filename='/tmp/ultra_garden.log')

# WIRING
relays = Relays(relays={"FOG": {"PIN": 28, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "FUN": {"PIN": 29, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "PUMP": {"PIN": 26, "ON": wiringpi.GPIO.HIGH, "OFF": wiringpi.GPIO.LOW}},  # PIN 11 unused yet
                timing={"BEFORE_PUMP": 2,
                        "PUMPING": 8,
                        "FUN_PROTECTION": 10})

sensors = Sensors([ds18b20("28-011564df1dff", "barrel"),
                   ds18b20("28-011564aee4ff", "balcony")])


def _(func, *args, **kwargs):
        # noinspection PyBroadException
        try:
            return func(*args, **kwargs)
        except:
            logging.exception("Main oops:")

#####relays.pumping_cycle()

while True:
    now = datetime.now()
    record = _(sensors.read_sensors_data)

    if now.minute % 10 == 0:
        _(sensors.write_sensors_data, record, SENSOR_DATA_FULL_FILE)
        _(relays.pumping_cycle)

    if now.minute == 0:
        month_of_records_count = 24*7*4
        _(sensors.write_sensors_data, record, SENSOR_DATA_SHORT_FILE, max_records=month_of_records_count)

    if sms_gateway and (now.hour, now.minute) == (12, 00):
        # TODO: send water level info
        _(send_mail, gmail_account["address"], gmail_account["password"], sms_gateway, "I am alive")

    sleep(60-datetime.now().second)

# TODO: create more oxigen when high temperature
# TODO: no point in making fog when temperature is up to 26C or below 5C ?
# TODO: no point in funing when temperature is below 5C
# wattering interval in minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5