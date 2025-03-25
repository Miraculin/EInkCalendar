import weather.weather as wm
import ecalendar.ecalendar as ecal
import ecalendar.event as event
from datetime import date, timedelta
from config import Config

def main():

    conf = Config.fromJson()

    weather_api_key = conf.weather_api_key
    lat = conf.latitude
    lon = conf.longitude
    
    weather_manager = wm.Weather(lat, lon, weather_api_key)
    cal = ecal.ECalendar()

    #load events
    #render calendar
    fake_event = event.Event("Friend 1 Birthday", date.today(), date.today())
    fake_event_2 = event.Event("Friend 2 Birthday", date.today(), date(year=2023,month=9,day=30))
    fake_events = [fake_event, fake_event_2]
    cal.add_events(fake_events)

    cal.render(weather_manager.get_weather(), conf, output_path="test.bmp")

if __name__ == "__main__":
    main()
