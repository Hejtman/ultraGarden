import requests


class Weather:
    # datetime.fromtimestamp(['dt']).strftime('%Y-%m-%d %H:%M:%S')
    def __init__(self, params):
        self.params = "&".join("{}={}".format(key, value) for key, value in params.items())

    def get_weather(self):
        # self.value['main']['temp_min', 'temp', 'temp_max', 'humidity']
        return requests.get("http://api.openweathermap.org/data/2.5/weather?" + self.params).json()

    def get_forecast(self):
        # [?]['main']['temp_min', 'temp', 'temp_max', 'humidity','dt']
        return requests.get("http://api.openweathermap.org/data/2.5/forecast?" + self.params).json()['list']


class WeatherSensor(Weather):
    def __init__(self, key, name, args):
        Weather.__init__(self, args)
        self.name = name
        self.key = key
        self.value = None

    def read_value(self):
        w = self.get_weather()
        if w:
            self.value = w['main'][self.key]


# UNIT TESTS:
if __name__ == '__main__':
    PARAMS = {
        'APPID': 'aa432246c65701ad7ab5c55d83e717b5',
        'q': 'Brno,cz',
        'units': 'metric'
    }
    weather = Weather(PARAMS)
    assert(weather.get_weather()['name'] == 'Brno')
    assert(weather.get_weather()['name'] == 'Brno')

    temperature = WeatherSensor('temp', 'Brno temperature', PARAMS)
    temperature.read_value()
    assert(temperature.value > -100)

    humidity = WeatherSensor('humidity', 'Brno humidity', PARAMS)
    humidity.read_value()
    assert(humidity.value > 0)

    assert(len(weather.get_forecast()) > 30)
    assert(len(weather.get_forecast()) > 30)
