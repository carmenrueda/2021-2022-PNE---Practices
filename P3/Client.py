from seq_client import Client

SERVER_IP = "localhost"
SERVER_PORT = 8081
BASES = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["ADA", "FRAT1", "U5", "RNU6_269P", "FXN"]

c = Client(SERVER_IP, SERVER_PORT)
print(c)

for n in range(5):
    c.debug_talk(f"GET {n}")
    print()

c.debug_talk(f"COMP {BASES}")
print()

c.debug_talk(f"REV {BASES}")
print()

for gene in GENES:
    c.debug_talk(f"GENE {gene}")
    print()