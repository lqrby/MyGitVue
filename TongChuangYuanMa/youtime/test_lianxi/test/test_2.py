from locust import web

@web.app.route("/added_page")
def my_added_page():
    return "Another page"

from locust import events

def my_success_handler(request_type=1, name=2, response_time=0, response_length=5, **kw):
    print ("Successfully fetched: %s" % (name))

events.request_success += my_success_handler
print(events.request_success)