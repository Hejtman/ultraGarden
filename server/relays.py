import wiringpi
from time import sleep


class Relays:
    def __init__(self, relays, timing):
        self.relays = relays
        self.timing = timing
        self.default_set = {"FUN": 0, "FOG": 0, "PUMP": 0, "DELAY": 0}                                # default configuration between cycles
        self.operational = {"FUN": 0, "FOG": 0, "PUMP": 1, "DELAY": 0}                                # can be remotely turned on / off
        self.PUMPING_SET = [{"FUN": 0, "FOG": 0, "PUMP": 0, "DELAY": self.timing["BEFORE_PUMP"]},     # stabilize power for pump
                            {"FUN": 0, "FOG": 0, "PUMP": 1, "DELAY": self.timing["PUMPING"]},         # just pump for a while
                            {"FUN": 0, "FOG": 1, "PUMP": 0, "DELAY": self.timing["FUN_PROTECTION"]}]  # run fun after water level drops

        for key, relay in self.relays.items():
            wiringpi.pinMode(relay["PIN"], wiringpi.GPIO.OUTPUT)

    def pumping_cycle(self):
        for configuration in self.PUMPING_SET+[self.default_set]:
            for relay in ["FUN", "FOG", "PUMP"]:
                pin = self.relays[relay]["PIN"]
                value = self.relays[relay]["ON" if configuration[relay] and self.operational[relay] else "OFF"]
                wiringpi.digitalWrite(pin, value)
            sleep(configuration["DELAY"])
