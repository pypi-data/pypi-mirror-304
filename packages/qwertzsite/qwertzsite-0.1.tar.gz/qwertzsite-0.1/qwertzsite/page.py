from .body import Body

class Page:
    def __init__(self, title):
        self.title = title
        self.body = None
        self.favicon = None

    def setBody(self, body: Body):
        self.body = body

    def setFavicon(self, path):
        self.favicon = path

    def render(self):
        favicon_link = f'<link rel="icon" type="image/x-icon" href="{self.favicon}">' if self.favicon else ''
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.title}</title>
            {favicon_link}
        </head>
        <body>
            {self.body.render() if self.body else ''}
        </body>
        </html>
        """
    
    @classmethod
    def fromHTML(cls, html_content):
        page = cls("")
        page.render = lambda: html_content
        page.setBody = lambda *args, **kwargs: print("[QWERTZSite] [ERROR] Cannot set body for HTML content")
        page.setFavicon = lambda *args, **kwargs: print("[QWERTZSite] [ERROR] Cannot set favicon for HTML content")
        return page