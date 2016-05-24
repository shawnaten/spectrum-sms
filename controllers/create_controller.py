import datetime

from google.appengine.ext import deferred

import controllers.onboard_controller as onboard
import models.account as account_model
from models.account import Account


def controller(request):
    phone = request.get("From")

    account = Account(phone=phone)
    account.put()
    account.state = account_model.STATE_ONBOARD
    account.substate = onboard.SUBSTATE_WELCOME
    account.state_locked = True

    deferred.defer(account_model.incomplete_handler, account.key.id(),
                   _countdown=datetime.timedelta(minutes=10).seconds)

    return account
