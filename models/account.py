from google.appengine.ext import ndb
from twilio.rest import TwilioRestClient

import models.response as response_model
import response_strings
import strings

STATE_ONBOARD = "onboard"
STATE_DELETE = "delete"


def incomplete_handler(account_id):
    account = Account.get_by_id(account_id)
    client = TwilioRestClient(strings.ACCOUNT_SID, strings.AUTH_TOKEN)

    if account and not account.complete:
        response_body = response_model.get_response(response_strings.ONBOARD_TIMEOUT)
        client.messages.create(to=account.phone, from_=strings.SERVICE_NUMBER, body=response_body)
        account.key.delete()


class Account(ndb.Model):
    phone = ndb.StringProperty()
    first = ndb.StringProperty()
    last = ndb.StringProperty()
    email = ndb.StringProperty()
    classification = ndb.StringProperty()

    state = ndb.StringProperty()
    substate = ndb.StringProperty()
    state_locked = ndb.BooleanProperty(default=False)

    created = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False)
