import os
import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from Seq1 import Seq

PORT = 8080
SEQUENCES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/":
            contents = Path('Form4.html').read_text()
            self.send_response(200)

        elif self.path == "/ping?":
            contents = f""" 
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>Result</title>
                    </head>
                    <body>
                        <h1>PING OK!</h1>
                        <p>The SEQ2 server is running</p>
                        <a href="/">Main page</a>
                    </body>
                </html>"""
            self.send_response(200)

        elif self.path.startswith("/get"):
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query) #diccionario: key-msg ; valor-lista con 1 string (abcdefg)
            try:
                seq_num = int(params["sequence_number"][0])
                sequence = Seq()
                filename = os.path.join("..", "Genes", f"{SEQUENCES[seq_num]}")
                sequence.read_fasta(filename)
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>GET</title>
                        </head>
                        <body>
                            <h1>Sequence number {seq_num}:</h1>
                            <p>{sequence}</p>
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.send_response(200)
            except(KeyError, IndexError):
                contents = Path(f"Error.html").read_text()
                self.send_response(404)

        elif self.path.startswith("/gene"):
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)  # diccionario: key-msg ; valor-lista con 1 string (abcdefg)
            try:
                gene = params["gene"][0]
                sequence = Seq()
                filename = os.path.join("..", "Genes", f"{gene}.txt")
                sequence.read_fasta(filename)
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>GET</title>
                        </head>
                        <body>
                            <h1>Gene: {gene}:</h1>
                            <textarea rows="50" cols="50">{sequence}</textarea><br>
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.send_response(200)
            except IndexError:
                contents = Path(f"Error.html").read_text()
                self.send_response(404)

        elif self.path.startswith("/operation"):
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)  # diccionario: key-msg ; valor-lista con 1 string (abcdefg)
            try:
                bases = params["html"][0]
                op = params["op"][0]
                if op in ["info", "comp", "rev"]:
                    sequence = Seq(bases)
                    contents = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <meta charset="utf-8">
                                <title>GET</title>
                            </head>
                            <body>
                                <h1>Sequence</h1>
                                <p>{sequence}</p>
                                <h1>Operation</h1>
                                <p>{op.upper()}</p>
                                <h1>Result>/h1>
                        """
                    if op == "info":
                        contents += f"<p>{sequence.info()}</p>"
                    elif op == "comp":
                        contents += f"<p>{sequence.complement()}</p>"
                    elif op == "rev":
                        contents += f"<p>{sequence.reverse()}</p>"
                    contents+= """
                                <a href="/">Main page</a>
                            </body>
                        </html>"""
                    self.send_response(200)
                else:
                    contents = Path(f"Error.html").read_text()
                    self.send_response(404)
            except IndexError:
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
        print("Stopped by the user")
        httpd.server_close()