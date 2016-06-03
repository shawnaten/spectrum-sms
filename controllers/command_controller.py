from twilio.rest import TwilioRestClient

import models.account as account_model
import models.response as response_model
import response_strings
import strings

COMMAND_MENU = "menu"
COMMAND_DELETE = "delete"


def controller(request, account):
    message = request.get("Body")
    twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    message = message.lower()

    if message == COMMAND_MENU:
        response = response_model.get_response(response_strings.MENU)
    elif message == COMMAND_DELETE:
        account.state = account_model.STATE_DELETE
        response = response_model.get_response(response_strings.DELETE_CONFIRM)
    else:
        response = response_model.get_response(response_strings.NO_MATCH, response_strings.VAR_NAME)
        response = response.replace(response_strings.VAR_NAME, account.first)

    account.put()
    twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)
