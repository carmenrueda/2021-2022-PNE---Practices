import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import parse_qs, urlparse
from Seq1 import Seq

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


HTML_FOLDER = "./html/"
LIST_SEQS = ["ACGTGGCAG", "ATGTGTGTGTCA", "GTCACTGT", "ACGTGTGCA"]
LIST_GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def count_bases(seq):
    seq_dict = {"A": 0, "C": 0, "T": 0, "G": 0}
    for b in seq:
        pass


def do_GET(self):
    termcolor.cprint(self.requestline, 'green')
    url_path = urlparse(self.path)
    path = url_path.path
    arguments =parse_qs(url_path.query)
    print("The old path is", self.path)
    print("The new path is", url_path.path)
    print("arguments", arguments)

    if self.path == "/":
        contents = read_html_file("index.html")\
            .render(context={"n_sequences": len(LIST_SEQS),
                             "genes": LIST_GENES})
    elif path == "/ping":
        contents = read_html_file(path[1: + ".html"]).render() #asi se tiene el nombre
    elif path == "/get":
        n_sequence = int(arguments["n_sequence"][0])
        sequence = LIST_SEQS[n_sequence]
        contents = read_html_file(path[1: + ".html"])\
            .render(context = {
            "n_sequence": n_sequence,
            "sequence": sequence
        })
    elif path == "/gene":
        gene_name = arguments["gene_name"][0]
        sequence = Path("./sequences/" + gene_name + ".txt").read_text()
        contents = read_html_file(path[1: + ".html"]) \
            .render(context={
            "gene_name": gene_name,
            "sequence": sequence
        })
    elif path =="/operation":
        sequence = arguments["sequence"][0]
        operation = arguments["operation"][0]
        if operation == "rev":
            contents = read_html_file(path[1: + ".html"]) \
                .render(context={
                "operation": operation,
                "result": sequence
            })
        elif operation == "comp":
            contents = read_html_file(path[1: + ".html"]) \
                .render(context={
                "operation": operation,
                "result": sequence
            })
        elif operation == "":
            contents = read_html_file(path[1: + ".html"]) \
                .render(context={
                "operation": operation,
                "result": sequence
            })

    else:
        contents ="Happy server nsek"

    self.send_response(200)




