import socket
import termcolor
import os  # Operative System
from Seqclass import Seq

IP = "localhost"  # "127.0.0.1" para la máquina en la que se ejecuta
PORT = 8080
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]


def get_command(gene_number):
    gene = GENES[gene_number]
    sequence = Seq()
    file_name = os.path.join("..", "Genes", f"{gene}.txt")  # file_name = "../Genes/U5.txt"
    sequence.read_fasta(file_name)

    response = f"{sequence}\n"
    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configured!")

    while True:
        print(f"Waiting for clients...")
        (client_socket, client_address) = server_socket.accept()

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode("utf-8")

        try:
            slices = request.split(" ")
            command = slices[0]
            termcolor.cprint(f"{command}", 'green')
            response = ""

            if command == "PING" and len(slices) == 1:

                response = f"OK!\n"

            elif command == "GET" and len(slices) == 2:
                gene_number = int(slices[1])

                response = get_command(gene_number)

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
                file_name = os.path.join("..", "Genes", f"{gene}.txt")  # file_name = "../Genes/U5.txt"
                sequence.read_fasta(file_name)

                response = f"{sequence}\n"

            elif command == "LEN":
                if len(slices) == 1:
                    sequence = Seq()
                else:
                    bases = slices[1]
                    sequence = Seq(bases)

                response = f"{sequence.len()}\n"

            else:
                response = "Invalid command\n"

        except Exception:  # IndexError | ValueError
            response = "ERROR\n"

        print(response)
        response_bytes = str.encode(response)
        client_socket.send(response_bytes)

        client_socket.close()

except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")

except KeyboardInterrupt:
    print("Server stopped by the admin")

    server_socket.close()
