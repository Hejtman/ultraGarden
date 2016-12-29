try:
    import wiringpi
except ImportError:
    import wiringpi_fake as wiringpi


class Relays:
    def __init__(self, relays, timing):
        self.relays = relays
        self.timing = timing
        self.default_set = {"FAN": 0, "FOG": 0, "PUMP": 0, "DELAY": 0}                                # default configuration between cycles
        self.operational = {"FAN": 0, "FOG": 0, "PUMP": 1, "DELAY": 0}                                # can be remotely turned on / off
        self.PUMPING_SET = [{"FAN": 0, "FOG": 0, "PUMP": 0, "DELAY": self.timing["BEFORE_PUMP"]},     # stabilize power for pump
                            {"FAN": 0, "FOG": 0, "PUMP": 1, "DELAY": self.timing["PUMPING"]},         # just pump for a while
                            {"FAN": 0, "FOG": 1, "PUMP": 0, "DELAY": self.timing["FAN_PROTECTION"]}]  # run fan after water level drops

        for key, relay in self.relays.items():
            wiringpi.pinMode(relay["PIN"], wiringpi.GPIO.OUTPUT)

    def pumping_cycle(self):
        for configuration in self.PUMPING_SET+[self.default_set]:
            for relay in ["FAN", "FOG", "PUMP"]:
                pin = self.relays[relay]["PIN"]
                value = self.relays[relay]["ON" if configuration[relay] and self.operational[relay] else "OFF"]
                wiringpi.digitalWrite(pin, value)
            sleep(configuration["DELAY"])


# UNIT TESTS
if __name__ == '__main__':
    from time import sleep
    from ultraGarden import relays

    UNCONNECTED = 11  # GPIO pin number

    while True:
        wiringpi.digitalWrite(relays.relays["FAN"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["FOG"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["PUMP"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(relays.relays["FAN"]["PIN"], wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(relays.relays["FOG"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["PUMP"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(relays.relays["FAN"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["FOG"]["PIN"], wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(relays.relays["PUMP"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(relays.relays["FAN"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["FOG"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays.relays["PUMP"]["PIN"], wiringpi.GPIO.HIGH)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.LOW)
        sleep(5)

        wiringpi.digitalWrite(relays["FAN"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays["FOG"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(relays["PUMP"]["PIN"], wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(UNCONNECTED, wiringpi.GPIO.HIGH)
        sleep(5)
