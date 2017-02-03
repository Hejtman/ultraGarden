import threading

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
        'pump': "ON" if wiringpi.digitalRead(threading.garden.pump.pin) == threading.garden.pump.on else "OFF",
        'sensor_data': str(threading.garden.sensors)
    }
    return render_template('index.html', **data)
