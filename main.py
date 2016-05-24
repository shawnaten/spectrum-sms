#!/usr/bin/env python

import webapp2
from controllers.sms_handler import SMSHandler


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/sms', SMSHandler)
], debug=True)
