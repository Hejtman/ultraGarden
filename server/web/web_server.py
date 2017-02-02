from flask import Flask, render_template

app = Flask(__name__)


class WebServer:
    @app.route('/')
    def index():
        data = {
            'sensor_data': "bbb"
        }
        return render_template('index.html', **data)

    @staticmethod
    def run():
        # FIXME: this manages to initialize WIRINGPI twice
        # FIXME: handle exceptions
        app.run(host='0.0.0.0', port=5000, debug=True)
