from google.appengine.ext import ndb

from models.account import Account


class Event(ndb.Model):
    cal_id = ndb.StringProperty()
    summary = ndb.StringProperty()
    description = ndb.StringProperty()

    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()

    tasks = ndb.StringProperty(repeated=True)
    attendees = ndb.KeyProperty(kind=Account, repeated=True)

