from Client import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 4


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "127.0.0.1"
PORT = 8080
c = Client(IP, PORT)

FOLDER = "../Session-04/"
FILENAME = ["U5", "FRAT1", "FXN", "ADA", "RNU6_269P"]

for e in FILENAME:
    s = Seq()
    s.read_fasta(FOLDER, FILENAME)
    msg = str(s)
    print("To server: Sending U5 gene to the server... ")
    response = c.talk(msg)
    print(f"Response: {response}")
    print("To server:", msg)