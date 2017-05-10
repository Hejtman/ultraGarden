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
    now = datetime.now()
    garden = threading.garden
    data = {
        'fog': "ON" if wiringpi.digitalRead(garden.fog.pin) == garden.fog.on else "OFF",
        'fan': "ON" if wiringpi.digitalRead(garden.fan.pin) == garden.fan.on else "OFF",
        'pump': "ON" if wiringpi.digitalRead(garden.pump.pin) == garden.pump.on else "OFF",

        'status': garden.status,
        'last_change': now - garden.last_change,
        
        'last_fogging': td_format(now - garden.last_fogging) + " ago" if garden.last_fogging else "-",
        'next_fogging': "in " + td_format(garden.next_fogging - now) if garden.next_fogging else "-",
        'interval_fogging': td_format(garden.interval_fogging) if garden.interval_fogging else "-",

        'last_watering': td_format(now - garden.last_watering) + " ago" if garden.last_watering else "-",
        'next_watering': "in " + td_format(garden.next_watering - now) if garden.next_watering else "-",
        'interval_watering': td_format(garden.interval_watering) if garden.interval_watering else "-",
    }
    for sensor in threading.garden.sensors:
        data[sensor.name] = str(sensor.value)

    return render_template('index.html', **data)
