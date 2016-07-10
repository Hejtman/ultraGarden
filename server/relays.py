import wiringpi
from time import sleep


PIN, ON, OFF = 0, 1, 2


class Relays:
    def __init__(self, relays, timing):
        self.relays = relays
        self.timing = timing

        for key,relay in self.relays.iteritems():    
            wiringpi.pinMode(relay[PIN], wiringpi.GPIO.OUTPUT)

    def pumping_cycle(self):
        try:
            for value, time in [[[OFF, OFF, ON], self.timing["PUMPING"]],         # just pump for a while
                                [[OFF, ON, OFF], self.timing["FUN_PROTECTION"]],  # run fun after water level drops
                                [[ON, ON, OFF], 0]]:                              # change back to normal and continue
                for i, relay in enumerate(["FUN", "FOG", "PUMP"]):
                    wiringpi.digitalWrite(self.relays[relay][PIN], self.relays[relay][value[i]])
                sleep(time)
        except:
            pass
