import os
import shutil
from datetime import datetime


class Records:
    """
     * Collects and store sensors data + current garden state.
       * sensors data log + current garden state
       * web server
         * light version of sensor data history
         * current garden state (TODO)
         * next planned maintenance action (TODO)
       * sms notifications (TODO: alerts)
    """
    def __init__(self, sensors):
        self.sensors = sensors

    def __generate_record(self):
        heading = "{  " + "date: new Date(\"{}\")".format(datetime.now().strftime('%Y-%m-%dT%H:%M'))
        records = ""
        ending = "  },"

        for s in self.sensors:
            records += ", {}: {}".format(s.name, s.value)

        return heading + records + ending

    def write_values(self, file):
        # FIXME: write only valid values and write only record with at least one valid value
        heading = "var chartData = ["
        record = self.__generate_record()
        ending = "];"
        try:
            with open(file, "br+") as f:
                f.seek(-len(ending), os.SEEK_END)
                f.write((record + os.linesep + ending).encode("ascii"))
        except IOError:
            with open(file, "w") as f:
                f.write(heading + os.linesep + record + os.linesep + ending)

    @staticmethod
    def trim_records(file, count):
        with open(file, "r") as original, open(file + ".tmp", "w") as trimmed:
            trimmed.write(original.readline())                      # first line
            trimmed.writelines(original.readlines()[-count-1:])     # last line + count records above
        shutil.move(file + ".tmp", file)
