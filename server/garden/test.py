import unittest
from itertools import combinations_with_replacement

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi

from garden import Garden, RelayWiring, RelaySet


class SensorFake:
    def __init__(self, name):
        self.name = name
        self.value = None

    def read_value(self):
        self.value = 1
        return self.value

garden = Garden()


class TestGarden(unittest.TestCase):
    def setUp(self):
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            wiringpi.pin_mode = [wiringpi.GPIO.INPUT] * 40
            wiringpi.pin_value = [0] * 40
            wiringpi.pin_mode_history = []
            wiringpi.pin_value_history = []

    def test_a_that_fogging_method_set_relays(self):
        # when
        garden.fogging()

        # than
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            self.assertEqual(wiringpi.pin_value_history, ['27:1', '28:0', '29:0',   # fun off, fog on, pump off
                                                          '27:0', '28:0', '29:0',   # fun on, fog on, pump off
                                                          '27:0', '28:1', '29:0',   # fun on, fog off, pump off
                                                          '27:1', '28:1', '29:0'])  # default

    def test_b_that_watering_method_set_relays(self):
        # when
        garden.watering()

        # than
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            self.assertEqual(wiringpi.pin_value_history, ['27:1', '28:1', '29:1',   # fun off, fog off, pump on
                                                          '27:1', '28:1', '29:0',   # fun off, fog off, pump off
                                                          '27:1', '28:1', '29:0'])  # again with default

    # Overwrites garden duty cycles! Only as last relay test.
    def test_z_that_it_turns_on_all_relays(self):
        # given
        unused_pin = RelayWiring(pin=26, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
        garden.relays = (unused_pin,) + garden.relays
        wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

        relays_count = len(garden.relays)
        all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), relays_count)
        garden.watering_cycle = (RelaySet((a, b, c, d), delay=3) for a, b, c, d in all_combinations)
        garden.default_cycle = (RelaySet((1, 1, 1, 1), delay=0),)

        # when
        garden.watering()

        # than
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            self.assertEqual(wiringpi.pin_value_history, ["26:0", "27:0", "28:0", "29:0",
                                                          "26:0", "27:0", "28:0", "29:1",
                                                          "26:0", "27:0", "28:1", "29:1",
                                                          "26:0", "27:1", "28:1", "29:1",
                                                          "26:1", "27:1", "28:1", "29:1",
                                                          "26:1", "27:1", "28:1", "29:1"])

    def test_that_it_reads_sensors_data(self):
        # given
        garden.sensors = (SensorFake("balcony"), SensorFake("barrel"), SensorFake("tube"))

        # when
        garden.sensors_refresh()

        # then
        sensors_values = tuple(s.value for s in garden.sensors)
        self.assertEqual(sensors_values, (1, 1, 1))


if __name__ == '__main__':
    unittest.main()
