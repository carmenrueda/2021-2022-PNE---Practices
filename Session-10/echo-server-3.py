import socket
import termcolor

IP = "localhost"
PORT = 8081
MAX_OPEN_REQUESTS = 5

n = 0
clients = []
connections = 5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((IP, PORT))
    server_socket.listen(MAX_OPEN_REQUESTS)

    while n != connections:
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        n += 1
        clients.append(client_address)
        
        print(f"Connection {n} from ({client_address})")

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode("utf-8")
        print(f"Message from client: ", end="")
        termcolor.cprint(request,'green')

        response = f"ECHO: {request}\n"
        response_bytes = str.encode(response)
        client_socket.send(response_bytes)

        client_socket.close()

except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")

except KeyboardInterrupt:
    print(f"Server stopped by the user")
    server_socket.close()