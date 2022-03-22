import socket
import termcolor
from seq_server import Seq
import os #modulo para interactuar con mi sistema operativo

IP = "localhost"
PORT = 8081
GENES = ["ADA", "FRAT1", "U5", "RNU6_269P", "FXN"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Seq Server configured!")

    while True:
        try:
            print(f"Waiting for clients at ({IP}:{PORT})...")
            (client_socket, client_address) = server_socket.accept()

            request_bytes = client_socket.recv(2048)
            request = request_bytes.decode("utf-8")

            slices = request.split(" ")
            command = slices[0]
            termcolor.cprint(f"{command} Command", 'green')

            if command == "PING":
                response = f"OK!\n"

            elif command == "GET":
                gene_number = int(slices[1])
                gene = GENES[gene_number]
                sequence = Seq()
                filename = os.path.join("..", "Genes", f"{gene}.txt") #"../GENES/U5.txt"
                sequence.read_fasta(filename)

                response = f"{sequence}\n"

            elif command == "INFO":
                bases = slices[1]
                sequence = Seq(bases)

                response = f"{sequence.info()}"

            elif command == "COMP":
                bases = slices[1]
                sequence = Seq(bases)

                response = f"{sequence.complement()}\n"

            elif command == "REV":
                bases = slices[1]
                sequence = Seq(bases)

                response = f"{sequence.reverse()}\n"

            elif command == "GENE":
                gene = slices[1]
                sequence = Seq()
                filename = os.path.join("..", "Genes", f"{gene}.txt")
                sequence.read_fasta(filename)

                response = f"{sequence}\n"

            elif command == "LEN":
                if len(slices) == 1:
                    sequence = Seq()
                else:
                    bases = slices[1]
                    sequence = Seq(bases)

                response = f"{sequence.len()}\n"

        except Exception:
            response ="ERROR\n"

        print(response)
        response_bytes = str.encode(response)
        client_socket.send(response_bytes)

        client_socket.close()


except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")

except KeyboardInterrupt:
    print(f"Server stopped by the user")
    server_socket.close()