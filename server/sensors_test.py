import os
import unittest
from contextlib import ignored

from sensors import Sensors
from datetime import datetime


class SensorFake:
    def __init__(self, name):
        self.name = name
        self.value = None

    def read_value(self):
        self.value = 1
        return self.value


class TestSensors(unittest.TestCase):

    def test_that_it_reads_data(self):
        sensors = Sensors(balcony_tmp=SensorFake("balcony"),
                          barrel_tmp=SensorFake("barrel"),
                          tune_tmp=SensorFake("tube"))

        sensors.refresh_values()

        self.assertEqual(sensors.balcony_tmp.value, 1)
        self.assertEqual(sensors.barrel_tmp.value, 1)
        self.assertEqual(sensors.tune_tmp.value, 1)

    def test_that_it_writes_data_to_file(self):
        # given
        now = datetime.now()
        expected_content = """var chartData = [
        {{  date: new Date("{0}"), aa: 2, bb: 3, cc: 4  }},
        ];""".format(now.strftime('%Y-%m-%dT%H:%M'))
        test_output_file = "/tmp/ultra_garden_test"
        with ignored(OSError):
            os.remove(test_output_file)

        sensors = Sensors(a=SensorFake("aa"),
                          b=SensorFake("bb"),
                          c=SensorFake("cc"))

        # when
        sensors.a.value = 2
        sensors.b.value = 3
        sensors.c.value = 4
        sensors.write_values(now, test_output_file)

        for record in range(1,5):
            for i, s in enumerate(sensors.sensors):
                s.value = record + i
            sensors.write_values(now, test_output_file)

        # then
        with open(test_output_file) as f:
            self.assertEqual(f.read(), expected_content)

        os.remove(test_output_file)

    def test_that_it_trim_data_in_file(self):
        pass


if __name__ == '__main__':
    unittest.main()
