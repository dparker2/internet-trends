import falcon
from app.resources.html import HTMLResource


print("PRINTED")


app = falcon.API()


HTML_resource = HTMLResource()
app.add_route("/", HTML_resource, suffix="index")
