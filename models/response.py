from google.appengine.ext import ndb

TAG_START = "start"
TAG_END = "end"
TAG_ERROR = "error"
TAG_CANCEL = "cancel"
TAG_MENU = "menu"
TAG_TIMEOUT = "timeout"

VAR_NAME = "[NAME]"
VAR_EMAIL = "[EMAIL]"
VAR_URL = "[URL]"
VAR_CLASS = "[CLASS]"


def get(state, substate, tag, *variables):

    response = Response.query().filter(
        Response.state == state,
        Response.substate == substate,
        Response.tag == tag).get()

    if variables is not None:
        var_field = ""
        for variable in variables:
            var_field += variable + " "
        var_field = var_field.strip()
    else:
        var_field = None

    if response is None:
        response = Response(state=state, substate=substate, tag=tag, vars=var_field)
        response.put()

    if response.text is None:
        text = "state: " + (state if state is not None else "none") + "\n"
        text += "substate: " + (substate if substate is not None else "none") + "\n"
        text += "tag: " + (tag if tag is not None else "none")
        return text
    else:
        return response.text


class Response(ndb.Model):
    text = ndb.StringProperty()
    state = ndb.StringProperty()
    substate = ndb.StringProperty()
    tag = ndb.StringProperty()
    vars = ndb.StringProperty()



