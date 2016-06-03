import logging
import random

import twilio.twiml
import webapp2
from twilio.util import RequestValidator

import response_strings
import strings
from models.account import Account
from models.response import get_response


class CallHandler(webapp2.RequestHandler):
    def get(self):

        # Validate that request came from Twilio service.
        validator = RequestValidator(strings.AUTH_TOKEN)
        url = self.request.url
        url = url.replace("http", "https")
        signature = self.request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, {}, signature):
            logging.warn("Request did not come from Twilio.")
            self.response.status = 403
            return

        phone = self.request.get("From", None)
        account = Account.query().filter(Account.phone == phone).get()

        # Sending messages separately, send empty TwiML for now.
        twiml = twilio.twiml.Response()

        response = get_response(response_strings.CALL_HELLO, response_strings.VAR_NAME)

        if account and account.first:
            response = response.replace(response_strings.VAR_NAME, account.first)
        else:
            response = response.replace(response_strings.VAR_NAME, "")

        twiml.addSay(response)

        tracks = [
            "better_things",
            "dare",
            "enchanted",
            "makes_me_wonder",
            "the_reeling",
            "viva_la_vida"
        ]

        track_num = random.randint(0, len(tracks) - 1)

        twiml.addPlay(self.request.application_url + "/static/mp3/" + tracks[track_num] + ".mp3")

        response = get_response(response_strings.CALL_GOODBYE)

        twiml.addSay(response)
        twiml.addHangup()

        self.response.write(twiml)
