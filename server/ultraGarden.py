import wiringpi
from time import sleep
from datetime import datetime
# from hw.releTest inport releTest
from relays import Relays
from sensors import Sensors
from hw.ds18b20.ds18b20 import ds18b20


# files
SENSOR_DATA_SHORT_FILE = "/var/www/html/sensors_data_short"
SENSOR_DATA_FULL_FILE = "/var/www/html/sensors_data_full"

# MAIN
wiringpi.wiringPiSetup()

# WIRING
relays = Relays(relays={"FOG": [28, wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH],
                        "FUN": [29, wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH],
                        "PUMP": [26, wiringpi.GPIO.HIGH, wiringpi.GPIO.LOW]},  # PIN 11 unused yet
                timing={"PUMPING": 6,
                        "FUN_PROTECTION": 10})

sensors = Sensors([ds18b20("28-011564aee4ff", "tube"),
                   ds18b20("28-011564d01bff", "barel"),
                   ds18b20("28-011564df1dff", "balcony")])

relays.pumping_cycle()

while True:
    record = sensors.read_sensors_data()

    if datetime.now().minute % 5 == 0:
        sensors.write_sensors_data(record, SENSOR_DATA_FULL_FILE)

    if datetime.now().minute % 15 == 0:
        week_records_count = 4*24*7
        sensors.write_sensors_data(record, SENSOR_DATA_SHORT_FILE, max_records=week_records_count)
        relays.pumping_cycle()

    sleep(60-datetime.now().second)

#TODO: no point in making fog when temperature is up to 26C or below 5C ?
#TODO: no point in funing when temperature is below 5C
