import os
from datetime import datetime


class Sensors:
    def __init__(self, sensor_list):
        self.sensors = sensor_list

    def read_sensors_data(self):
        try:
            record = "{  " + "date: new Date(\"{}\")".format(datetime.now().strftime('%Y-%m-%dT%H:%M'))

            for s in self.sensors:
                try:
                    s.readValue()
                except IOError:
                    pass
                else:
                    record += ", {}: {}".format(s.name, s.value)

            record += "  },"
            return record
        except:
            pass

    @staticmethod
    def write_sensors_data(record, record_file, max_records=0):
        try:
            try:
                with open(record_file) as f1:
                    # APPEND: overwrite closing line with record and new closing line
                    data = f1.read().splitlines()
                    data[-1] = record + '\n];'

                    # TRIM OLDEST: overwrite opening line and top record(s) by new opening
                    if max_records and max_records+1 < len(data):
                        data = data[len(data)-max_records-1:]
                        data[0] = "var chartData = ["

                    with open(record_file + "_tmp", 'w') as f2:
                        f2.write('\n'.join(data))

                os.rename(record_file + "_tmp", record_file)

            except IOError:
                with open(record_file, "w") as f:
                    f.write("var chartData = [\n{}\n];".format(record))

        except:
            pass


# UNIT TESTS
if __name__ == '__main__':
    Sensors.write_sensors_data('    record1', "test_file", 3)
    Sensors.write_sensors_data('    record2', "test_file", 3)
    Sensors.write_sensors_data('    record3', "test_file", 3)
    Sensors.write_sensors_data('    record4', "test_file", 3)
    Sensors.write_sensors_data('    record5', "test_file", 3)
