import time
import logging
import schedule
from datetime import datetime

from config import SensorData
from garden.garden import Garden
from records.sms import send_sms
from records.records import Records


class Gardener:
    """
    Gardener manages garden according collected sensor data.
     * Garden - Controls HW I/O.
       * sensors: temperature (TODO: water level, light density, ...)
       * relays: pump, fan, fogger
     * Records - Collects and store sensors data + current garden state.
       * web server
         * light version of sensor data history
         * current garden state (TODO)
         * next planned maintenance action (TODO)
       * full sensors data log
       * sms notifications (TODO: alerts)
    """
    def __init__(self):
        self.garden = Garden()
        self.records = Records(sensors=self.garden.sensors)

        schedule.every(1).minute.do(self.garden.sensors_refresh)
        schedule.every(10).minutes.do(self.records.write_values(SensorData.FULL_FILE))
        schedule.every(1).hour.do(self.records.write_values(SensorData.WEB_FILE))
        schedule.every(1).week.do(self.records.trim_records(SensorData.WEB_FILE, count=24 * 7 * 4))    # only last month
        # TODO: schedule wifi check (utils)? or when some data needed?

        schedule.every(1).minute.do(self.garden.check_watering).run()

    @staticmethod
    def __recover(failed_job):
        failed_job.last_run = datetime.now()
        failed_job._schedule_next_run()

    @staticmethod
    def working_loop():
        """
        Server main working loop. Logs all, never falls.
        """
        while True:
            # noinspection PyBroadException
            try:
                schedule.run_pending()

                # FIXME: use other scheduler? This depends on timing and can be missed
                # TODO: add water level info
                now = datetime.now()
                if (now.hour, now.minute) == (12, 00):
                    send_sms("I am alive")

                time.sleep(schedule.idle_seconds())

            except:
                logging.exception("Ignoring min exception:")
                Gardener.__recover(failed_job=sorted(schedule.jobs)[0])
