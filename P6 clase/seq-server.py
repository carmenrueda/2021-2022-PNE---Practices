import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2
from urllib.parse import parse_qs, urlparse
from Seq1 import Seq

PORT = 8080
HTML_FOLDER = "./html/"
LIST_SEQUENCES = ["ACGTCCAGTAAA", "ACGTAGTTTTTAAACCC", "GGGTAAACTACG",
                  "CGTAGTACGTA", "TGCATGCCGAT", "ATATATATATATATATATA"]
LIST_GENES = ["ADA", "FRAT1", "FXN", "RNU5A", "U5"]

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    """Return the decoded contents of the pointed-to file (./html/html) as a string"""
    contents = jinja2.Template(contents)
    """A Jinja template is simply a text file with any text-based format (HTML, XML). 
    A template contains variables which get replaced with others when a template is rendered; 
    and tags, which control the logic of the template."""
    return contents


def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1
    """suma 1 a cada value de las bases que se encuentra en la iteration y se queda en forma de diccionario"""

    total = sum(d.values())
    """el total de bases será la suma de todos los values"""
    for k, v in d.items():
        d[k] = [v, (v * 100) / total]
        """d = {"A": [4, 20], "C": [8, 25], "G": [12, 30], "T": [8, 25]} 
        siendo el primer numero la cant y el segundo el porcentaje"""
    return d


def convert_message(base_count):
    message = ""
    for k,v in base_count.items():
        message += k + ": " + str(v[0]) + " (" + str(v[1]) + "%)" +"\n"
        """el mensaje será = 'C':'8'('25'%)"""
    return message

def info_operation(arg):
    base_count = count_bases(arg)
    """d = {"A": [4, 20], "C": [8, 25], "G": [12, 30], "T": [8, 25]} """
    response = "<p> Sequence: " + arg + "</p>"
    response += "<p> Total length: " + str(len(arg)) + "</p>"
    response += convert_message(base_count)
    return response


socketserver.TCPServer.allow_reuse_address = True
"""para que se pueda conectar con el mismo puerto si de primeras no funciona"""


class TestHandler(http.server.BaseHTTPRequestHandler):
    """clase con funciones que nos permitirá manejar nuestra http request"""


    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        """request line en verde"""
        url_parsed = urlparse(self.path)
        """urlparse splits a URL string into its components (normally a 6 items tuple)"""
        path = url_parsed.path #.path???
        arguments = parse_qs(url_parsed.query) #.query???
        """Parse a query string given as a string argument. 
        Data are returned as a dictionary -> 
        keys: unique query variable names, values: lists of values for each name."""

        # Message to send back to the client

        if path == "/":
            """Si está vacío le enseño mi index con formato html"""
            contents = read_html_file("html/index.html")\
                .render(context=
                        {"n_sequences": len(LIST_SEQUENCES),
                         "genes": LIST_GENES})
            """Combines a given template with a given context dictionary 
            and returns an HttpResponse object with that rendered text.
            NECESSARY: 
            {template_name : request object used to generate this response} """

        elif path == "/ping":
            """Si me piden ping le enseño mi ping con formato html"""
            contents = read_html_file(path[1:] + ".html").render()

        elif path == "/get":
            """Si me piden get le muestro una lista de números, 
            asocio cada número a una secuencia
            y según el que elija le enseño mi get en formato html con su secuencia asociada al número"""
            n_sequence = int(arguments["n_sequence"][0])
            sequence = LIST_SEQUENCES[n_sequence]
            contents = read_html_file(path[1:] + ".html")\
                .render(context = {
                "n_sequence": n_sequence,
                "sequence": sequence
            })

        elif path == "/gene":
            """Si me piden gene le muestro una lista de genes,
            como lo que quieren es la secuencia hago un caminito './sequences/gene_name.txt'
            y le enseño mi get en formato html con el gen elegido y su secuencia asociada"""
            gene_name = arguments["gene_name"][0]
            sequence = Path("./sequences/" + gene_name + ".txt").read_text()
            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "gene_name": gene_name,
                "sequence": sequence
            })

        elif path == "/operation":
            """Si me piden operation muestro primero la lista de genes y luego la de posibles operaciones"""
            sequence = arguments["sequence"][0]
            operation = arguments["operation"][0]

            if operation == "rev":
                """Si eligen rev, enseño mi operation en formato html, 
                meto las elecciones de la operación y la secuencia y enseño el reversed de mi clase Seq."""
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "operation": operation,
                    "result": sequence.reverse()
                })

            elif operation == "info":
                """Si eligen info hago lo mismo pero con la función que he hecho antes de info_operation"""
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "operation": operation,
                    "result": info_operation(sequence)
                })

            elif operation == "comp":
                """Si me piden comp igual con el complement de mi clase Seq."""
                contents = read_html_file(path[1:] + ".html") \
                    .render(context={
                    "operation": operation,
                    "result": Seq.complement(sequence)
                })

        else:
            contents = "I am the happy server! :-)"
            """Si me piden otra cosa en vez de controlar el error le pongo q soy un happy server"""

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



