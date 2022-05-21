import http.server
import socketserver
import termcolor
from urllib.parse import urlparse, parse_qs

from pathlib import Path
import tools

PORT = 8080
ENDPOINTS = ["/", "/listSpecies", "/karyotype", "/chromosomeLength", "/geneSeq", "/geneInfo", "/geneCalc", "/geneList"]

socketserver.TCPServer.allow_reuse_address = True


def handle_karyotype(parameters):
    has_error = False
    contents = ""
    status = 400
    if len(parameters) == 1:
        try:
            specie = parameters['specie'][0]
            status, contents = su.karyotype(specie)
        except (KeyError, IndexError):
            has_error = True
    else:
        has_error = True

    return status, contents, has_error


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, "blue")

        url = urlparse(self.path)
        endpoint = url.path
        parameters = parse_qs(url.query)
        print("Endpoint: ", endpoint)
        print("Parameters: ", parameters)

        has_error = False
        contents = ""
        status = 400  # BAD_REQUEST
        if endpoint in ENDPOINTS:
            if endpoint == "/":
                status = 200
                contents = Path("./html/index.html").read_text()
            elif endpoint == "/listSpecies":
                if len(parameters) == 0:
                    status, contents = tools.list_species()
                elif len(parameters) == 1:
                    try:
                        limit = int(parameters['limit'][0])
                        status, contents = tools.list_species(limit)
                    except (KeyError, IndexError, ValueError):  # Exception
                        has_error = True
                else:
                    has_error = True

        if has_error:
            contents = Path("./html/error.html").read_text()

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