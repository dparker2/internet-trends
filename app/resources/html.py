import falcon


def ensure_html_content(request, response, resource):
    response.content_type = falcon.MEDIA_HTML


@falcon.after(ensure_html_content)
class HTMLResource:
    def __init__(self):
        from templates import env

        self.templates = env

    def on_get_index(self, request, response):
        template = self.templates.get_template("index.j2")
        response.body = template.render(twitter=["#JohnDoe"])
