import logging
import threading
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

import config
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
        self.scheduler = BackgroundScheduler(
            {'apscheduler.executors.default':
                {'class': 'apscheduler.executors.pool:ThreadPoolExecutor', 'max_workers': '1'}
             }
        )
        # TODO: schedule wifi check (utils)? or when some data needed?
        # TODO: schedule daily reboot

    def schedule_fogging(self):
        # TODO: no point in making fog when temperature is up to 26C or below 5C ?
        temperature = self.garden.brno_temperature.value
        if self.garden.last_fogging and temperature and temperature > 4:
            threading.next_fogging = self.garden.last_fogging + timedelta(minutes=24*60/(temperature-4)**2)
            self.scheduler.add_job(self.garden.fogging, trigger='date', next_run_time=threading.next_fogging,
                                   id='FOGGING', replace_existing=True, misfire_grace_time=100)
 
    def schedule_watering(self):
        # TODO: create more oxygen when high temperature (pump longer?)
        temperature = self.garden.brno_temperature.value
        if self.garden.last_watering and temperature and temperature > 4:
            threading.next_watering = self.garden.last_watering + timedelta(minutes=24*60/(temperature-4)**1.5)
            self.scheduler.add_job(self.garden.watering, trigger='date', next_run_time=threading.next_watering, 
                                   id='WATERING', replace_existing=True, misfire_grace_time=100)

    def working_loop(self):
        # shared cross threads
        threading.garden = self.garden
        threading.next_watering = None

        # default schedule
        cron_params = {'trigger': 'cron', 'misfire_grace_time': 100}
        self.scheduler.add_job(self.garden.watering, trigger='date')
        self.scheduler.add_job(self.garden.watering, minute='*/20', id='WATERING', **cron_params)
        self.scheduler.add_job(self.garden.fogging, minute='*/10', id='FOGGING', **cron_params)

        # weather dependent modification
        self.scheduler.add_job(self.schedule_fogging, 'cron', minute='*')
        self.scheduler.add_job(self.schedule_watering, 'cron', minute='*')

        # sensors maintenance
        self.scheduler.add_job(self.garden.sensors_refresh, 'cron', minute='*', **cron_params)
        self.scheduler.add_job(self.records.write_values, minute='*/10',
                               kwargs={'file': config.SensorData.FULL_FILE}, **cron_params)
        self.scheduler.add_job(self.records.write_values, hour='*',
                               kwargs={'file': config.SensorData.WEB_FILE}, **cron_params)
        self.scheduler.add_job(self.records.trim_records, week='*',  # show on web only latest 30 days
                               kwargs={'file': config.SensorData.WEB_FILE, 'count': 24*7*4}, **cron_params)

        # TODO: add water level info
        self.scheduler.add_job(send_sms, hour='*/12', kwargs={'message': 'I am alive'}, **cron_params)

        logging.info('Starting scheduler.')
        self.scheduler.start()

        # web server needs main thread for its signal handling
        logging.info('Starting web server.')
        web_server.run(**config.WebServer)

        self.scheduler.shutdown()
