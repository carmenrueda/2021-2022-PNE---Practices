import socket
import termcolor

IP = "127.0.0.1"
PORT = 8080

def process_client(s):

    #HTTP Request

    req_bytes = s.recv(2048)
    req = req_bytes.decode()

    print("Message FROM CLIENT: ")

    lines = req.splitlines()
    req_line = lines[0]
    slices = req_line.split(" ")
    method = slices[0] #GET
    path = slices[1] #directory/otherfile.html
    version = slices[2] #HTTP/1.0
    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")

    #HTTP Response
    status_line = "HTTP/1.1 200 OK\n"
    header = "Content-Type: text/plain\n" #tipo del contenido: texto plano
    body = "Hello from my first web server!\n"
    header += f"Content-Length: {len(body)}\n" #longitud de la respuesta en bytes

    response = status_line + header + "\n" + body
    response_bytes = response.encode()
    client_socket.send(response_bytes)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("SEQ Server configured!")

try:
    while True:
        print("Waiting for clients....")
        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()

except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()