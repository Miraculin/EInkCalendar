from jinja2 import Environment, FileSystemLoader
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont
import requests
from textwrap import wrap

from .entry import Entry
from .event import Event
#TODO add moon phases

class ECalendar:
    weekdays_ordering = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(self):
        self.events = {}
        self.update()
    
    def add_events(self,events):
        for e in events:
            if e.start_date not in self.events.keys():
                self.events[e.start_date] = []
            if e.end_date not in self.events.keys():
                self.events[e.end_date] = []
            self.events[e.start_date].append(e)
            if e.start_date != e.end_date:
                self.events[e.end_date].append(e)
        self.update()

    def update(self, debug = False):
        self.today = date.today()
        current_weekday = self.today.weekday()

        entries = []
        if (current_weekday < 6):
            for i in range(current_weekday+1,0,-1):
                processing_date = self.today-i*timedelta(days=1)
                curr_entry = Entry(processing_date)
                if processing_date in self.events.keys():
                    processing_date_events = self.events[processing_date]
                    curr_entry.add_events(processing_date_events)

                entries.append(curr_entry)
        i = 0
        while len(entries) < 42:
            processing_date = self.today+i*timedelta(days=1)
            curr_entry = Entry(processing_date)
            if processing_date in self.events.keys():
                processing_date_events = self.events[processing_date]
                curr_entry.add_events(processing_date_events)

            entries.append(curr_entry)
            i = i + 1
        
        if (debug):
            print(entries)
        self.entries = entries


    def render(self, today_weather, config_data, output_path = None):
        conf = config_data
        width = conf.display_width
        height = conf.display_height

        resolution = (width, height)
        font_file = conf.font

        im = Image.new("L", resolution, 255) # 255 is white
        draw = ImageDraw.Draw(im)

        font_size = 20
        bigfont_size = 40

        font = ImageFont.truetype(font_file, font_size)
        bigfont = ImageFont.truetype(font_file, bigfont_size)

        calendar_area_ratio = 0.75 #Percentage of width taken up by the calendar
        calendar_width = 7*(int(calendar_area_ratio*width)//7) # Round to nearest multiple of 7, as we will always have 7 cells (1 week)
        bar_width = width-calendar_width

        cell_width = calendar_width//7
        cell_height = height//6

        date_area_height = 1*cell_height
        weather_area_height = 1* cell_height

        self.__render_area_delimiters(draw, calendar_width,width,height,date_area_height, weather_area_height)
        self.__render_entries(draw,cell_width, cell_height,font)
        self.__render_date_area(draw, calendar_width, bar_width, date_area_height, bigfont)
        self.__render_weather_area(draw, im, today_weather, calendar_width, date_area_height, bar_width, weather_area_height, bigfont)

        if output_path is None:
            im.save(sys.stdout, "BMP")
        else:
            im.save(output_path, "BMP")
    
    def __render_area_delimiters(self, draw,start, width, height,date_area_height, weather_area_height):
        '''draw: ImageDraw to render to'''

        draw.line([(start,0),(start, height)],0,1)
        draw.line([(start,date_area_height),(width, date_area_height)],0,1)
        draw.line([(start,date_area_height+weather_area_height),(width, date_area_height+weather_area_height)],0,1)

    def __render_entries(self, draw, cell_width, cell_height, font):
        text_padding = 5 #padding from left and top in px for text in each calendar entry
        text_overflow = 20 #length of string before we overflow to next line

        for i, e in enumerate(self.entries):
            x = i%7
            y = i//7
            
            xy = ((x*cell_width, y*cell_height),((x+1)*cell_width,(y+1)*cell_height))
            
            date_divide_height = 32
            date_divide = [(x*cell_width, y*cell_height+date_divide_height),((x+1)*cell_width,y*cell_height+date_divide_height)]
            
            draw.rectangle(xy,255,0,1)
            draw.line(date_divide,0,1)
            
            date_center_x = x*cell_width+cell_width//2
            date_center_y = y*cell_height+date_divide_height
            date_xy = (date_center_x, date_center_y)

            if e.date == self.today:
                today_indicator = [(x*cell_width, y*cell_height),((x+1)*cell_width,(y)*cell_height+date_divide_height)]
                draw.rectangle(today_indicator,188,0,1)

            if e.date < self.today or e.date.month > self.today.month+1:
                draw.text(date_xy, e.date.strftime("%b %d %a"), 188, font, anchor="md")
            else:
                draw.text(date_xy, e.date.strftime("%b %d %a"), 0, font,anchor="md")

            events_list = "\n".join(map(lambda x: "\n  ".join(wrap(x, width=text_overflow)),e.events))
            draw.multiline_text((x*cell_width+text_padding, y*cell_height+date_divide_height+text_padding), events_list, 0, font)
    
    def __render_date_area(self, draw, start, width, height, font):
        date_text = self.today.strftime("%A\n The %d of %B\n in the Year %Y")
        draw.multiline_text((start+width//2, height//2), date_text, 0, font, anchor="mm",align="center")

    def __render_weather_area(self, draw, im, weather, start_x,start_y, width, height, font):
        weather_text = "\n".join([f"{weather.temperature}°C", weather.weather.title()])
        draw.multiline_text((start_x+width//2, start_y+height//2), weather_text, 0, font, anchor="mm", align="center")
        icon = Image.open(requests.get(weather.icon, stream=True).raw)
        im.paste(icon,(start_x+width//2-icon.width//2, start_y+height//2+icon.height//2), icon)

