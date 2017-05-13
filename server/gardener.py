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
        self.scheduler = BackgroundScheduler({
            'apscheduler.executors.default':
                {'class': 'apscheduler.executors.pool:ThreadPoolExecutor', 'max_workers': '1'}
            }
        )

    def schedule_fogging(self):
        temperature = self.garden.brno_temperature.value
        if not temperature:
            return

        period_minutes = self.compute_fogging_period(temperature)
        fogging_period = timedelta(minutes=period_minutes)
        if fogging_period == self.garden.fogging_period:
            return

        self.garden.fogging_period = fogging_period
        self.garden.next_fogging = max((self.get_asap_schedule(), self.garden.get_last_fogging() + fogging_period))

        self.scheduler.add_job(self.garden.fogging, start_date=str(self.garden.next_fogging),
                               trigger='cron', minute="*/{}".format(period_minutes),
                               id='FOGGING', replace_existing=True, misfire_grace_time=MISFIRE_GRACE_TIME)

    def schedule_watering(self):
        temperature = self.garden.brno_temperature.value
        if not temperature:
            return

        period_minutes = self.compute_watering_period(temperature)
        watering_period = timedelta(minutes=period_minutes)
        if watering_period == self.garden.watering_period:
            return

        self.garden.watering_period = watering_period
        self.garden.next_watering = max((self.get_asap_schedule(), self.garden.get_last_watering() + watering_period))

        self.scheduler.add_job(self.garden.watering, start_date=str(self.garden.next_watering),
                               trigger='cron', minute="*/{}".format(period_minutes),
                               id='WATERING', replace_existing=True, misfire_grace_time=MISFIRE_GRACE_TIME)

    def send_sms_report(self):
        message = 'I am alive.'
        for sensor in self.garden.sensors:
            message += " {}:{}".format(sensor.name, str(sensor.value))
        utils.sms.send_sms(message)

    def working_loop(self):
        # shared cross threads
        threading.garden = self.garden

        # default schedule
        cron_params = {'trigger': 'cron', 'misfire_grace_time': MISFIRE_GRACE_TIME}
        self.scheduler.add_job(self.garden.watering, trigger='date')
        self.scheduler.add_job(self.garden.watering, minute='*/20', id='WATERING', **cron_params)
        self.scheduler.add_job(self.garden.fogging, minute='*/3', id='FOGGING', **cron_params)

        # sensors maintenance
        self.scheduler.add_job(self.garden.sensors_refresh, minute='*/10', **cron_params)
        self.scheduler.add_job(self.records.write_values, minute='*/10',
                               kwargs={'file': config.SensorData.FULL_FILE}, **cron_params)
        self.scheduler.add_job(self.records.write_values, hour='*',
                               kwargs={'file': config.SensorData.WEB_FILE}, **cron_params)
        self.scheduler.add_job(self.records.trim_records, week='*',  # show on web only latest 30 days
                               kwargs={'file': config.SensorData.WEB_FILE, 'count': 24*7*4}, **cron_params)
        self.scheduler.add_job(self.send_sms_report, hour='12', **cron_params)

        # sensors/weather dependent modification
        self.scheduler.add_job(self.schedule_fogging, minute='*/10', **cron_params)
        self.scheduler.add_job(self.schedule_watering, minute='*/10', **cron_params)
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

    @staticmethod
    def get_asap_schedule():
        return datetime.now() + timedelta(seconds=2)

    @staticmethod
    def compute_fogging_period(temperature):
        return int(4 * 60 / (temperature - 4) ** 1.5) if 4 < temperature < 27 else INFINITE_MINUTES

    @staticmethod
    def compute_watering_period(temperature):
        return int(24 * 60 / (temperature - 4) ** 2) if 4 < temperature < 27 else INFINITE_MINUTES
