# FIXME: like sensors_test

from collections import namedtuple
from itertools import combinations_with_replacement
import unittest

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi
from wiringpi_fake import pin_mode, pin_value

from garden import Garden
from relays import RelayWiring, RelaySets


# FIXME: Should work without garden initialization?
class RelaysTest(unittest.TestCase):

    def test_that_it_runs_generic_cycle_pumping(self):
        # given
        garden = Garden()

        # when
        garden.relays.pumping()

        # then
        self.assertEqual(wiringpi.pin_mode, {23: 1, 24: 1, 25: 1})
        self.assertEqual(wiringpi.pin_value, {23: 1, 24: 1, 25: 0})

    def test_that_it_turns_on_and_off_all_relays(self):
        # given
        garden = Garden()

        unused_pin = RelayWiring(pin=18, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
        garden.relays.relays += (unused_pin,)
        wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

        all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), len(garden.relays.relays))
        testing_cycle = (RelaySets((a, b, c, d), delay=5) for a, b, c, d in all_combinations)

        # when
        garden.relays.cycling(testing_cycle)

        # than
        self.assertEqual(wiringpi.pin_mode, {23: 1, 24: 1, 25: 1, 18: 1})
        self.assertEqual(wiringpi.pin_value, {23: 1, 24: 1, 25: 1, 18: 1})


if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    unittest.main()
