# TODO https://github.com/lneoe/ds18b20/blob/master/DS18B20.py


class ds18b20:
    """
    Reads from ds18b20 temperature sensor and holds temperature value from last successful reading.
    Every 1-wire sensor has an unique id which is given in initialization.
    It is possible to specify even name/description usually based on sensor's position or function.
    Reading fail is indicated by raising IOError exception.
    """
    DEVICE_DIR = "/sys/bus/w1/devices"
    DEVICE_FILE = "w1_slave"

    def __init__(self, w1id, name):
        self.w1id = w1id
        self.name = name
        self.value = 0

    def read_value(self):
        with open("{}/{}/{}".format(self.DEVICE_DIR, self.w1id, self.DEVICE_FILE), 'r') as device:
            if device.readline()[36:] == 'YES\n':
                self.value = float(device.readline()[29:])/1000
            else:
                raise IOError

# UNIT TESTS
if __name__ == '__main__':
    print("UNIT TESTS:")
    temp = ds18b20("28-011564aee4ff", "temp")
    # noinspection PyBroadException
    try:
        temp.read_value()
    except:
        print("Failed to read: {} - probably not connected".format(temp.w1id))
    else:
        print("Temperature {}: {}".format(temp.name, temp.value))

    # valid data expected
    temp.w1id = ""
    temp.DEVICE_DIR = "." 
    temp.DEVICE_FILE = "ds18b20_test_success"
    temp.read_value()
    result = "OK" if temp.value == 22.625 else "FAIL"
    print("Temperature {}: {} - {}".format(temp.name, temp.value, result))

    # invalid crc - exception expected
    temp.DEVICE_FILE = "ds18b20_test_fail"
    try:
        temp.read_value()
    except IOError:
        result = "OK"
    else:
        result = "FAIL"

    print("Temperature {}: {} - {}".format(temp.name, temp.value, result))
