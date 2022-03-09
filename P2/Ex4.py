from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 4


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8081
c = Client(SERVER_IP, SERVER_PORT)

gene_list = ["U5", "FRAT1", "ADA"]

for gene in gene_list:
    s = Seq()
    s.read_fasta(f"../Genes/{gene}.txt")
    c.debug_talk(f"Sending {gene} Gene to the server...")
    c.debug_talk(str(s))
    print()