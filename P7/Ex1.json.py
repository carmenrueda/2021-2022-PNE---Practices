import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'
PORT = 8080

print(f"\nConnecting to server: {SERVER}\n")

conn = http.client.HTTPConnection(SERVER, PORT)

try:
    conn.request("GET", ENDPOINT + PARAMS)

except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()


response = conn.getresponse()

print(f"Response received!: {response.status} {response.reason}\n")

data = response.read().decode("utf-8")
data = json.loads(data)

if data["ping"] == 1:
    print("ok database running")
else:
    print("ERROR database not running")


print(f"CONTENT: {data}")


