import logging
import threading
from apscheduler.schedulers.background import BackgroundScheduler

from config import SensorData
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
        self.weather = Weather()

        # TODO: weather integrate with records
        # TODO: refresh weather

        # TODO: schedule wifi check (utils)? or when some data needed?

    def working_loop(self):
        # shared cross threads
        threading.garden = self.garden

        scheduler = BackgroundScheduler()
        # FIXME: ERROR HANDLING in scheduled jobs: logging.exception("Ignoring exception from scheduled job:")
        scheduler.add_job(self.garden.sensors_refresh, 'cron', minute='*')
        scheduler.add_job(self.garden.schedule_watering, 'date', run_date=None, kwargs={'scheduler': scheduler})
        scheduler.add_job(self.garden.schedule_watering, 'cron', minute='*', kwargs={'scheduler': scheduler})
        scheduler.add_job(self.records.write_values, 'cron', minute='*/10', kwargs={'file': SensorData.FULL_FILE})
        scheduler.add_job(self.records.write_values, 'cron', hour='*', kwargs={'file': SensorData.WEB_FILE})
        # TODO: add water level info
        scheduler.add_job(send_sms, trigger='cron', hour='*/12', kwargs={'message': 'I am alive'})
        scheduler.add_job(self.records.trim_records, 'cron', week='*', kwargs={'file': SensorData.WEB_FILE,
                                                                               'count': 24*7*4})  # keep only last month
        logging.info('Starting scheduler.')
        scheduler.start()

        # web server needs main thread for its signal handling
        logging.info('Starting web server.')
        web_server.run(host='0.0.0.0', port=5000, debug=False)

        scheduler.shutdown()
