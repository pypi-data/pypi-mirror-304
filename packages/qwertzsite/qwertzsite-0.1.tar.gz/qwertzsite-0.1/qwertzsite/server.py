import os
import http.server

class QWERTZHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, app=None, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)

    def do_GET(self):
        content = self._handle_request(self.path)
        if content == "404 Not Found":
            self.send_error(404, "File not found")
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
    
    def _handle_request(self, path):
        for base_path, directory in self.app.directories.items():
            if path.startswith(base_path):
                relative_path = path[len(base_path):]
                file_path = os.path.join(directory, relative_path)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        return file.read()
        
        # If not found in directories, check routes
        if path in self.app.routes:
            return self.app.routes[path].render()
        
        custom_404 = self.app._getErrorPage(404)
        if custom_404:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return custom_404.render()
        
        return "404 Not Found"