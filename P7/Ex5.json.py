import http.client
import json
from http import HTTPStatus
from Seq1 import Seq

GENES_DICT = {"SRCAP": "ENSG00000080603",
             "FRAT1": "ENSG00000165879",
             "ADA": "ENSG00000196839",
             "FXN": "ENSG00000165060",
             "RNU6_269P": "ENSG00000212379",
             "MIR633": "ENSG00000207552",
             "TTTY4C": "ENSG00000228296",
             "RBMY2YP": "ENSG00000227633",
             "FGFR3": "ENSG00000068078",
             "KDR": "ENSG00000128052",
             "ANK2": "ENSG00000145362"}

for GENE in GENES_DICT:

    SERVER = 'rest.ensembl.org'
    ENDPOINT = f"/sequence/id/{GENES_DICT[GENE]}"
    PARAMS = '?content-type=application/json'

    print(f"\nServer: {SERVER}")
    print(f"URL: {SERVER}{ENDPOINT}{PARAMS}")

    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", ENDPOINT + PARAMS)
        response = conn.getresponse()

        if response.status == HTTPStatus.OK:
            print(f"Response received!: {response.status} {response.reason}\n")
            print()

            data = response.read().decode("utf-8")
            data = json.loads(data)

            print(f"Gene: {GENE}")
            print(f"Description: {data['desc']}")

            sequence = Seq(data['seq'])
            print(sequence.info())

        else:
            print(f"Invalid response")

    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()