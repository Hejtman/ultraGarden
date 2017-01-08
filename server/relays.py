from time import sleep
from itertools import chain
from collections import namedtuple

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi


RelayWiring = namedtuple('RelayWiring', 'pin off on')
RelaySets = namedtuple('RelaySet', 'fan fog pump delay')


class Relays:
    def __init__(self, fan, fog, pump: RelayWiring):
        self.relays = (fan, fog, pump)                                          # relays order has to match relays order in any _cycle

        for r in self.relays:
            wiringpi.pinMode(r.pin, wiringpi.GPIO.OUTPUT)

        self.default_set = RelaySets(fan.off, fog.off, pump.off, delay=0)        # default configuration between cycles

        self.pumping_cycle = (RelaySets(fan.off, fog.off, pump.off, delay=1),    # stabilize power for pump
                              RelaySets(fan.off, fog.off, pump.on,  delay=8),    # just pump for a while
                              RelaySets(fan.off, fog.on,  pump.off, delay=10))   # wait with fan until water level drops

    def pumping(self):
        self.cycling(chain(self.pumping_cycle, (self.default_set,)))

    def cycling(self, relay_sets):
        for relay_set in relay_sets:
            for relay, value in zip(self.relays, relay_set):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relay_set.delay)
