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
    s.read_fasta(FOLDER, e)

    msg = str(s)
    sep = []
    for i in range(0, 50, 10):
        sep.append(msg[i:i+10])

    print("To server: Sending", e, "gene to the server... ")
    response = c.talk(msg)
    print("To server:", sep)