import os
import unittest
from datetime import datetime
from contextlib import suppress

from records import Records
from garden.test import SensorFake


class TestReports(unittest.TestCase):
    def test_that_it_writes_single_line_data_to_file(self):
        # given
        records = Records((SensorFake("aa"),
                           SensorFake("bb"),
                           SensorFake("cc")))

        for i, s in enumerate(records.sensors, 1):
            s.value = i

        test_output_file = "/tmp/ultra_garden_test_single"
        with suppress(FileNotFoundError):
            os.remove(test_output_file)

        now = datetime.now()
        expected_content = "var chartData = [\n{{  date: new Date(\"{0}\"), aa: 1, bb: 2, cc: 3  }},\n];" \
            .format(now.strftime('%Y-%m-%dT%H:%M'))

        # when
        records.write_values(test_output_file)

        # then
        with open(test_output_file) as f:
            self.assertEqual(expected_content, f.read())

    def test_that_it_writes_multi_line_data_to_file(self):
        # given
        records = Records((SensorFake("aa"),
                           SensorFake("bb"),
                           SensorFake("cc")))

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
            for i, s in enumerate(records.sensors, 1):
                s.value = len(records.sensors) * record + i
            records.write_values(test_output_file)

        # then
        with open(test_output_file) as f:
            self.assertEqual(expected_content, f.read())

    def test_that_it_trims_records_from_5_to_3_lines(self):
        # given
        now = datetime.now()
        content = """var chartData = [
{{  date: new Date("{0}"), aa: 1, bb: 2, cc: 3  }},
{{  date: new Date("{0}"), aa: 4, bb: 5, cc: 6  }},
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        expected_content = """var chartData = [
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        test_output_file = "/tmp/ultra_garden_test_trim53"
        with open(test_output_file, "w") as f:
            f.write(content)

        # when
        Records.trim_records(test_output_file, 3)

        # then
        with open(test_output_file) as f:
            self.assertEqual(expected_content, f.read())

    def test_that_it_trims_records_from_5_to_1_line(self):
        # given
        now = datetime.now()
        content = """var chartData = [
{{  date: new Date("{0}"), aa: 1, bb: 2, cc: 3  }},
{{  date: new Date("{0}"), aa: 4, bb: 5, cc: 6  }},
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        expected_content = """var chartData = [
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        test_output_file = "/tmp/ultra_garden_test_trim51"
        with open(test_output_file, "w") as f:
            f.write(content)

        # when
        Records.trim_records(test_output_file, 1)

        # then
        with open(test_output_file) as f:
            self.assertEqual(expected_content, f.read())

    def test_that_it_trims_records_from_5_to_6_line(self):
        # given
        now = datetime.now()
        content = """var chartData = [
{{  date: new Date("{0}"), aa: 1, bb: 2, cc: 3  }},
{{  date: new Date("{0}"), aa: 4, bb: 5, cc: 6  }},
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        expected_content = """var chartData = [
{{  date: new Date("{0}"), aa: 1, bb: 2, cc: 3  }},
{{  date: new Date("{0}"), aa: 4, bb: 5, cc: 6  }},
{{  date: new Date("{0}"), aa: 7, bb: 8, cc: 9  }},
{{  date: new Date("{0}"), aa: 10, bb: 11, cc: 12  }},
{{  date: new Date("{0}"), aa: 13, bb: 14, cc: 15  }},
];""".format(now.strftime('%Y-%m-%dT%H:%M'))

        test_output_file = "/tmp/ultra_garden_test_trim51"
        with open(test_output_file, "w") as f:
            f.write(content)

        # when
        Records.trim_records(test_output_file, 6)

        # then
        with open(test_output_file) as f:
            self.assertEqual(expected_content, f.read())


if __name__ == '__main__':
    unittest.main()
