import http.client
import json
from http import HTTPStatus

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

GENE = "MIR633"

SERVER = 'rest.ensembl.org'
ENDPOINT = f"/sequence/id/{GENES_DICT[GENE]}"
PARAMS = '?content-type=application/json'

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", ENDPOINT + PARAMS)

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()


response = conn.getresponse()

print(f"\nServer: {SERVER}")
print(f"URL: {SERVER + ENDPOINT + PARAMS}")

if response.status == HTTPStatus.OK:
    print(f"Response received!: {response.status} {response.reason}\n")
    print()

    data = response.read().decode("utf-8")
    data = json.loads(data)
    print(f"Gene: {GENE}")
    print(f"Description: {data['desc']}")
    print(f"Sequence: {data['seq']}")




