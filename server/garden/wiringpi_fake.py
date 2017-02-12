"""
Fake GPIO interface for debugging on non-raspberry pi platforms.
"""


class GPIO(object):
    WPI_MODE_PINS = 0
    WPI_MODE_GPIO = 1
    WPI_MODE_GPIO_SYS = 2
    WPI_MODE_PHYS = 3
    WPI_MODE_PIFACE = 4
    WPI_MODE_UNINITIALISED = -1

    INPUT = 0
    OUTPUT = 1
    PWM_OUTPUT = 2
    GPIO_CLOCK = 3

    LOW = 0
    HIGH = 1

    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2

    PWM_MODE_MS = 0
    PWM_MODE_BAL = 1

    INT_EDGE_SETUP = 0
    INT_EDGE_FALLING = 1
    INT_EDGE_RISING = 2
    INT_EDGE_BOTH = 3

    LSBFIRST = 0
    MSBFIRST = 1

    MODE = 0


pin_mode = ["INPUT"]*40
pin_value = [0]*40


def wiringPiSetup():
    print("wiringPiSetup")


def pinMode(pin, mode):
    pin_mode[pin] = mode
    print("pin {} set to {}".format(pin, ["INPUT", "OUTPUT", "PWM_OUTPUT", "GPIO_CLOCK"][mode]))


def digitalWrite(pin, value):
    pin_value[pin] = value
    print("pin {} set to {}".format(pin, value))


def digitalRead(pin):
    return pin_value[pin]
