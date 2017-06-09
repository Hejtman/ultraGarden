import re
import logging
import threading
from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler

import config
import utils.sms
import utils.system
import utils.network
from garden import Garden
from records import Records
from web.web_server import web_server


# One year in minutes = greatest task period
INFINITE_MINUTES = 60*24*365

# Seconds after which will be missed tasks forgotten.
# Smaller than shortest task period so it won't buffer in scheduler.
MISFIRE_GRACE_TIME = 4*60


class Gardener:
    """
    Gardener manages garden according schedule and collected sensor data.
     * Garden - Controls HW I/O - simple stateless servant for single thread use.
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
        self.scheduler = BackgroundScheduler({
            'apscheduler.executors.default':
                {'class': 'apscheduler.executors.pool:ThreadPoolExecutor', 'max_workers': '1'}
            }
        )

    def reschedule_job(self, job_id):
        period_minutes = self.compute_period(job_id, self.garden.city_temperature.value)
        last_job_run = self.garden.get_last_job_run(job_id)
        next_job_run = max((self.get_asap_schedule(), last_job_run + timedelta(minutes=period_minutes)))
        self.scheduler.reschedule_job(job_id, trigger='cron',
                                      minute="*/{}".format(period_minutes), start_date=str(next_job_run))

    def sensors_refresh(self):
        old_temperature = self.garden.city_temperature.value
        self.garden.sensors_refresh()
        new_temperature = self.garden.city_temperature.value

        if old_temperature != new_temperature and new_temperature:
            self.reschedule_job('FOGGING')
            self.reschedule_job('WATERING')

    def send_sms_report(self):
        message = 'I am alive.'
        for sensor in self.garden.sensors:
            message += " {}:{}".format(sensor.name, str(sensor.value))
        message += " f:{}/{} w:{}/{}".format(self.get_job_period("FOGGING"),
                                             self.garden.get_job_run_count("FOGGING"),
                                             self.get_job_period("WATERING"),
                                             self.garden.get_job_run_count("WATERING"))
        utils.sms.send_sms(message)

    def working_loop(self):
        # shared cross threads
        threading.gardener = self

        # default schedule
        cron_params = {'trigger': 'cron', 'misfire_grace_time': MISFIRE_GRACE_TIME}
        self.scheduler.add_job(self.garden.watering, trigger='date')
        self.scheduler.add_job(self.garden.watering, minute='*/20', id='WATERING', **cron_params)
        self.scheduler.add_job(self.garden.fogging, minute='*/3', id='FOGGING', **cron_params)

        # sensors maintenance
        self.scheduler.add_job(self.sensors_refresh, minute='*/10', **cron_params)
        self.scheduler.add_job(self.records.write_values, minute='*/10',
                               kwargs={'file': config.SensorData.FULL_FILE}, **cron_params)
        self.scheduler.add_job(self.records.write_values, hour='*',
                               kwargs={'file': config.SensorData.WEB_FILE}, **cron_params)
        self.scheduler.add_job(self.records.trim_records, week='*',  # show on web only latest 30 days
                               kwargs={'file': config.SensorData.WEB_FILE, 'count': 24*7*4}, **cron_params)
        self.scheduler.add_job(self.send_sms_report, hour='12', **cron_params)

        # TODO: create more oxygen when high temperature via extra long pumping cycle?

        # network maintenance
        self.scheduler.add_job(utils.network.check_and_fix, hour='*',
                               kwargs={'address': config.RouterAddress, 'network': 'wlan0'}, **cron_params)
        self.scheduler.add_job(utils.system.reboot, hour='0', **cron_params)

        logging.info('Starting scheduler.')
        self.scheduler.start()

        # web server needs main thread for its signal handling
        logging.info('Starting web server.')
        web_server.run(**config.WebServer)

        self.scheduler.shutdown()

    def get_job_period(self, job_id):
        trigger = self.scheduler.get_job(job_id).trigger
        period = re.search(r"cron\[minute='\*/(\d+)'\]", str(trigger))
        return int(period.group(1)) if period else 0

    def get_job_next_run_time(self, job_id):
        return self.scheduler.get_job(job_id).next_run_time

    def start_job(self, job_id):
        # FIXME
        job = self.scheduler.get_job(job_id)

    @staticmethod
    def get_asap_schedule():
        return datetime.now() + timedelta(seconds=2)

    @staticmethod
    def compute_period(job_id, temperature):

        if job_id == 'FOGGING':
            return int(4 * 60 / (temperature - 4) ** 1.5) if 4 < temperature < 27 else INFINITE_MINUTES
        elif job_id == 'WATERING':
            return int(24 * 60 / (temperature - 4) ** 2) if 4 < temperature < 27 else INFINITE_MINUTES
        else:
            assert 0
