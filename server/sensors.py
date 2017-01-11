import os


class Sensors:
    def __init__(self, **sensors):
        self.sensors = tuple(s for s in sensors.values())
        for name, data in sensors.items():
            setattr(self, name, data)

    def refresh_values(self):
        for s in self.sensors:
            try:
                s.read_value()
            except IOError:
                # TODO: log warning here
                pass

    def __generate_record(self, now):
        heading = "{  " + "date: new Date(\"{}\")".format(now.strftime('%Y-%m-%dT%H:%M'))
        records = ""
        ending = "  },"

        for s in self.sensors:
            records += ", {}: {}".format(s.name, s.value)

        return heading + records + ending

    def write_values(self, now, file):
        heading = "var chartData = ["
        record = self.__generate_record(now)
        ending = "];"
        try:
            with open(file, "br+") as f:
                f.seek(-len(ending), os.SEEK_END)
                f.write((record + os.linesep + ending).encode("ascii"))
        except IOError:
            with open(file, "w") as f:
                f.write(heading + os.linesep + record + os.linesep + ending)


if __name__ == '__main__':
    import unittest
    # noinspection PyUnresolvedReferences
    from sensors_test import TestSensors

    unittest.main()
