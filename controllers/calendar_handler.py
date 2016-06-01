import datetime
import logging
import time

import pytz
import strict_rfc3339
import webapp2
from apiclient import discovery
from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from httplib2 import Http
from oauth2client.contrib.appengine import AppAssertionCredentials

from models.account import Account
from models.event import Event
from models.service_settings import ServiceSettings


def convert_central_time(utc_datetime):
    central_tz = pytz.timezone('America/Chicago')
    return datetime.datetime.fromtimestamp(time.mktime(utc_datetime.timetuple()), central_tz)


def parse_date_time(date_string, date_time_string):
    if date_string:
        date_time = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    else:
        timestamp = strict_rfc3339.rfc3339_to_timestamp(date_time_string)
        date_time = datetime.datetime.utcfromtimestamp(timestamp)
    
    return date_time


def set_event_reminders(event):
    summary = event.summary.lower()
    dates = []

    if "general meeting" in summary:

        first = event.start
        second = event.start

        first = convert_central_time(first)
        second = convert_central_time(second)

        first -= datetime.timedelta(days=2)

        first = first.replace(hour=10, minute=0, second=0)
        second = second.replace(hour=10, minute=0, second=0)

        logging.info("Reminder set for: %s", first)
        logging.info("Reminder set for: %s", second)

        dates.append(first)
        dates.append(second)

    else:
        return

    for date in dates:
        task = deferred.defer(send_event_reminders, event.key, _eta=date)
        event.tasks.append(task.name)


def send_event_reminders(key):
    event = key.get()
    accounts = Account.query().get()

    client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    for account in accounts:
        response_body = response_model.get(None, None, response_model.TAG_REMINDER)
        client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response_body+event.summary)
    

class CalendarHandler(webapp2.RequestHandler):

    def get(self):

        credentials = AppAssertionCredentials("https://www.googleapis.com/auth/calendar.readonly")
        http_auth = credentials.authorize(Http())
        cal_service = discovery.build('calendar', 'v3', http=http_auth)

        service_settings = ServiceSettings.query().get()
        if not service_settings:
            service_settings = ServiceSettings()
        next_sync_token = service_settings.cal_sync_token

        cal_events = []
        if next_sync_token:
            now = None
        else:
            now = strict_rfc3339.now_to_rfc3339_utcoffset()

        try:
            events_result = cal_service.events().list(calendarId="utsaspectrum@gmail.com", timeMin=now,
                                                      syncToken=next_sync_token).execute()
        except:
            service_settings.cal_sync_token = None
            service_settings.put()
            raise

        cal_events += events_result.get('items', [])
        next_page_token = events_result.get('nextPageToken', None)

        while next_page_token:
            events_result = cal_service.events().list(calendarId="utsaspectrum@gmail.com", timeMin=now,
                                                      syncToken=next_sync_token, pageToken=next_page_token).execute()
            cal_events += events_result.get('items', [])
            next_page_token = events_result.get('nextPageToken', None)

        next_sync_token = events_result.get("nextSyncToken", None)
        service_settings.cal_sync_token = next_sync_token
        service_settings.put()

        for cal_event in cal_events:
            cal_id = cal_event.get("id")

            event = Event.query().filter(Event.cal_id == cal_id).get()

            if event:
                q = taskqueue.Queue('default')
                for task in event.tasks:
                    q.delete_tasks(taskqueue.Task(name=task))
                event.tasks = []

                if cal_event.get("status") == "cancelled":
                    event.key.delete()
                    logging.info("Event deleted: %s", event)
                    continue
            else:
                event = Event(cal_id=cal_id)
                event.put()

            summary = cal_event.get("summary")
            description = cal_event.get("description")

            start = cal_event.get("start")
            end = cal_event.get("end")

            start = parse_date_time(start.get("date"), start.get("dateTime"))
            end = parse_date_time(end.get("date"), end.get("dateTime"))

            event.summary = summary
            event.description = description
            event.start = start
            event.end = end

            set_event_reminders(event)

            event.put()

            logging.info("New event created: %s", event)
