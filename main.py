#!/usr/bin/env python

import webapp2
from controllers.sms_handler import SMSHandler


app = webapp2.WSGIApplication([
    ('/sms', SMSHandler)
])
