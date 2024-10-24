import socketserver
from .server import QWERTZHandler

class App:
    def __init__(self):
        self.routes = {}
        self.directories = {}
        self.error_pages = {}

    def setPage(self, route, page):
        self.routes[route] = page

    def setDirectory(self, path, base_path="/"):
        base_path = base_path.rstrip('/') + '/'
        self.directories[base_path] = path

    def listen(self, host="0.0.0.0", port=1337):
        app = self
        class Handler(QWERTZHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(app=app, *args, **kwargs)

        with socketserver.TCPServer((host, port), Handler) as httpd:
            print(f"Serving on {host}:{port}")
            httpd.serve_forever()

    def setErrorPage(self, error_code, page):
        """Set a custom error page for a specific error code."""
        self.error_pages[str(error_code)] = page

    def _getErrorPage(self, error_code):
        """Get the custom error page for a specific error code."""
        return self.error_pages.get(str(error_code))