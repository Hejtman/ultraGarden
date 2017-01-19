import os
import unittest
from datetime import datetime
from contextlib import suppress

from sensors import Sensors


class SensorFake:
    def __init__(self, name):
        self.name = name
        self.value = None

    def read_value(self):
        self.value = 1
        return self.value


class SensorsTest(unittest.TestCase):

    def test_that_it_reads_data_from_sensors(self):
        # given
        sensors = Sensors(balcony_tmp=SensorFake("balcony"),
                          barrel_tmp=SensorFake("barrel"),
                          tune_tmp=SensorFake("tube"))

        # when
        sensors.refresh_values()

        # then
        self.assertEqual(sensors.balcony_tmp.value, 1)
        self.assertEqual(sensors.barrel_tmp.value, 1)
        self.assertEqual(sensors.tune_tmp.value, 1)

    def test_that_it_writes_single_line_data_to_file(self):
        # given
        sensors = Sensors(a=SensorFake("aa"),
                          b=SensorFake("bb"),
                          c=SensorFake("cc"))

        sensors.a.value = 1
        sensors.b.value = 2
        sensors.c.value = 3

        test_output_file = "/tmp/ultra_garden_test_single"
        with suppress(FileNotFoundError):
            os.remove(test_output_file)

        now = datetime.now()
        expected_content = "var chartData = [\n{{  date: new Date(\"{0}\"), aa: 1, bb: 2, cc: 3  }},\n];"\
            .format(now.strftime('%Y-%m-%dT%H:%M'))

        # when
        sensors.write_values(test_output_file)

        # then
        with open(test_output_file) as f:
            self.assertEqual(f.read(), expected_content)

    def test_that_it_writes_multi_line_data_to_file(self):
        # given
        sensors = Sensors(a=SensorFake("aa"),
                          b=SensorFake("bb"),
                          c=SensorFake("cc"))

        test_output_file = "/tmp/ultra_garden_test_multi"
        with suppress(FileNotFoundError):
            os.remove(test_output_file)

        now = datetime.now()
        expected_content = """var chartData = [
{{  date: new Date("{0}"), aa: 1, bb: 2, cc: 3  }},
{{  date: new Date("{0}"), aa: 4, bb: 5, cc: 6  }},
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        # when
        for record in range(5):
            for i, s in enumerate(sensors.sensors, 1):
                s.value = len(sensors.sensors) * record + i
            sensors.write_values(test_output_file)

        # then
        with open(test_output_file) as f:
            self.assertEqual(f.read(), expected_content)

    def test_that_it_trim_data_in_file(self):
        # TODO
        pass


if __name__ == '__main__':
    unittest.main()
