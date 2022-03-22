import socket

IP = "localhost" # 127.0.0.1 #la IP tiene que coincidir si tengo cliente y servidor en el mismo orde
PORT = 8081 # del 1 al 1024 estan reservados para el equipo #el port tiene que ser distinto si tengo cliente y servidor en el mismo orde, sino puede coincidir
MAX_OPEN_REQUESTS = 5 # puedo tener 5 conexiones abiertas a la vez (me comunico con 5 clientes), vinculado a listen()

n = 0 # cada vez que se conecta un nuevo cliente suma 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #me creo un socket, el canal de comunicacion para leer y escribir pero sin utilidad
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #el port esta siendo utilizado pero vuelvo a intentarlo

try:
    server_socket.bind((IP, PORT)) #oye socket, vinculate a la tuple de la IP de mi maquina y el PORT q use, ahora el socket se puede usar
    server_socket.listen(MAX_OPEN_REQUESTS) #las puertas se abren y puedo escuchar las peticiones de conexion de 5 clientes max

    while True: #se queda escuchando, atiende a un cliente, da la vuelta al bucle, se queda escuchando...
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept() #acepta la conexion de un cliente #devuelve el socket y la direccion del cliente
        n += 1 #se ha conectado un nuevo cliente
        print(f"Connection {n} from ({client_address})")

        msg_bytes = client_socket.recv(2048) #recibe los bytes que me envia el cliente, pueden ser como max 2048 bytes (1024-2048-4096)
        msg = msg_bytes.decode("utf-8") #decodificar los bytes en formato utf-8, con tildes, ñ...
        print(f"Message from client: {msg}")

        msg = "Hello from the server!"
        msg_bytes = str.encode(msg)
        client_socket.send(msg_bytes)

        client_socket.close()

except socket.error: #cualquier error relacionado con el socket
    print(f"Problems using port {PORT}. Do you have permission?")

except KeyboardInterrupt:
    print(f"Server stopped by the user")
    server_socket.close()