import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import termcolor
import tools

PORT = 8080
HTML = "./html/"
VALID_ENDPOINTS = ["/", "listSpecies", "/karyotype", "/chromosomeLength", "/geneSeq", "/geneInfo", "/geneCalc", "geneList"]

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')

        url = urlparse(self.path)
        endpoint = url.path
        arg = parse_qs(url.query)

        print(f"Endpoint: {endpoint}")
        print(f"Parameters: {arg}")

        error = True
        contents = ""
        status = 400

        while not error:

            if endpoint in VALID_ENDPOINTS:
                if endpoint == "/":
                    status = 200
                    contents = Path(HTML + "index.html").read_text()

                elif endpoint == "/listSpecies":
                    if len(arg) == 0:
                        status, contents = tools.list_species()
                    elif len(arg) == 1:
                        try:
                            limit = int(arg['limit'][0])
                            status, contents = tools.list_species(limit)
                        except (ValueError, KeyError, IndexError):
                            error = False
                    else:
                        error = False

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
