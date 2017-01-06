import os
from collections import namedtuple

SensorsX = namedtuple('SensorsX', 'barrel_temperature balcony_temperature')  # FIXME: move inside Garden class?


class Sensors:
    def __init__(self, sensors: SensorsX):
        self.sensors = sensors

    def refresh_values(self):
        for s in self.sensors:
            try:
                s.read_value()
            except IOError:
                # TODO: log warning here
                pass

#    FIXME: not needed when named tuple
#    def get_value(self, name):
#        return filter(lambda x: x.name == name, self.sensors)[0]

    def __generate_record(self, now):
        heading = "{  " + "date: new Date(\"{}\")".format(now.strftime('%Y-%m-%dT%H:%M'))
        records = ""
        ending = "  },"

        for s in self.sensors:
            records += ", {}: {}".format(s.name, s.value)

        return heading + records + ending

    def write_values(self, now, file, max_records=0):
        tmp_file = file + "_tmp"
        last_line = "\n];"
        record = self.__generate_record(now)

        try:
            with open(file) as original, open(tmp_file, "w") as new:
                for line in original:
                    if line == last_line:
                        new.write(record)
                    new.write(line)
            os.rename(tmp_file, file)

        # file not found? start new one
        except IOError:
            with open(file, "w") as f:
                f.write("var chartData = [\n{}\n];".format(record))

# UNIT TESTS
# if __name__ == '__main__':
# TODO: sensors = Sensors(A,B,C)
# TODO: sensors.A.value = "10"
# TODO: sensors.B.value = "11"
# TODO: sensors.C.value = "12"
# TODO: sensors.write_values("/tmp/ultragarden_sensors")
# TODO: check file content with template
