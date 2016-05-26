import webapp2
from google.appengine.api import urlfetch


class CalendarHandler(webapp2.RequestHandler):
    def get(self):

        calendar_url = "https://calendar.google.com/calendar/ical/utsaspectrum%40gmail.com/public/basic.ics"

        try:
            result = urlfetch.fetch(calendar_url)
            if result.status_code == 200:
                logging.info(result.content)
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('caught exception fetching calendar')

        self.response.write("")
