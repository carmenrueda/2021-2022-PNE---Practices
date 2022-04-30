# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client
import json

SERVER = "https://rest.ensembl.org"
ENDPOINT = "/sequence/id/"
PARAMS = '?content-type=application/json'

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", ENDPOINT + PARAMS)
    gene_dict = {"SCARP": "ENSG00000080603",
                 "FRAT1": "ENSG00000165879",
                 "ADA": "ENSG00000196839",
                 "FXN": "ENSG00000165060",
                 "RNU6_269P": "ENSG00000212379",
                 "MIR633": "ENSG00000207552",
                 "TTTY4C": "ENSG00000228296",
                 "RBMYY2YP": "ENSG00000228296",
                 "FGFR3": "ENSG00000068078",
                 "KDR": "ENSG00000128052",
                 "ANK2": "ENSG00000145362"}

    for k, v in gene_dict.items():
        print(f"{k} : {v}")

    r1 = conn.getresponse()
    data1 = r1.read().decode("utf-8")
    data1 = json.loads(data1)


except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()
