import logging


class SensorData:
    WEB_FILE = "/var/www/html/sensors_data_short"
    FULL_FILE = "/var/www/html/sensors_data_full"


class GMailAccount:
    ADDRESS = None
    PASSWORD = None
    SMS_GATEWAY = None


class Log:
    LEVEL = logging.INFO
    FILE = "/tmp/ultra_garden.log"
