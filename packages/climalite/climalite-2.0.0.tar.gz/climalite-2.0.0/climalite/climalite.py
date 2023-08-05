import requests


class Weather:
    """
    Creates a weather object using an apikey and a city or coordinates as arguments
    the apikeys provided below are not guaranteed to work. It is recommended to use your own
    api key via https://openweathermap.org. Keys can take several hours to be activated.

    Usage:
    weather = Weather(city="Montreal", apikey="dd0db823487a5ae87659377a632d64f7")
    or
    weather = Weather(lat=41.5, lon=50, apikey="dd0db823487a5ae87659377a632d64f7")

    apikey: dd0db823487a5ae87659377a632d64f7
    alt: 26631f0f41b95fb9f5ac0df9a8f43c92
    """

    def __init__(self, city=None, lat=None, lon=None, apikey="dd0db823487a5ae87659377a632d64f7"):
        if city:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={apikey}'
            response = requests.get(url)
            self.data = response.json()
        elif lat and lon:
            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}'
            response = requests.get(url)
            self.data = response.json()
        else:
            raise TypeError("provide either a city or lat and lon arguments")

        if self.data['cod'] != "200":
            raise ValueError(self.data['message'])

    def next_12h(self):
        """
        returns weather data as a dict for the next 12 hrs
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        data = self.next_12h()
        results = []
        for i in range(4):
            results.append((data[i]['dt_txt'],
                            data[i]['main']['temp'],
                            data[i]['weather'][0]['description'],
                            data[i]['weather'][0]['icon']))
        return results
