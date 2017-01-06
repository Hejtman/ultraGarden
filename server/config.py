import logging


class SensorData:
    short_file = "/var/www/html/sensors_data_short"
    full_file = "/var/www/html/sensors_data_full"


class GMailAccount:
    address = None
    password = None


sms_gateway = None
log_level = logging.INFO
