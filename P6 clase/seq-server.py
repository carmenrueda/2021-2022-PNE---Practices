import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import parse_qs, urlparse
from Seq1 import Seq

HTML_FOLDER = "./html/"
LIST_SEQUENCES = ["ACGTCCAGTAAA", "ACGTAGTTTTTAAACCC", "GGGTAAACTACG",
                  "CGTAGTACGTA", "TGCATGCCGAT", "ATATATATATATATATATA"]
LIST_GENES = ["ADA", "FRAT1", "FXN", "RNU5A", "U5"]

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1

    total = sum(d.values())
    for k,v in d.items():
        d[k] = [v, (v * 100) / total]
    return d


def convert_message(base_count):
    message = ""
    for k,v in base_count.items():
        message += k + ": " + str(v[0]) + " (" + str(v[1]) + "%)" +"\n"
    return message

def info_operation(arg):
    base_count = count_bases(arg)
    response = "<p> Sequence: " + arg + "</p>"
    response += "<p> Total length: " + str(len(arg)) + "</p>"
    response += convert_message(base_count)
    return response

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        url_path = urlparse(self.path)
        path = url_path.path
        arguments = parse_qs(url_path.query)

        print("The old path was", self.path)
        print("The new path is", url_path.path)
        print("arguments", arguments)

        # Message to send back to the client

        if self.path == "/":
            contents = read_html_file("html/index.html")\
                .render(context=
                        {"n_sequences": len(LIST_SEQUENCES),
                         "genes": LIST_GENES})

        elif path == "/ping":
            contents = read_html_file(path[1:] + ".html").render()

        elif path == "/get":
            n_sequence = int(arguments["n_sequence"][0])
            sequence = LIST_SEQUENCES[n_sequence]
            contents = read_html_file(path[1:] + ".html")\
                .render(context = {
                "n_sequence": n_sequence,
                "sequence": sequence
            })

        elif path == "/gene":
            gene_name = arguments["gene_name"][0]
            sequence = Path("./sequences/" + gene_name + ".txt").read_text()
            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "gene_name": gene_name,
                "sequence": sequence
            })

        elif path == "/operation":
            sequence = arguments["sequence"][0]
            operation = arguments["operation"][0]
            if operation == "rev":
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "operation": operation,
                    "result": sequence.reverse()
                })

            elif operation == "info":
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "operation": operation,
                    "result": info_operation(sequence)
                })

        else:
            contents = "I am the happy server! :-)"

        # Generating the response message
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



