import time
import logging
import smtplib
import schedule
from datetime import datetime

from config import SensorData, GMail
from garden.garden import Garden


class Gardener:
    """
    Gardener manages garden and reports.
     * Garden
       - sensors: temperature (TODO: water level, light density, ...)
       - relays: pump, fan, fogger
     * Reports
       - web server
       - sensors data log
       - sms notifications
    """
    def __init__(self):
        self.garden = Garden()

        schedule.every(1).minute.do(self.garden.sensors.refresh_values)
        schedule.every(10).minutes.do(self.garden.sensors.write_values, file=SensorData.FULL_FILE)
        schedule.every(1).hour.do(self.garden.sensors.write_values, file=SensorData.WEB_FILE)
        # TODO: schedule trim of WEB_FILE for month_of_records_count = 24*7*4
        # TODO: schedule wifi check (utils)?

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
                    Gardener.send_sms("I am alive")

                time.sleep(schedule.idle_seconds())

            except:
                logging.exception("Ignoring min exception:")
                Gardener.__recover(failed_job=sorted(schedule.jobs)[0])

    @staticmethod
    def send_sms(message):
        server = smtplib.SMTP(GMail.SERVER, GMail.PORT)
        server.starttls()
        server.login(GMail.ADDRESS, GMail.PASSWORD)
        msg = "From:{}\nTo:{}\nSubject:Garden: \n\n{}".format(GMail.ADDRESS, GMail.SMS_GATEWAY, message)
        server.sendmail(GMail.ADDRESS, GMail.SMS_GATEWAY, msg)
        server.quit()


if __name__ == '__main__':
    import unittest
    # noinspection PyUnresolvedReferences
    from gardener_test import GardenerTest

    unittest.main()
