from google.appengine.ext import ndb


def get_response(description, *text_vars):

    if len(text_vars) == 0:
        vars_string = None
    else:
        vars_string = ""
        for sub in text_vars:
            vars_string += sub + " "
        vars_string = vars_string.strip()

    response = Response.query().filter(Response.description == description, Response.vars == vars_string).get()

    if response is None:
        response = Response(description=description, vars=vars_string)
        response.put()

    if response.text:
        return response.text
    else:
        return "Response not set: " + response.description + (" " + response.vars) if response.vars else ""


class Response(ndb.Model):
    description = ndb.StringProperty(required=True)
    vars = ndb.StringProperty()
    text = ndb.StringProperty()




