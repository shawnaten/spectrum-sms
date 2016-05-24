import webapp2

import controllers.command_controller as command
import controllers.create_controller as create
import controllers.delete_controller as delete
import controllers.onboard_controller as onboard
import models.account as account_model
from models.account import Account


class SMSHandler(webapp2.RequestHandler):
    def get(self):

        phone = self.request.get("From")
        account = Account.query().filter(Account.phone == phone).get()

        if account is None:
            account = create.controller(self.request)

        if not account.state_locked:
            command.controller(self.request, account)

        if account.state == account_model.STATE_ONBOARD:
            onboard.controller(self.request, account)
        elif account.state == account_model.STATE_DELETE:
            delete.controller(self.request, account)

        self.response.write("")
