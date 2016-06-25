import wiringpi
from time import sleep
from datetime import datetime
# from hw.releTest inport releTest
from hw.ds18b20.ds18b20 import ds18b20


# WRING PI
FOG_RELE = 28
FUN_RELE = 29
PUMP_RELE = 26
UNUSED_RELE = 11

# WIRING
FOG_ON = wiringpi.GPIO.LOW
FOG_OFF = wiringpi.GPIO.HIGH
FUN_ON = wiringpi.GPIO.LOW
FUN_OFF = wiringpi.GPIO.HIGH
PUMP_ON = wiringpi.GPIO.HIGH
PUMP_OFF = wiringpi.GPIO.LOW
sensors = [ds18b20("28-011564aee4ff", "tube"),
           ds18b20("28-011564d01bff", "barel"),
           ds18b20("28-011564df1dff", "balcony")]

# timing
PUMPING_TIME = 6
FUN_PROTECT_TIME = 10

# files
SENSOR_DATA_FILE = "/var/www/html/sensors_data"


def pumpingCycle():
    try:
        wiringpi.digitalWrite(FUN_RELE, FUN_OFF)
        wiringpi.digitalWrite(FOG_RELE, FOG_OFF)
        wiringpi.digitalWrite(PUMP_RELE, PUMP_ON)
        sleep(PUMPING_TIME)

        wiringpi.digitalWrite(FUN_RELE, FUN_OFF)
        wiringpi.digitalWrite(FOG_RELE, FOG_ON)
        wiringpi.digitalWrite(PUMP_RELE, PUMP_OFF)
        sleep(FUN_PROTECT_TIME)

        # run fun after watter level drops
        wiringpi.digitalWrite(FUN_RELE, FUN_ON)
        wiringpi.digitalWrite(FOG_RELE, FOG_ON)
        wiringpi.digitalWrite(PUMP_RELE, PUMP_OFF)
    except:
        pass


def readValues():
    record = "{  " + "date: new Date(\"{}\")".format(datetime.now().strftime('%Y-%m-%dT%H:%M'))

    for s in sensors:
        try:
            s.readValue()
        except IOError:
            pass
        else:
            record += ", {}: {}".format(s.name, s.value)

    record += "  },"


def collectSensorsData():
    try:
        record = readValues()
        try:
            with open(SENSOR_DATA_FILE, "r+") as f:
                f.seek(-2, 2)
                f.write(record + "\n];")
        except IOError:
            with open(SENSOR_DATA_FILE, "w") as f:
                f.write("var chartData = [\n{}\n];".format(record))
    except:
        pass


# MAIN
wiringpi.wiringPiSetup()
for pin in [FOG_RELE, FUN_RELE, PUMP_RELE, UNUSED_RELE]:
    wiringpi.pinMode(pin, wiringpi.GPIO.OUTPUT)

pumpingCycle()

while(True):
    collectSensorsData()

    if datetime.now().minute in [0, 15, 30, 45]:
        pumpingCycle()

    sleep(60-datetime.now().second)
