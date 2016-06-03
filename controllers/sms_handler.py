import logging

import twilio.twiml
import webapp2
from twilio.util import RequestValidator

import controllers.command_controller as command
import controllers.create_controller as create
import controllers.delete_controller as delete
import controllers.onboard_controller as onboard
import models.account as account_model
import response_strings
import strings
from models.account import Account
from models.response import get_response


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

        twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

        phone = self.request.get("From", None)

        account = Account.query().filter(Account.phone == phone).get()

        if account is None:
            account = create.controller(self.request)

        was_command = False
        if not account.state_locked:
            was_command = command.controller(self.request, account)

        if not was_command:
            if account.state == account_model.STATE_ONBOARD:
                onboard.controller(self.request, account)
            elif account.state == account_model.STATE_DELETE:
                delete.controller(self.request, account)
            else:
                response = get_response(response_strings.NO_MATCH, response_strings.VAR_NAME)
                response = response.replace(response_strings.VAR_NAME, account.first)
                twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)
