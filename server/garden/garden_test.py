import unittest
from itertools import combinations_with_replacement

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi
    from garden.wiringpi_fake import pin_mode, pin_value

from garden.garden import Garden, RelayWiring, RelaySet


class SensorFake:
    def __init__(self, name):
        self.name = name
        self.value = None

    def read_value(self):
        self.value = 1
        return self.value


class TestGarden(unittest.TestCase):
    def __init__(self):
        self.garden = Garden()

    def test_a_that_it_turns_on_and_off_all_relays(self):
        # given
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            pin_mode.clear()
            pin_value.clear()

        unused_pin = RelayWiring(pin=1, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
        self.garden.relays += (unused_pin,)
        wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

        relays_count = len(self.garden.relays)
        all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), relays_count)
        self.garden.watering_cycle = (RelaySet((a, b, c, d), delay=3) for a, b, c, d in all_combinations)
        self.garden.default_cycle = (RelaySet((1, 1, 1, 1), delay=0),)

        # when
        self.garden.watering()

        # than
        if wiringpi.__doc__ and "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1, 1: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 1, 1: 1})

    def test_that_watering_method_set_relays(self):
        # given
        garden = Garden()
        if "Fake" in wiringpi.__doc__:
            pin_mode.clear()
            pin_value.clear()

        # when
        garden.watering()

        # than
        if "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 0})

    def test_that_it_reads_sensors_data(self):
        # given
        garden = Garden()
        garden.sensors = (SensorFake("balcony"), SensorFake("barrel"), SensorFake("tube"))

        # when
        garden.sensors_refresh()

        # then
        sensors_values = tuple(s.value for s in garden.sensors)
        self.assertEqual(sensors_values, (1, 1, 1))


if __name__ == '__main__':
    unittest.main()
