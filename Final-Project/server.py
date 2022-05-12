import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import termcolor
import tools

PORT = 8080
HTML_FOLDER = "./html/"
VALID_ENDPOINTS = ["/", "listSpecies", "/karyotype", "/chromosomeLength", "/geneSeq", "/geneInfo", "/geneCalc", "geneList"]

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')

        url = urlparse(self.path)
        endpoint = url.path
        params = parse_qs(url.query)

        print(f"Endpoint: {endpoint}")
        print(f"Parameters: {params}")

        error = False
        contents = ""
        status = 400

        if endpoint in VALID_ENDPOINTS:
            if endpoint == "/":
                status = 200
                contents = Path(HTML_FOLDER + "index.html").read_text()

            elif endpoint == "/listSpecies":
                if len(params) == 0:
                    status, contents = tools.list_species()
                elif len(params) == 1:
                    try:
                        limit = int(params['limit'][0])
                    except (ValueError, KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/karyotype":
                if len(params) == 1:
                    try:
                        species = int(params['species'][0])
                        status, contents = tools.karyotype()
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/chromosomeLength":
                if len(params) == 2:
                    try:
                        species = int(params['species'][0])
                        chromosomes = params['chromosomes'][0]
                        status, contents = tools.chrom_length(species, chromosomes)
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/geneSeq":
                if len(params) == 1:
                    try:
                        gene = int(params['gene'][0])
                        status, contents = tools.gene_seq(gene)
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/geneInfo":
                if len(params) == 1:
                    try:
                        gene = params['gene'][0]
                        status, contents = tools.gene_info(gene)
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/geneCalc":
                if len(params) == 1:
                    try:
                        gene = params['gene'][0]
                        status, contents = tools.gene_calc(gene)
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True

            elif endpoint =="/geneList":
                if len(params) == 3:
                    try:
                        chromo = int(params['chromo'][0])
                        start = int(params['start'][0])

                        chromo = int(params['chromo'][0])
                        gene = params['gene'][0]
                        status, contents = tools.gene_calc(gene)
                    except (KeyError, IndexError):
                        error = True
                else:
                    error = True



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
