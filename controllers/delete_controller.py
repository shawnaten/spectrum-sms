from twilio.rest import TwilioRestClient

import models.account as account_model
import models.response as response_model
import strings

COMMAND_YES = "yes"
COMMAND_NO = "no"


def controller(request, account):
    message = request.get("Body")
    twilio_client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    message = message.lower()

    if message == COMMAND_YES:
        account.key.delete()
        response = response_model.get(account_model.STATE_DELETE, None, response_model.TAG_END)
    elif message == COMMAND_NO:
        account.state = None
        account.put()
        response = response_model.get(account_model.STATE_DELETE, None, response_model.TAG_CANCEL)
    else:
        response = response_model.get(account_model.STATE_DELETE, None, response_model.TAG_ERROR)

    twilio_client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response)