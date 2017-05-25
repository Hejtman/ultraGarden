import threading
from datetime import datetime
from utils.format import td_format_shortest

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi

from flask import Flask, render_template


web_server = Flask(__name__)


@web_server.route('/')
def show():
    now = datetime.now()
    garden = threading.gardener.garden

    data = {
        'fog': "ON" if wiringpi.digitalRead(garden.fog.pin) == garden.fog.on else "OFF",
        'fan': "ON" if wiringpi.digitalRead(garden.fan.pin) == garden.fan.on else "OFF",
        'pump': "ON" if wiringpi.digitalRead(garden.pump.pin) == garden.pump.on else "OFF",

        # FIXME: better top of the log info level
        'status': garden.status,
        'last_change': td_format_shortest(now - garden.last_change),
        'up_time': td_format_shortest(now - garden.get_start_time())
    }

    for job_id in ["FOGGING", "WATERING"]:
        next_job_run_time = threading.gardener.get_job_next_run_time(job_id).replace(tzinfo=None)
        data.update({
            job_id.lower() + '_period': str(threading.gardener.get_job_period(job_id)) + "m",
            job_id.lower() + '_count': garden.get_job_run_count(job_id),
            'last_' + job_id.lower(): td_format_shortest(now - garden.get_last_job_run(job_id)) + " ago",
            'next_' + job_id.lower(): "in " + td_format_shortest(next_job_run_time - now)
        })

    for sensor in threading.gardener.garden.sensors:
        data[sensor.name] = str(sensor.value)

    return render_template('index.html', **data)
