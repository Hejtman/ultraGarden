import wiringpi
from time import sleep
from datetime import datetime
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

# WIRING
relays = Relays(relays={"FOG": {"PIN": 28, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "FUN": {"PIN": 29, "ON": wiringpi.GPIO.LOW, "OFF": wiringpi.GPIO.HIGH},
                        "PUMP": {"PIN": 26, "ON": wiringpi.GPIO.HIGH, "OFF": wiringpi.GPIO.LOW}},  # PIN 11 unused yet
                timing={"BEFORE_PUMP": 2,
                        "PUMPING": 8,
                        "FUN_PROTECTION": 10})

sensors = Sensors([ds18b20("28-011564df1dff", "barrel"),
                   ds18b20("28-011564aee4ff", "balcony")])

relays.pumping_cycle()

while True:
    now = datetime.now()
    record = sensors.read_sensors_data()

    if now.minute % 5 == 0:
        sensors.write_sensors_data(record, SENSOR_DATA_FULL_FILE)

    if now.minute % 15 == 0:
        week_records_count = 4*24*7
        sensors.write_sensors_data(record, SENSOR_DATA_SHORT_FILE, max_records=week_records_count)
        relays.pumping_cycle()

    if sms_gateway and (now.hour, now.minute) == (12, 00):
        send_mail(gmail_account["address"], gmail_account["password"], sms_gateway, "I am alive")  # TODO: send water level info

    sleep(60-datetime.now().second)

# TODO: create more oxigen when high temperature
# TODO: no point in making fog when temperature is up to 26C or below 5C ?
# TODO: no point in funing when temperature is below 5C
