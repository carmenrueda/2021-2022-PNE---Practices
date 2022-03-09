import socket
import termcolor
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080
MAX_OPEN_REQUESTS = 5

n = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((IP, PORT))
    server_socket.listen(MAX_OPEN_REQUESTS)

    while True:
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()
        n += 1
        print(f"Connection {n} from ({client_address})")

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode("utf-8").replace("\n","").strip()
        splitted_cmd = request.split(" ")
        cmd = splitted_cmd[0]
        if cmd != "PING":
            arg = splitted_cmd[1]
        print(cmd)
        termcolor.cprint(f"Message from client: {request}", 'green')
        if cmd == "PING":
            response = "OK!!!\n"
        elif cmd == "GET":
            list_seq = ["ACGTGTGGGGTCAGTG", "ACCCGTGTGGCCCCA", "TGGGTTCAACGTG", "ACGTGCACCAACCCGT", "ACCCACAACACGTGT"]
            response = list_seq[int(arg)]
            print(response)
        elif cmd == "INFO":
            s = Seq(arg)
            response = f"Total length: {str(s.len())}\n"
            print(response)
        else:
            response = "Not available command is not available\n"

        response_bytes = str.encode(response)
        client_socket.send(response_bytes)

        client_socket.close()


except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")

except KeyboardInterrupt:
    print(f"Server stopped by the user")
    server_socket.close()