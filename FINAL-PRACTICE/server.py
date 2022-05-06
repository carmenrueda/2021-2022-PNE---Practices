import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2
from urllib.parse import parse_qs, urlparse
from Seq1 import Seq
import json

PORT = 8080
HTML_FOLDER = "./html/"
ARGUMENT = "?content-type=application/json"

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = jinja2.Template(contents)
    return contents


def get_species(endpoint):

    PORT = 8080
    SERVER = "rest.ensembl.org"
    print(f"\nConnecting to server: {SERVER}, and port: {PORT}\n")
    connection = http.client.HTTPConnection(SERVER)

    try:
        connection.request("GET", endpoint)
        response = connection.getresponse()
        print(f"Response received!: {response.status} {response.reason}\n")
        data = response.read().decode("utf-8")
        data = json.loads(data)
        return data

    except ConnectionRefusedError:
        print("ERROR! Connection has been refused")
        exit()


socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        url_parsed = urlparse(self.path)
        path = url_parsed.path
        arguments = parse_qs(url_parsed.query)


        if path == "/":
            contents = Path('indexchulo.html').read_text()

        elif path == "/listSpecies":
            ENDPOINT = "info/species"
            species = get_species(HTML_FOLDER+ ENDPOINT + ARGUMENT)["species"]
            if len(path) == 2:
                second_argument = arguments[1]
                third_argument = second_argument.split('=')[1]  # from = to the end of second argument
            else:
                third_argument = ""
            if third_argument == "":  # no number (no 3arg), print all species

                n_sequence = int(arguments["n_sequence"][0])
                sequence = LIST_SEQUENCES[n_sequence]
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "n_sequence": n_sequence,
                    "sequence": sequence
                })

    else:
            contents = Path('Error.html').read_text()


        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))
        self.end_headers()

        self.wfile.write(contents.encode())

        return


Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()