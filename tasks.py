#!/usr/bin/env python

import webapp2

from controllers.calendar_handler import CalendarHandler

app = webapp2.WSGIApplication([
    ('/tasks/calendar', CalendarHandler)
])
