import logging
from time import sleep
from datetime import datetime

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from utils.logging import log_exceptions
from relays import Relays
from sensors import Sensors
from hw.ds18b20.ds18b20 import ds18b20
from config import gmail_account, sms_gateway, log_level
from utils.communication import send_mail


# MAIN INIT
wiringpi.wiringPiSetup()
logging.basicConfig(level=log_level, filename='/tmp/ultra_garden.log')

# FILES
SENSOR_DATA_SHORT_FILE = "/var/www/html/sensors_data_short"
SENSOR_DATA_FULL_FILE = "/var/www/html/sensors_data_full"

# WIRING
# FIXME: named tuples?
relays = Relays(relays={"FOG": {"PIN": 28, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "FAN": {"PIN": 29, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "PUMP": {"PIN": 26, "ON": wiringpi.GPIO.HIGH, "OFF": wiringpi.GPIO.LOW}},  # PIN 11 unused yet
                timing={"BEFORE_PUMP": 2,
                        "PUMPING": 8,
                        "FAN_PROTECTION": 10})

sensors = Sensors([ds18b20("28-011564df1dff", "barrel"),
                   ds18b20("28-011564aee4ff", "balcony")])


# START SERVER
if __name__ == '__main__':
    relays.pumping_cycle()

    while True:
        now = datetime.now()
        record = log_exceptions(sensors.read_sensors_data)

        if now.minute % 10 == 0:
            log_exceptions(sensors.write_sensors_data, record, SENSOR_DATA_FULL_FILE)
            log_exceptions(relays.pumping_cycle)

        if now.minute == 0:
            month_of_records_count = 24*7*4
            log_exceptions(sensors.write_sensors_data, record, SENSOR_DATA_SHORT_FILE, max_records=month_of_records_count)

        if sms_gateway and (now.hour, now.minute) == (12, 00):
            # TODO: send water level info
            log_exceptions(send_mail, gmail_account["address"], gmail_account["password"], sms_gateway, "I am alive")

        sleep(60-datetime.now().second)


# TODO: create more oxygen when high temperature
# TODO: no point in making fog when temperature is up to 26C or below 5C ?
# TODO: watering interval in minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5
