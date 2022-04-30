# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'

print(f"\nConnecting to server: {SERVER}\n")

# Connect with the server
conn = http.client.HTTPConnection(SERVER)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", ENDPOINT + PARAMS) #we dont need to put server + endpoint + params
    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    data1 = r1.read().decode("utf-8")
    data1 = json.loads(data1)  # necesario pq cambia automaticamente a un integer cuando detecta str o float

    # -- Print the received data
    print(f"CONTENT: {data1}")

    if data1("ping") == 1:
        print("ok database running")
    else:
        print("ERROR database not running")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

