import http.server
import socketserver
import json
import termcolor
from pathlib import Path
from Seq1 import Seq


def species_get(endpoint):  # function to obtain species from server rest.ensembl.org
    PORT = 8080
    SERVER = "rest.ensembl.org"
    print(f"\nConnecting to server: {SERVER}, and port: {PORT}\n")
    connection = http.client.HTTPConnection(SERVER)
    try:
        connection.request("GET", endpoint)
    except ConnectionRefusedError:
        print("ERROR! The database is down")
        exit()
    response = connection.getresponse()
    print(f"Response received!: {response.status} {response.reason}\n")
    data = response.read().decode("utf-8")  # answer decoded
    data_1 = json.loads(data)  # json format
    return data_1

PORT = 8080
PARAMS = "?content-type=application/json"
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'blue')  # line printed on terminal of service requested
        req_line = self.requestline.split(' ')
        path = req_line[1]
        arguments = path.split('?')
        first_argument = arguments[0]  # first part path until ?
        if first_argument == "/":  # if just /, main page -> index.html
            contents = Path('index.html').read_text()
            error_code = 200
        elif first_argument == "/listSpecies":
            ENDPOINT = "info/species"
            species = species_get(ENDPOINT+PARAMS)["species"]
            if len(arguments) == 2:
                second_argument = arguments[1]
                third_argument = second_argument.split('=')[1]  # from = to the end of second argument
            else:
                third_argument = ""
            if third_argument == "":  # no number (no 3arg), print all species
                contents = f"""
                        <!DOCTYPE html>
                        <html lang = "en">
                        <head>
                        <meta charset = "utf-8" >
                          <title> List of species </title >
                        </head >
                        <body>
                        <body style="background-color: LimeGreen">
                        <p>Total number of species: {len(species)}</p>
                        <p>Limit of species selected: {len(species)}</p>
                        <p>Name(s) of the species:</p>
                        </body>
                        </html>
                        """
                error_code = 200
                for name in species:
                    contents += f"""<p>- {name["common_name"]}<p>"""
                contents += f"""<a href="/">Main page</a>"""  # return to main page -> index.html
            elif int(third_argument) < 0 or int(third_argument) > len(species):   # 3rd argument not in range
                contents = Path('Error.html').read_text()
                error_code = 404
            else:  # if 3arg in range, print 3arg species
                contents = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title> List of species </title>
                        </head>
                        <body style="background-color: limegreen">
                        <p>Total number of species is: {len(species)} </p>
                        <p>The limit you have selected is:{third_argument}</p>
                        <p>The names of the species are:</p>
                        </body></html>
                        """
                error_code = 200
                for name in species[:int(third_argument)]:
                    contents += f"""<p>- {name["common_name"]}<p>"""
                contents += f"""<a href="/">Main page</a>"""
        elif first_argument == "/karyotype":
            ENDPOINT = "info/assembly/"  # final '/' because introduced in variable karyotype (line 99)
            second_argument = arguments[1]
            third_argument = second_argument.split("=")[1]
            if third_argument == "":  # no argument introduced
                contents = Path('Error.html').read_text()
                error_code = 404
            else:
                try:  # check if available
                    karyotype = species_get(ENDPOINT + third_argument + PARAMS)["karyotype"]
                    contents = f"""
                               <!DOCTYPE html>
                               <html lang = "en">
                               <head>
                               <meta charset = "utf-8" >
                                 <title> Karyotype </title >
                               </head >
                               <body>
                               <body style="background-color: DeepSkyBlue">
                               <p>The names of the chromosomes are:</p>
                               </body>
                               </html>
                               """
                    error_code = 200
                    for chromosome in karyotype:
                        contents += f"""<p>- {chromosome}<p>"""
                    contents += f"""<a href="/">Main page</a>"""  # return main page -> index.html
                except KeyError:  # if not available, error page
                    contents = Path('Error.html').read_text()
                    error_code = 404
        elif first_argument == "/chromosomeLength":
            ENDPOINT = "/info/assembly/"  # add '/' so in line 131 is correct the path
            second_argument = arguments[1]
            third_argument, fourth_argument = second_argument.split("&")
            species = third_argument.split("=")[1]
            chromosome = fourth_argument.split("=")[1]

            if species == "" or chromosome == "":  # if specie and/or chromosome left in blank
                contents = Path('Error.html').read_text()
                error_code = 404
            else:  # if none is blank
                try:  # check if arguments available
                    chromo_len = species_get(ENDPOINT + species + PARAMS)["top_level_region"]  # path key obtained
                    contents = ""
                    for element in chromo_len:
                        if element["coord_system"] == "chromosome":  # access to key coord_system when 'chromosome'
                            if element["name"] == chromosome:  # specified chromosome variable
                                contents = f"""
                                        <!DOCTYPE html>
                                        <html lang = "en">
                                        <head>
                                          <meta charset = "utf-8" >
                                          <title> Chromosome length </title >
                                        </head >
                                        <body>
                                        <body style="background-color: darkviolet">
                                        </body>
                                        </html>
                                        """
                                contents += f"""<p>Length of chromosome: {chromosome} of {species} is: {element['length']}</p>"""
                    error_code = 200
                    if contents == "":
                        contents = Path('Error.html').read_text()
                    contents += f"""<a href="/">Main page</a>"""

                except KeyError:  # if not available, error page
                    contents = Path('Error.html').read_text()
                    error_code = 404
        elif first_argument == "/geneSeq":
            try:  # check if value in endpoint
                ENDPOINT = "xrefs/symbol/homo_sapiens/"
                second_argument = arguments[1]
                third_argument = second_argument.split("=")[1]
                if third_argument == "":  # if nothing inserted, error page thrown
                    contents = Path('Error.html').read_text()
                    error_code = 404
                elif third_argument.isdigit() is True:  # if number inserted, error thrown
                    contents = Path('Error.html').read_text()
                    error_code = 404
                else:  # everything correct
                    sequence = species_get(ENDPOINT + third_argument + PARAMS)[0]
                    contents = f"""
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="utf-8">
                                    <title>Gene sequence</title>
                                </head>
                                <body style="background-color: darkorange">
                                </body></html>
                                """
                    contents += f"""<b>The sequence of gene {sequence["id"]} known as {third_argument} is: <b>"""
                    ENDPOINT = "/sequence/id/"  # put '/' at the end of endpoints
                    sequence_1 = species_get(ENDPOINT + sequence["id"] + PARAMS)
                    contents += f"""<p> <textarea readonly rows="40" cols="100"> {sequence_1["seq"]} </textarea>"""
                    error_code = 200

            except IndexError:
                contents = Path('Error.html').read_text()
                error_code = 404
        elif first_argument == "/geneInfo":
            try:
                ENDPOINT = "xrefs/symbol/homo_sapiens/"
                second_argument = arguments[1]
                third_argument = second_argument.split("=")[1]
                if third_argument == "":  # if nothing inserted, error page thrown
                    contents = Path('Error.html').read_text()
                    error_code = 404
                elif third_argument.isdigit() is True:  # if number inserted, error thrown
                    contents = Path('Error.html').read_text()
                    error_code = 404
                else:  # if everything correct
                    sequence = species_get(ENDPOINT + third_argument + PARAMS)[0]
                    contents = f"""<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="utf-8">
                                        <title> Gene information </title>
                                    </head>
                                    <body style="background-color: aqua">
                                    </body></html>"""
                    contents += f"""<b> The information about gene {third_argument} is: <b>"""
                    ENDPOINT = "lookup/id/"
                    sequence_1 = species_get(ENDPOINT + sequence["id"] + PARAMS)
                    gene_length = int(sequence_1["end"]) - int(sequence_1["start"])
                    contents += f"""The start of the gene is: {sequence_1["start"]} </p>"""
                    contents += f"""The end of the gene is: {sequence_1["end"]} </p>"""
                    contents += f"""The length of the gene is: {gene_length} </p>"""
                    contents += f"""The ID of the gene is: {sequence_1["id"]} </p>"""
                    contents += f"""The gene is in the chromosome: {sequence_1["seq_region_name"]}"""
                    error_code = 200
            except IndexError:
                contents = Path('Error.html').read_text()
                error_code = 404
        elif first_argument == "/geneCalc":
            try:
                ENDPOINT = "xrefs/symbol/homo_sapiens/"
                second_argument = arguments[1]
                third_argument = second_argument.split("=")[1]
                if third_argument == "":  # if blank, error thrown
                    contents = Path('Error.html').read_text()
                    error_code = 404
                elif third_argument.isdigit() is True:
                    contents = Path('Error.html').read_text()
                    error_code = 404
                else:  # if everything correct
                    sequence = species_get(ENDPOINT + third_argument + PARAMS)[0]
                    contents = f"""<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="utf-8">
                                        <title> Gene calculations </title>
                                    </head>
                                    <body style="background-color: cornflowerblue">
                                    </body></html>"""
                    contents += f"""<b> The calculations of the gene {third_argument} are: </b>"""
                    ENDPOINT = "sequence/id/"
                    sequence_1 = species_get(ENDPOINT + sequence["id"] + PARAMS)
                    seq = Seq(sequence_1["seq"])
                    contents += f"""<p> Length of the gene is: {seq.len()} </p>"""
                    bases = ["A", "C", "T", "G"]
                    for base in bases:
                        base_percentage = round(seq.count_base(base) * 100 / seq.len(), 2)
                        contents += f"""The percentage of base {base} is: {base_percentage} %<br>"""
                    error_code = 200
            except IndexError:
                contents = Path('Error.html').read_text()
                error_code = 404

        else:
            contents = Path('Error.html').read_text()
            error_code = 404

        self.send_response(error_code)
        self.send_header('Content-Type', "text/html")
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