from jinja2 import Environment, FileSystemLoader
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont

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

    def render_web(self, todays_weather,template_path="templates/", output_path = None):
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("cal_template.html")


        content = template.render(entries=self.entries,
                                  today=self.today,
                                  weekdays=self.weekdays_ordering,
                                  forecast=todays_weather)
        if output_path is None:
            print(content)
        else:
            with open(output_path, "w+") as f:
                f.write(content)


    def render(self, today_weather, resolution, output_path = None):
        im = Image.new("L", resolution, 255) # 255 is white
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(r'/usr/share/fonts/truetype/arial.ttf', 12)
        bigfont = ImageFont.truetype(r'/usr/share/fonts/truetype/arial.ttf', 20)

        self.__render_area_delimiters(draw, 1359)
        self.__render_entries(draw,font)
        self.__render_date_area(draw, 1359, bigfont)

        if output_path is None:
            im.save(sys.stdout, "BMP")
        else:
            im.save(output_path, "BMP")
    
    def __render_area_delimiters(self, draw,width):
        '''draw: ImageDraw to render to'''
        draw.line([(width,0),(width, 1404)],0,1)
        draw.line([(width,226),(width+513, 226)],0,1)
        draw.line([(width,453),(width+513, 453)],0,1)

    def __render_entries(self, draw,font):
        for i, e in enumerate(self.entries):
            x = i%7
            y = i//7
            xy = ((x*194, y*228),((x+1)*194,(y+1)*228))
            date_divide = [(x*194, y*228+32),((x+1)*194,y*228+32)]
            draw.rectangle(xy,255,0,1)
            draw.line(date_divide,0,1)

            if e.date == self.today:
                today_indicator = [(x*194, y*228),((x+1)*194,(y)*228+32)]
                draw.rectangle(today_indicator,188,0,1)
                draw.text((x*194+5,y*228+5), e.date.strftime("%b %d %a"), 0, font)
            elif e.date < self.today or e.date.month > self.today.month+1:
                draw.text((x*194+5,y*228+5), e.date.strftime("%b %d %a"), 188, font)
            else:
                draw.text((x*194+5,y*228+5), e.date.strftime("%b %d %a"), 0, font)
    
    def __render_date_area(self, draw,width, font):
        draw.text((width+5, 10), self.today.strftime("%A, The %d of %B in the Year %Y"), 0, font)

