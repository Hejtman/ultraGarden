import time
import logging
import schedule
from datetime import datetime

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from config import SensorData, LOG_LEVEL
from garden import Garden


# START SERVER
if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    logging.basicConfig(level=LOG_LEVEL, filename='/tmp/ultra_garden.log')

    garden = Garden()
    schedule.every(1).minute.do(garden.sensors.refresh_values)
    schedule.every(10).minutes.do(garden.sensors.write_values, file=SensorData.FULL_FILE)
    schedule.every(1).hour.do(garden.sensors.write_values, file=SensorData.WEB_FILE)
    # TODO: schedule trim of WEB_FILE for month_of_records_count = 24*7*4
    # TODO: schedule sms_check with _(send_mail, GMailAccount.address, GMailAccount.password, sms_gateway, "I am alive")
    # * job.last_run = datetime(yesterday 12:00)?
    # TODO: send water level info at 12:00

    schedule.every(1).minute.do(garden.check_watering)

    garden.watering()

    # SERVER LOOP = log all, never fall
    while True:
        # noinspection PyBroadException
        try:
            schedule.run_pending()
            time.sleep(schedule.idle_seconds())

        except:
            logging.exception("Ignoring min exception:")
            failed_job = sorted(schedule.jobs)[0]
            failed_job.last_run = datetime.now()
            failed_job._schedule_next_run()
