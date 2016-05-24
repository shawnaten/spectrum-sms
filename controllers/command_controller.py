from twilio.rest import TwilioRestClient

import models.account as account_model
import models.response as response_model
import strings

COMMAND_MENU = "menu"
COMMAND_DELETE = "delete"


def controller(request, account):
    message = request.get("Body")
    twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    message = message.lower()

    if message == COMMAND_MENU:
        response = response_model.get(None, None, response_model.TAG_MENU)
    elif message == COMMAND_DELETE:
        account.state = account_model.STATE_DELETE
        response = response_model.get(account_model.STATE_DELETE, None, response_model.TAG_START)
    else:
        response = response_model.get(None, None, None, response_model.VAR_NAME)
        response = response.replace(response_model.VAR_NAME, account.first)

    account.put()
    twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)
