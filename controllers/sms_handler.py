import logging

import twilio.twiml
import webapp2
from twilio.util import RequestValidator

import controllers.command_controller as command
import controllers.create_controller as create
import controllers.delete_controller as delete
import controllers.onboard_controller as onboard
import models.account as account_model
import strings
from models.account import Account


class SMSHandler(webapp2.RequestHandler):
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

        # Sending messages separately, send empty TwiML for now.
        twiml = twilio.twiml.Response()
        self.response.write(twiml)

        phone = self.request.get("From", None)

        account = Account.query().filter(Account.phone == phone).get()

        if account is None:
            account = create.controller(self.request)

        if not account.state_locked:
            command.controller(self.request, account)

        if account.state == account_model.STATE_ONBOARD:
            onboard.controller(self.request, account)
        elif account.state == account_model.STATE_DELETE:
            delete.controller(self.request, account)
