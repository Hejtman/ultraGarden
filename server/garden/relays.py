import types
from collections import namedtuple
from itertools import chain
from time import sleep

try:
    import wiringpi
except (ImportError, ModuleNotFoundError):
    import garden.wiringpi_fake as wiringpi


RelayWiring = namedtuple('RelayWiring', 'pin off on')
RelaySets = namedtuple('RelaySet', 'relays delay')


class Relays:
    """
    Duty cycles.
    """
    def __init__(self, **atr):
        self.relays = tuple(wiring for name, wiring in atr.items() if not name.endswith("_cycle"))
        for variable, value in atr.items():
            setattr(self, variable, value)

        for r in self.relays:
            wiringpi.pinMode(r.pin, wiringpi.GPIO.OUTPUT)

    def cycling(self, relay_sets):
        for relay_set in relay_sets:
            for relay, value in zip(self.relays, relay_set.relays):
                wiringpi.digitalWrite(relay.pin, value)
            sleep(relay_set.delay)

    def __getattr__(self, name):
        def func(s):
            duty_cycle = eval("s.{}_cycle".format(name))
            s.cycling(chain(duty_cycle, s.default_cycle))
        return types.MethodType(func, self)
