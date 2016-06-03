from twilio.rest import TwilioRestClient

import models.response as response_model
import response_strings
import strings

COMMAND_YES = "yes"
COMMAND_NO = "no"


def controller(request, account):
    message = request.get("Body")
    twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    message = message.lower()

    if message == COMMAND_YES:
        account.key.delete()
        response = response_model.get_response(response_strings.DELETE_COMPLETE, response_strings.VAR_NAME)
    elif message == COMMAND_NO:
        account.state = None
        account.put()
        response = response_model.get_response(response_strings.DELETE_CANCEL)
    else:
        response = response_model.get_response(response_strings.DELETE_INPUT_ERROR)

    twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)