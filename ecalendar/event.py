from datetime import date, timedelta
class Event:
    
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def is_multiday(self):
        return self.start_date != self.end_date
