from time import sleep
from collections import namedtuple

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi


RelayWiring = namedtuple('RelayWiring', 'pin off on')
RelaySets = namedtuple('RelaySet', 'fan fog pump delay')


class Relays:
    def __init__(self, fan, fog, pump: RelayWiring):
        self.relays = (fan, fog, pump)                                          # relays order has to match relays order in _cycles

        self.default_cycle = (RelaySets(fan.off, fog.off, pump.off, delay=0))    # default configuration between duty cycles

        self.pumping_cycle = (RelaySets(fan.off, fog.off, pump.off, delay=1),    # stabilize power for pump
                              RelaySets(fan.off, fog.off, pump.on,  delay=8),    # just pump for a while
                              RelaySets(fan.off, fog.on,  pump.off, delay=10))   # wait with fan for water level drops

        for r in self.relays:
            wiringpi.pinMode(r.pin, mode=wiringpi.GPIO.OUTPUT)

    def pumping(self):
        self.__cycle((self.pumping_cycle, self.default_cycle))

    def __cycle(self, relay_sets):
        for relay_set in relay_sets:
            for i, r in enumerate(self.relays):
                wiringpi.digitalWrite(r.pin, value=relay_set[i])
            sleep(relay_set.delay)


# UNIT TESTS
if __name__ == '__main__':
    from itertools import combinations_with_replacement
    from ultraGarden import relays    # GPIO initialization? import ultraGarden

    __unused_relay = RelayWiring(pin=11, off=wiringpi.GPIO.LOW, on=wiringpi.GPIO.HIGH)
    __tested_relays = relays.relays + (__unused_relay,)
    __relay_combinations = combinations_with_replacement((wiringpi.GPIO.LOW, wiringpi.GPIO.HIGH), len(__tested_relays))

    while True:
        for __relay_set in __relay_combinations:
            for __i, __relay in enumerate(__tested_relays):
                wiringpi.digitalWrite(__relay.pin, __relay_set[__i])
            sleep(5)
