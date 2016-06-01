from google.appengine.ext import ndb


class ServiceSettings(ndb.Model):
    cal_sync_token = ndb.StringProperty()

