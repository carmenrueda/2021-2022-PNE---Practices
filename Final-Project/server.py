import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import termcolor
import tools

PORT = 8080
HTML = "./html/"
VALID_ENDPOINTS = ["/", "listSpecies", "/karyotype", "/chromosomeLength", "/geneSeq", "/geneInfo", "/geneCalc", "geneList"]
OK = 200
ERROR = 400

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')
        url = urlparse(self.path)

        endpoint = url.path
        print(f"Endpoint: {endpoint}")
        arg = parse_qs(url.query)
        print(f"Parameters: {arg}")
        status = 404
        error = False
        contents = ""

        if endpoint in VALID_ENDPOINTS:

            if endpoint == "/":
                status = OK
                contents = Path(HTML + "index.html").read_text()

            elif endpoint == "/listSpecies":
                if len(arg) == 0:
                    status, contents = tools.list_species()
                elif len(arg) == 1:
                    try:
                        limit = int(arg['limit'][0])
                        status, contents = tools.list_species(limit)
                    except (KeyError, IndexError, ValueError):  # Exception
                        error = True
                else:
                    error = True

            elif endpoint == "/karyotype":
                if len(arg) == 1:
                    try:
                        species = int(arg['species'][0])
                        status, contents = tools.karyotype(species)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            elif endpoint == "/chromosomeLength":
                if len(arg) == 2:
                    try:
                        species = int(arg['species'][0])
                        chromosomes = arg['chromosomes'][0]
                        status, contents = tools.chrom_length(species, chromosomes)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            elif endpoint == "/geneSeq":
                if len(arg) == 1:
                    try:
                        gene = int(arg['gene'][0])
                        status, contents = tools.gene_seq(gene)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            elif endpoint == "/geneInfo":
                if len(arg) == 1:
                    try:
                        gene = arg['gene'][0]
                        status, contents = tools.gene_info(gene)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            elif endpoint == "/geneCalc":
                if len(arg) == 1:
                    try:
                        gene = arg['gene'][0]
                        status, contents = tools.gene_calc(gene)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            elif endpoint == "/geneList":
                if len(arg) == 3:
                    try:
                        chromo = int(arg['chromo'][0])
                        start = int(arg['start'][0])

                        chromo = int(arg['chromo'][0])
                        gene = arg['gene'][0]
                        status, contents = tools.gene_calc(gene)
                    except (KeyError, IndexError):
                        error = False
                else:
                    error = False

            else:
                error = True

        if error:
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
