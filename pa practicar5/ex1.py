import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import termcolor

PORT = 8080
VALID_ENDPOINTS = ["/", "/info/A", "/info/T", "/info/C", "/info/G"]
ERROR = 400
OK = 200

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'yellow')
        url = urlparse(self.path)
        endpoint = url.path
        arg = parse_qs(url.query)
        print(f"Endpoint: {endpoint}")
        print(f"Parameters: {arg}")

        status = ERROR
        contents = ""

        if endpoint == "/" or endpoint == "/index.html":
            status = OK
            contents = Path("index.html").read_text()

        else:
            resource = endpoint[1:]
            try:
                contents = Path(f"{resource}").read_text()
                status = OK
            except FileNotFoundError:
                contents = Path("./html/error.html").read_text()
                status = ERROR


        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents.encode())))
        self.end_headers()
        self.wfile.write(contents.encode())


handler = TestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
