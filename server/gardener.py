import logging
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from config import SensorData, OpenWeatherMapConf
from garden.garden import Garden
from records.records import Records
from utils.sms import send_sms
from utils.weather import Weather
from web.web_server import web_server


class Gardener:
    """
    Gardener manages garden according schedule and collected sensor data.
     * Garden - Controls HW I/O.
       * sensors: temperature (TODO: water level, light density, ...)
       * relays: pump, fan, fogger
     * Records - Via scheduler collects and store sensors data + current garden state.

     * Web server shows
       * current garden state (TODO)
       * light version of sensor data history
       * next planned maintenance action (TODO)
       * buttons for manipulation with garden
    """
    def __init__(self):
        self.garden = Garden()
        self.records = Records(sensors=self.garden.sensors)
        self.weather = Weather(OpenWeatherMapConf)
        self.scheduler = BackgroundScheduler()
        # TODO: weather integrate with records
        # TODO: refresh weather

        # TODO: schedule wifi check (utils)? or when some data needed?

    def schedule_watering(self):
        # FIXME: base calculation on sensor data [minutes = 60*24*365 if c < 5 else 24*60/(x-4)**1.5]
        # TODO: create more oxygen when high temperature (pump longer?)
        # TODO: no point in making fog when temperature is up to 26C or below 5C ?
        if datetime.now() - self.garden.last_watering_time > timedelta(minutes=20):
            self.garden.watering()
        # self.scheduler.add_job(watering, 'date', time, id='watering', replace_existing=True)

    def working_loop(self):
        # shared cross threads
        threading.garden = self.garden

        # FIXME: ERROR HANDLING in scheduled jobs: logging.exception("Ignoring exception from scheduled job:")
        self.scheduler.add_job(self.garden.sensors_refresh, 'cron', minute='*')
        self.scheduler.add_job(self.schedule_watering, 'date', run_date=None)
        self.scheduler.add_job(self.schedule_watering, 'cron', minute='*')
        self.scheduler.add_job(self.records.write_values, 'cron', minute='*/10', kwargs={'file': SensorData.FULL_FILE})
        self.scheduler.add_job(self.records.write_values, 'cron', hour='*', kwargs={'file': SensorData.WEB_FILE})
        # TODO: add water level info
        self.scheduler.add_job(send_sms, trigger='cron', hour='*/12', kwargs={'message': 'I am alive'})
        self.scheduler.add_job(self.records.trim_records, 'cron', week='*',
                               kwargs={'file': SensorData.WEB_FILE, 'count': 24*7*4})  # keep only last month
        logging.info('Starting scheduler.')
        self.scheduler.start()

        # web server needs main thread for its signal handling
        logging.info('Starting web server.')
        web_server.run(host='0.0.0.0', port=5000, debug=False)

        self.scheduler.shutdown()
