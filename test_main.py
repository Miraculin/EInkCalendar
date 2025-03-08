import json
import weather.weather as wm
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
    fake_event = event.Event("Friend 1 Birthday", date.today(), date.today())
    fake_event_2 = event.Event("Friend 2 Birthday", date.today(), date(year=2023,month=9,day=30))
    fake_events = [fake_event, fake_event_2]
    cal.add_events(fake_events)
    cal.render_web(weather_manager.get_weather(), template_path="../templates/", output_path="test_output.html")

if __name__ == "__main__":
    main()
