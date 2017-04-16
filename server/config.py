"""
Configuration storage.
"""
import logging


class SensorData:
    WEB_FILE = "/var/www/html/sensors_data_short"
    FULL_FILE = "/var/www/html/sensors_data_full"


class GMail:
    SERVER = None
    PORT = None
    ADDRESS = None
    PASSWORD = None
    SMS_GATEWAY = None


class Log:
    LEVEL = logging.INFO
    FILE = "/tmp/ultra_garden.log"


OpenWeatherMap = {
    'APPID': 'aa432246c65701ad7ab5c55d83e717b5',
    'q': 'Brno,cz',
    'units': 'metric'
}
City = "Brno"


WebServer = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False
}

