import threading
from datetime import datetime
from contextlib import suppress
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

    with suppress(AttributeError):
        last_fogging = threading.garden.last_fogging
        data['last_fogging'] = "-" if last_fogging is None else td_format(now - last_fogging) + " ago"

    with suppress(AttributeError):
        next_fogging = threading.next_fogging
        data['next_fogging'] = "-" if next_fogging is None else "in " + td_format(next_fogging - now)

    with suppress(AttributeError):
        last_watering = threading.garden.last_watering
        data['last_watering'] = "-" if last_watering is None else td_format(now - last_watering) + " ago"

    with suppress(AttributeError):
        next_watering = threading.next_watering
        data['next_watering'] = "-" if next_watering is None else "in " + td_format(next_watering - now)

    with suppress(AttributeError):
        data['status'] = threading.status

    return render_template('index.html', **data)
