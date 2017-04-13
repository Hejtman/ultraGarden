import logging
import threading
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from config import SensorData
from garden import Garden
from records import Records
from utils.sms import send_sms
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
        self.scheduler = BackgroundScheduler()
        # TODO: schedule wifi check (utils)? or when some data needed?

    def schedule_fogging(self):
        if self.garden.last_fogging:
            temperature = self.garden.brno_temperature.value
            if temperature and temperature > 4:
		# FIXME: different equation
                threading.next_fogging = self.garden.last_fogging + timedelta(minutes=24*60/(temperature-4)**1.5)
                self.scheduler.add_job(self.garden.fogging, 'date', threading.next_fogging, id='FOGGING',
                                       replace_existing=True, misfire_grace_time=100)
        else:
            self.scheduler.add_job(self.garden.fogging, 'date', None, id='FOGGING', replace_existing=True)
 
    def schedule_watering(self):
        # TODO: create more oxygen when high temperature (pump longer?)
        if self.garden.last_watering:
            temperature = self.garden.brno_temperature.value
            if temperature and temperature > 4:
                threading.next_watering = self.garden.last_watering + timedelta(minutes=24*60/(temperature-4)**1.5)
                self.scheduler.add_job(self.garden.watering, 'date', threading.next_watering, id='WATERING',
                                       replace_existing=True, misfire_grace_time=100)
        else:
            self.scheduler.add_job(self.garden.watering, 'date', None, id='WATERING', replace_existing=True)

    def working_loop(self):
        # shared cross threads
        threading.garden = self.garden
        threading.next_watering = None

        # FIXME: ERROR HANDLING in scheduled jobs: logging.exception("Ignoring exception from scheduled job:")
        self.scheduler.add_job(self.garden.sensors_refresh, 'cron', minute='*')
        self.scheduler.add_job(self.schedule_fogging, 'cron', minute='*')
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

# TODO: no point in making fog when temperature is up to 26C or below 5C ?
