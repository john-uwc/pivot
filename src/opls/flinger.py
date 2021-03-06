
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import os
import util


class Flinger(BaseHTTPServer.HTTPServer, object):
    """custom handler for flinger"""

    class __Handler(SimpleHTTPRequestHandler):
        SimpleHTTPRequestHandler.protocol_version = "HTTP/1.0"

        def send_head(self):
            path = self.translate_path(self.path)
            f = None
            if os.path.isdir(path):
                if not self.path.endswith('/'):
                    self.send_response(301)
                    self.send_header("Location", self.path + "/")
                    self.end_headers()
                    return None
                for index in "index.html", "index.htm":
                    index = os.path.join(path, index)
                    if os.path.exists(index):
                        path = index
                        break
                else:
                    return self.list_directory(path)
            ctype = self.guess_type(path)
            try:
                f = open(path, 'rb')
            except IOError:
                self.send_error(404, "File not found")
                return None
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header(
                "Last-Modified", self.date_time_string(fs.st_mtime)
            )
            self.end_headers()
            return f

        def translate_path(self, path):
            return os.path.join(os.path.dirname(__file__), path[1:])

    """init for flinger"""

    def __init__(self, port):
        super(Flinger, self).__init__((util.net.localhost(), port), Flinger.__Handler)

    def launch(self):
        super(Flinger, self).serve_forever()
