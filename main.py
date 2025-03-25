import weather.weather as wm
#from weather import Weather
import ecalendar.ecalendar as ecal
import ecalendar.event as event
from g_calendar.g_calendar import GCalendar
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
    gcal = GCalendar()
    gcal_events = gcal.getEvents()

    # Convert to internal Event class
    events = event.Event.eventsFromGCal(gcal_events)

    #render calendar
    cal.add_events(events)
    # cal.render_web(weather_manager.get_weather(), output_path="output.html")
    cal.render(weather_manager.get_weather(), conf, output_path="output.bmp")

if __name__ == "__main__":
    main()