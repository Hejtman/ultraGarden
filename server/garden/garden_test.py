import unittest
from itertools import combinations_with_replacement

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi
    from garden.wiringpi_fake import pin_mode, pin_value

from garden.garden import Garden, RelayWiring, RelaySet


class TestGarden(unittest.TestCase):

    def test_a_that_it_turns_on_and_off_all_relays(self):
        # given
        pin_mode.clear()
        pin_value.clear()
        garden = Garden()

        unused_pin = RelayWiring(pin=1, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
        garden.relays += (unused_pin,)
        wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

        relays_count = len(garden.relays)
        all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), relays_count)
        garden.watering_cycle = (RelaySet((a, b, c, d), delay=3) for a, b, c, d in all_combinations)
        garden.default_cycle = (RelaySet((1, 1, 1, 1), delay=0),)

        # when
        garden.watering()

        # than
        if "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1, 1: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 1, 1: 1})

    def test_that_watering_method_set_relays(self):
        # given
        pin_mode.clear()
        pin_value.clear()
        garden = Garden()

        # when
        garden.watering()

        # than
        if "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 0})


if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    unittest.main()


