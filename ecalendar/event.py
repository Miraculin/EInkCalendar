from datetime import date, timedelta,datetime
class Event:
    
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def is_multiday(self):
        return self.start_date != self.end_date

    @staticmethod
    def eventsFromGCal(gevents):
        events = []
        for gevent in gevents:
            name = gevent["summary"]
            if "dateTime" in gevent["start"].keys():
                start_date = datetime.fromisoformat(gevent["start"]["dateTime"]).date()
            else:
                start_date = (datetime.fromisoformat(gevent["end"]["date"])-timedelta(seconds=1)).date()
            if "dateTime" in gevent["end"].keys():
                end_date = datetime.fromisoformat(gevent["end"]["dateTime"]).date()
            else:
                end_date = (datetime.fromisoformat(gevent["end"]["date"])-timedelta(seconds=1)).date()

            
            new_event = Event(name, start_date, end_date)
            print(new_event.name, new_event.start_date)
            events.append(new_event)
        
        return events