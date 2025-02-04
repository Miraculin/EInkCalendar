import json
import weather.weather as wm
#from weather import Weather
import ecalendar.ecalendar as ecal
import ecalendar.event as event
from datetime import date, timedelta

def main():

    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    lat = config_data["latitude"]
    lon = config_data["longitude"]
    API_KEY = config_data["weather_api_key"]
    
    weather_manager = wm.Weather(lat, lon, API_KEY)
    cal = ecal.ECalendar()

    #load events
    #render calendar
    events = []

    cal.add_events(events)
    cal.render(weather_manager.get_weather(), output_path="output.html")

if __name__ == "__main__":
    main()