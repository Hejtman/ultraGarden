import schedule, time, logging
from datetime import datetime, timedelta

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from config import SensorData, GMailAccount, LOG_LEVEL
from garden import Garden
from utils.communication import send_mail


def print_time(a='default'):
    print("From print_time", time.time(), a)


HIGH_PRIORITY = 1
LOW_PRIORITY = 2


# START SERVER
if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    logging.basicConfig(level=LOG_LEVEL, filename='/tmp/ultra_garden.log')

    garden = Garden()
    schedule.every(1).seconds.do(garden.watering).tag("WATERING").run()
    schedule.every(2).seconds.do(garden.schedule_watering)

    while True:
        schedule.run_pending()
        time.sleep(schedule.idle_seconds())


    """
    # FIXME: this stuff should be replaced by scheduler
    while True:
        now = datetime.now()
        record = _(garden.sensors.read_sensors_data)   # FIXME: each garden function should caught all its exceptions

        if now.minute % 10 == 0:
            _(garden.sensors.write_sensors_data, record, SensorData.full_file)

        garden.check_pumping(now, garden.last_pumping_time, garden.sensors)

        if now.minute == 0:
            month_of_records_count = 24*7*4
            _(garden.sensors.write_sensors_data, record, SensorData.short_file, max_records=month_of_records_count)

        if sms_gateway and (now.hour, now.minute) == (12, 00):
            # TODO: send water level info
            _(send_mail, GMailAccount.address, GMailAccount.password, sms_gateway, "I am alive")

        _(sleep(60-datetime.now().second))
    """


"""
import functools

def catch_exceptions(job_func, cancel_on_failure=False):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
            if cancel_on_failure:
                return schedule.CancelJob
    return wrapper

@catch_exceptions(cancel_on_failure=True)
def bad_task():
    return 1 / 0

schedule.every(5).minutes.do(bad_task)
"""