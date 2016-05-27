import datetime
import logging

import webapp2
from apiclient import discovery
from httplib2 import Http
from oauth2client.contrib.appengine import AppAssertionCredentials


class CalendarHandler(webapp2.RequestHandler):

    def get(self):

        credentials = AppAssertionCredentials("https://www.googleapis.com/auth/calendar.readonly")
        http_auth = credentials.authorize(Http())
        cal_service = discovery.build('calendar', 'v3', http=http_auth)

        events = []
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = cal_service.events().list(calendarId="utsaspectrum@gmail.com", timeMin=now).execute()
        events += events_result.get('items', [])
        next_page_token = events_result.get('nextPageToken', None)

        while next_page_token:
            events_result = cal_service.events().list(calendarId="utsaspectrum@gmail.com", timeMin=now,
                                                      pageToken=next_page_token).execute()
            events += events_result.get('items', [])
            next_page_token = events_result.get('nextPageToken', None)

        next_sync_token = events_result.get("nextSyncToken", None)

        logging.info("nextSyncToken: " + next_sync_token)

        for event in events:
            logging.info(event.get('summary'))
    
#    def get(self):

#        calendar_url = "https://calendar.google.com/calendar/ical/utsaspectrum%40gmail.com/public/basic.ics"

#        result = urlfetch.fetch(calendar_url, validate_certificate=True)

#        if result.status_code != 200:
#            logging.exception("Error syncing calendar.")
#            self.response.status = result.status_code
#            return

#        cal = Calendar.from_ical(result.content)

#        central = timezone('US/Central')
#        current = datetime.now(tz=central)
#        day = current.date()

#        for event in cal.walk("vevent"):
#            start = event.decoded('dtstart')
#            end = event.decoded('dtend')
#            summary = event.decoded('summary')

#            if type(start) is datetime and start >= current or type(start) is date and start >= day:
#                logging.info("%s: %s to %s", summary, start, end)