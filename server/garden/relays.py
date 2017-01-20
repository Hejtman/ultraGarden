from time import sleep
from itertools import chain
from collections import namedtuple
import types

try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi


RelayWiring = namedtuple('RelayWiring', 'pin off on')
RelaySets = namedtuple('RelaySet', 'relays delay')


class Relays:
    """
    Duty cycles.
    """
    def __init__(self, **relays):
        self.relays = tuple(s for s in relays.values())
        for variable, value in relays.items():
            setattr(self, variable, value)

        for r in self.relays:
            wiringpi.pinMode(r.pin, wiringpi.GPIO.OUTPUT)

        # FIXME: move this to garden?
        # stabilize power for pump ; pump for a while ; wait with fan until water level drops
        self.pumping_cycle = (RelaySets(relays=(self.fan.off, self.fog.off, self.pump.off), delay=1),
                              RelaySets(relays=(self.fan.off, self.fog.off, self.pump.on), delay=8),
                              RelaySets(relays=(self.fan.off, self.fog.on,  self.pump.off), delay=10))

        # default relays configuration between cycles
        self.default_set = RelaySets(relays=(self.fan.off, self.fog.off, self.pump.off), delay=0)

    def __getattr__(self, name):
        def func(self):
            duty_cycle = eval("self.{}_cycle".format(name))
            self.cycling(chain(duty_cycle, (self.default_set,)))
        return types.MethodType(func, self)

    def cycling(self, relay_sets):
        for relay_set in relay_sets:
            for relay, value in zip(self.relays, relay_set.relays):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relay_set.delay)
