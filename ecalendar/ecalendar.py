from jinja2 import Environment, FileSystemLoader
from datetime import date, timedelta

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

    def render(self, todays_weather,template_path="templates/", output_path = None):
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


