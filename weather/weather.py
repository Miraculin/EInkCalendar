import requests
import json
import os
from .forecast import Forecast

class Weather():
    '''Manages making API calls to OpenWeatherMap'''

    def __init__(self, lat, lon, api_key):
        self.lat = lat
        self.lon = lon
        self.api_key = api_key

        self.api_call_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=metric"
        self.icon_url = "https://openweathermap.org/img/wn/{}@2x.png"


    def get_weather(self):
        response = requests.get(self.api_call_url)

        forecast = Forecast()
        if response.status_code == 200:
            data = response.json()
            
            icon_id = data["weather"][0]["icon"]

            if not os.path.exists("icons"):
                os.mkdir("icons")
            icon_filepath = f"icons/{icon_id}.png"
            if not os.path.exists(icon_filepath):
                with open(icon_filepath, "wb+" ) as f:
                    icon_download = self.icon_url.format(icon_id)
                    r = requests.get(icon_download, stream=True)
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)

            forecast.set_forecast(data["main"]["temp"], data["weather"][0]["description"], icon_filepath)
            
            return forecast
        else:

            print(f"Request failed with status code {response.status_code}")
            return None
