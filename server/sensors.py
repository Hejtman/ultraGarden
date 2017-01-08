import os


class Sensors:
    def __init__(self, **sensors):
        self.sensors = (sensor for sensor in sensors.values())
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
