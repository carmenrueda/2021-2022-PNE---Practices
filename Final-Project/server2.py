import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import termcolor
import tools

PORT = 8080
VALID_ENDPOINTS = ["/", "/listSpecies", "/karyotype", "/chromosomeLength", "/geneSeq", "/geneInfo", "/geneCalc", "/geneList"]
ERROR = 400
OK = 200

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(f"Request line: {self.requestline}", 'green')
        termcolor.cprint(f"Path: {self.path}", 'green')
        url = urlparse(self.path)
        endpoint = url.path
        arg = parse_qs(url.query)
        print(f"Parsed URL: {url}")
        print(f"Endpoint: {endpoint}")
        print(f"Argument: {arg}")

        bad_request = False
        status = ERROR
        contents = ""

        if endpoint in VALID_ENDPOINTS:
            if endpoint == "/":
                status = OK
                contents = Path("./html/index.html").read_text()

            elif endpoint == "/listSpecies":
                if len(arg) == 0:
                    status, contents = tools.list_species()
                elif len(arg) == 1:
                    try:
                        lim = int(arg['limit'][0])
                        if 0 <= lim <= 311:
                            status, contents = tools.list_species(lim)
                        else:
                            bad_request = True
                    except ValueError:
                        bad_request = True
                else:
                    bad_request = True

            elif endpoint == "/karyotype":
                if len(arg) == 1:
                    specie = arg['specie'][0]
                    status, contents = tools.karyotype(specie)
                else:
                    bad_request = True

            elif endpoint == "/chromosomeLength":
                if len(arg) == 2:
                    species = arg['specie'][0]
                    chromo = arg['chromosome'][0]
                    status, contents = tools.chromosome_length(species, chromo)
                else:
                    bad_request = True

            elif endpoint == "/geneSeq":
                if len(arg) == 1:
                    try:
                        gene = arg['gene'][0]
                        status, contents = tools.gene_seq(gene)
                    except KeyError:
                        bad_request = True
                else:
                    bad_request = True

            elif endpoint == "/geneInfo":
                if len(arg) == 1:
                    try:
                        gene = arg['gene'][0]
                        status, contents = tools.gene_info(gene)
                    except (KeyError, IndexError):
                        bad_request = True
                else:
                    bad_request = True

            elif endpoint == "/geneCalc":
                if len(arg) == 1:
                    try:
                        gene = arg['gene'][0]
                        status, contents = tools.gene_calc(gene)
                    except (KeyError, IndexError):
                        bad_request = True
                else:
                    bad_request = True

            elif endpoint == "/geneList":
                if len(arg) == 3:
                    try:
                        chromosome = arg['chromo'][0]
                        start = int(arg['start'][0])
                        end = int(arg['end'][0])
                        status, contents = tools.gene_list(chromosome, start, end)
                    except (KeyError, ValueError, IndexError):
                        bad_request = True
                else:
                    bad_request = True
        else:
            bad_request = True

        if bad_request:
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
