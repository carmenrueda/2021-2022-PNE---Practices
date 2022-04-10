import socket
import termcolor
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080


def http_request(client_socket):

    req_bytes = client_socket.recv(2048)
    req = req_bytes.decode()

    print("Message FROM CLIENT: ")

    lines = req.splitlines()
    req_line = lines[0]
    slices = req_line.split(" ")
    method = slices[0]
    path = slices[1]
    version = slices[2]
    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")

def process_client(client_socket):

    #HTTP Request

    req_bytes = client_socket.recv(2048)
    req = req_bytes.decode()

    print("Message FROM CLIENT: ")

    lines = req.splitlines()
    req_line = lines[0]
    slices = req_line.split(" ")
    method = slices[0]
    path = slices[1]
    version = slices[2]
    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")

    #HTTP Response

    body = ""
    if path == "/info/A":
       body = Path("A.html").read_text()
    elif path == "/info/C":
       body = Path("C.html").read_text()

    status_line = "HTTP/1.1 200 OK\n"
    header = "Content-Type: text/html\n"
    header += f"Content-Length: {len(body)}\n"
    response = status_line + header + "\n" + body
    response_bytes = response.encode()
    client_socket.send(response_bytes)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

try:
    while True:
        print("Waiting for clients....")
        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()

except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()