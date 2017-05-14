import threading
from datetime import datetime
from utils.format import td_format, td_format_short

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
        'last_change': td_format_short(now - garden.last_change),

        'fogging_count': garden.get_fogging_count(),
        'last_fogging': td_format_short(now - garden.get_last_fogging()) + " ago",
        'next_fogging': "in " + td_format_short(garden.next_fogging - now),
        'fogging_period': td_format(garden.fogging_period),

        'watering_count': garden.get_watering_count(),
        'last_watering': td_format_short(now - garden.get_last_watering()) + " ago",
        'next_watering': "in " + td_format_short(garden.next_watering - now),
        'watering_period': td_format(garden.watering_period),

        'up_time': td_format_short(now - garden.get_start_time())
    }
    for sensor in threading.garden.sensors:
        data[sensor.name] = str(sensor.value)

    return render_template('index.html', **data)
