# FIXME: like sensors_test

from collections import namedtuple
from itertools import combinations_with_replacement

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi

from garden import Garden
from relays import RelayWiring


def test_that_it_turns_on_and_off_all_relays():
    RelaySetsFull = namedtuple('RelaySetFull', 'fan fog pump unused delay')

    garden = Garden()

    unused_pin = RelayWiring(pin=18, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
    garden.relays.relays += (unused_pin,)
    wiringpi.pinMode(unused_pin.pin, wiringpi.GPIO.OUTPUT)

    all_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), len(garden.relays.relays))
    testing_cycle = (RelaySetsFull(a, b, c, d, delay=5) for a, b, c, d in all_combinations)

    garden.relays.cycling(testing_cycle)


if __name__ == '__main__':
    wiringpi.wiringPiSetup()

    while True:
        test_that_it_turns_on_and_off_all_relays()
