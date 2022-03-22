from seq_client import Client

SERVER_IP = "localhost"
SERVER_PORT = 8080
BASES = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]


c = Client(SERVER_IP, SERVER_PORT)
print(c)

c.debug_talk("PING")

print()

for n in range(5):
    c.debug_talk(f"GET {n}")
    print()

c.debug_talk(f"INFO {BASES}")

print()

c.debug_talk(f"COMP {BASES}")

print()

c.debug_talk(f"REV {BASES}")

print()

for gene in GENES:
    c.debug_talk(f"GENE {gene}")
    print()