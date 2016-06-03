from google.appengine.ext import ndb


def get_response(description, *text_vars):

    if len(text_vars) == 0:
        vars_string = None
    else:
        vars_string = ""
        for var in text_vars:
            vars_string += var + " "
        vars_string = vars_string.strip()

    response = Response.query().filter(Response.description == description, Response.vars == vars_string).get()

    if response is None:
        response = Response(description=description, vars=vars_string)
        response.put()

    if response.text:
        return response.text
    else:
        response_string = "Response not set: " + response.description
        if response.vars:
            response_string += " " + response.vars
        return response_string


class Response(ndb.Model):
    description = ndb.StringProperty(required=True)
    vars = ndb.StringProperty()
    text = ndb.StringProperty()




