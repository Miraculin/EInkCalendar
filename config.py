import json
from dataclasses import dataclass 

@dataclass
class Config():
    weather_api_key: str
    latitude: str
    longitude: str
    display_width: int
    display_height: int
    font: str

    @classmethod
    def fromJson(cls, config_file_path="config.json"):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)

        weather_api_key = config_data["weather_api_key"]
        
        latitude = config_data["latitude"]
        longitude = config_data["longitude"]

        display_width = config_data["display_width"]
        display_height = config_data["display_height"]

        font = config_data["font"]

        return cls(weather_api_key, latitude, longitude, display_height, display_width, font)