import threading
from datetime import datetime
from utils.format import td_format

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi

from flask import Flask, render_template


web_server = Flask(__name__)


@web_server.route('/')
def show():
    data = {
        'fog': "ON" if wiringpi.digitalRead(threading.garden.fog.pin) == threading.garden.fog.on else "OFF",
        'fan': "ON" if wiringpi.digitalRead(threading.garden.fan.pin) == threading.garden.fan.on else "OFF",
        'pump': "ON" if wiringpi.digitalRead(threading.garden.pump.pin) == threading.garden.pump.on else "OFF"
    }
    for sensor in threading.garden.sensors:
        data[sensor.name] = str(sensor.value)

    now = datetime.now()
    last_watering = threading.garden.last_watering
    next_watering = threading.next_watering
    data['last_watering'] = "-" if last_watering is None else td_format(now - last_watering) + " ago"
    data['next_watering'] = "-" if next_watering is None else "in " + td_format(next_watering - now)

    return render_template('index.html', **data)
