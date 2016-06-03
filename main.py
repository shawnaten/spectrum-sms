#!/usr/bin/env python

import webapp2

from controllers.call_handler import CallHandler
from controllers.sms_handler import SMSHandler

app = webapp2.WSGIApplication([
    ('/sms', SMSHandler),
    ('/call', CallHandler)
])
