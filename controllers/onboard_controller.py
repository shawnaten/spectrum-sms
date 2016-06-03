import re

from twilio.rest import TwilioRestClient

import models.response as response_model
import response_strings
import strings

SUBSTATE_WELCOME = "welcome"
SUBSTATE_NAME = "name"
SUBSTATE_EMAIL = "email"
SUBSTATE_CLASS = "class"


def controller(request, account):
    message = request.get("Body")
    twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    if account.substate == SUBSTATE_WELCOME:
        response = response_model.get_response(response_strings.ONBOARD_WELCOME)
        twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)
        response = response_model.get_response(response_strings.ONBOARD_NAME)
        account.substate = SUBSTATE_NAME

    elif account.substate == SUBSTATE_NAME:
        message = message.title()
        names = message.split()

        if len(names) != 2:
            response = response_model.get_response(response_strings.ONBOARD_NAME_INPUT_ERROR)
        else:
            account.first = names[0]
            account.last = names[1]
            account.substate = SUBSTATE_EMAIL

            response = response_model.get_response(response_strings.ONBOARD_EMAIL)

    elif account.substate == SUBSTATE_EMAIL:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", message):
            response = response_model.get_response(response_strings.ONBOARD_EMAIL_INPUT_ERROR)
        else:
            account.email = message.lower()
            account.substate = SUBSTATE_CLASS
            response = response_model.get_response(response_strings.ONBOARD_CLASS)

    else:
        message = message.lower()

        if not re.match(r"freshman|sophomore|junior|senior|graduate", message):
            response = response_model.get_response(response_strings.ONBOARD_CLASS_INPUT_ERROR)
        else:
            account.classification = message
            account.complete = True
            account.state = None
            account.substate = None
            account.state_locked = False

            response = response_model.get_response(response_strings.ONBOARD_FINISH, response_strings.VAR_NAME)
            response = response.replace(response_strings.VAR_NAME, account.first)
            response = response.replace(response_strings.VAR_URL, request.host + "/rules")

    account.put()
    twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)
