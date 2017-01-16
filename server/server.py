import time
import logging
import schedule
from datetime import datetime

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from config import SensorData, Log
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
        # TODO: schedule sms_check with send_mail, GMailAccount.address, GMailAccount.password, sms_gateway,"I am alive"
        # * job.last_run = datetime(yesterday 12:00)?
        # TODO: send water level info at 12:00

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
                time.sleep(schedule.idle_seconds())

            except:
                logging.exception("Ignoring min exception:")
                Gardener.__recover(failed_job=sorted(schedule.jobs)[0])

                # FIXME:
                import traceback
                traceback.print_exc()


# START SERVER
if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    logging.basicConfig(level=Log.LEVEL, filename=Log.FILE)

    Gardener().working_loop()
