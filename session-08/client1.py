import socket

SERVER_IP = "localhost" #IP del servidor pq el cliente inicia la comunicacion y tiene q conocer donde esta el servidor
SERVER_PORT = 8081 #PORT tiene que ser distinto

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket sin inicializar
client_socket.connect((SERVER_IP, SERVER_PORT)) #en lugar de hacer un bind como en el servidor, hacemos un connect

msg = "Hello from the client"
msg_bytes = str.encode(msg) #encode transforma un string en bytes
client_socket.send(msg_bytes) #envia los bytes al servidor

msg_bytes = client_socket.recv(2048)  # recibe los bytes que me envia el cliente, pueden ser como max 2048 bytes (1024-2048-4096)
msg = msg_bytes.decode("utf-8")  # decodificar los bytes en formato utf-8, con tildes, ñ...
print(f"Message from server: {msg}")

client_socket.close()