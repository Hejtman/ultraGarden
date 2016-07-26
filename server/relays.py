import wiringpi
from time import sleep


PIN, ON, OFF = 0, 1, 2
FUN, FOG, PUMP = 0, 1, 2
VALUE, DELAY = 0, 1


class Relays:
    def __init__(self, relays, timing):
        self.relays = relays
        self.timing = timing
        # FORMAT:          [[[FUN, FOG, PUMP], DELAY],...]
        self.pumping_set = [[[OFF, OFF, OFF], self.timing["BEFOR_PUMP"]],     # stabilize power for pump
                            [[OFF, OFF, ON], self.timing["PUMPING"]],         # just pump for a while
                            [[OFF, ON, OFF], self.timing["FUN_PROTECTION"]],  # run fun after water level drops
                            [[ON, ON, OFF], 0]]                               # change back to normal and continue

        for key, relay in self.relays.iteritems():
            wiringpi.pinMode(relay[PIN], wiringpi.GPIO.OUTPUT)

    def pumping_cycle(self):
        pumping_set = self.pumping_set

        if True:    # TODO: connect with web-switch
            for i in range(len(pumping_set)):
                pumping_set[i][VALUE][FOG] = OFF

        try:
            for value, delay in self.pumping_set:
                for i, relay in enumerate(["FUN", "FOG", "PUMP"]):
                    wiringpi.digitalWrite(self.relays[relay][PIN], self.relays[relay][value[i]])
                sleep(delay)
        except:
            pass
