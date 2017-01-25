import unittest
from itertools import combinations_with_replacement

try:
    import wiringpi
except ImportError:
    import garden.wiringpi_fake as wiringpi
    from garden.wiringpi_fake import pin_mode, pin_value

from garden.garden import Garden
from garden.relays import RelayWiring, RelaySets


# FIXME: Should work without garden initialization?
class TestRelays(unittest.TestCase):

    def _test_a_that_it_turns_on_and_off_all_relays(self):
        # given
        garden = Garden()

        unused_pin = RelayWiring(pin=1, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
        garden.relays.relays += (unused_pin,)
        wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

        relays_count = len(garden.relays.relays)
        all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), relays_count)
        testing_cycle = (RelaySets((a, b, c, d), delay=3) for a, b, c, d in all_combinations)

        # when
        garden.relays.cycling(testing_cycle)

        # than
        if "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1, 1: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 1, 1: 1})

    def test_that_it_runs_generic_cycle_pumping(self):
        # given
        garden = Garden()

        # when
        garden.relays.pumping()

        # then
        if "Fake" in wiringpi.__doc__:
            self.assertEqual(pin_mode, {6: 1, 5: 1, 4: 1})
            self.assertEqual(pin_value, {6: 1, 5: 1, 4: 0})


if __name__ == '__main__':
    wiringpi.wiringPiSetup()
    unittest.main()
