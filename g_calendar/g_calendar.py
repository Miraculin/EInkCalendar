import datetime
import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GCalendar():
  

  def __init__(self):
    self.creds = None
    if os.path.exists("token.json"):
      self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      print("Credentials expired, please refresh by running quickstart.py")

  def getEvents(self):
    '''Call the Google Calendar API and get the events for the next 60 days. Requires credentials to be valid'''
    if not self.creds or not self.creds.valid:
      print("Credentials expired, please refresh by running quickstart.py")
      return
    try:
      service = build("calendar", "v3", credentials=self.creds)

      # Call the Calendar API
      now = datetime.datetime.now(datetime.UTC)
      delta = datetime.timedelta(days=60)
      time_max = now + delta
      now_s = now.isoformat()
      time_max_s = time_max.isoformat()
      print("Getting events coming up in the next 60 days")

      events_result = (
          service.events()
          .list(
              calendarId="primary",
              timeMin=now_s,
              timeMax=time_max_s,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])

      if not events:
        print("No upcoming events found.")
        return []
      else:
        return events
    except HttpError as error:
      print(f"An error occurred: {error}")

if __name__ == "__main__":
  gcal = GCalendar()
  gcal.getEvents()