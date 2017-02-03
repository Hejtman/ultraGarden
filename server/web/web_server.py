import threading
from flask import Flask, render_template


web_server = Flask(__name__)


@web_server.route('/')
def show():
    data = {
        'sensor_data': str(threading.garden.sensors)
    }
    return render_template('index.html', **data)
