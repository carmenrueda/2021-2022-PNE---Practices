import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/":
            contents = Path('Form-ex1.html').read_text()
            self.send_response(200)

        elif self.path.startswith("/echo?"):
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query) #diccionario: key-msg ; valor-lista con 1 string (abcdefg)            try:

            try:
                msg_param = params["msg"][0]
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>FORM 1</title>
                        </head>
                        <body>
                            <h1>Received message:</h1>
                            <p>{msg_param}</p>
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.response(200)

            except(KeyError, IndexError):
                contents = Path(f"Error.html").read_text()
                self.send_response(404)

        else:
            contents = Path(f"Error.html").read_text()
            self.send_response(404)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        self.end_headers()

        self.wfile.write(str.encode(contents))

        return

Handler = TestHandler


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()