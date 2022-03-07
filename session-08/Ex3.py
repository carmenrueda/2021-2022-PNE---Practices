import socket
SERVER_IP = "localhost"
SERVER_PORT = 8081

while True:
    msg = input(">> ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    msg_bytes = str.encode(msg)
    client_socket.send(msg_bytes)

    client_socket.close()