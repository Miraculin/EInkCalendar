from .event import Event
from datetime import date, timedelta

class Entry:

    def __init__(self, date):
        self.date = date
        self.events = []

    def add_events(self,events):
        for event in events:
            to_add = event.name
            if (event.start_date != self.date and event.end_date != self.date):
                continue
            elif (event.start_date == self.date and event.is_multiday()):
                self.events.append(to_add + " ->")
            elif (event.end_date == self.date and event.is_multiday()):
                self.events.append("<- "+ to_add)
            else:
                self.events.append(to_add)