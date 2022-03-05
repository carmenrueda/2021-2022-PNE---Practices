from Seq1 import Seq

print("---Exercise 9---")

FOLDER = "../Session-04/"
FILENAME = ["U5", "FRAT1", "FXN", "ADA", "RNU6_269P"]
for e in FILENAME:
    s = Seq()
    s.read_fasta(FOLDER, FILENAME)

    print(f"Sequence: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"Rev: {s.reverse()}")
    print(f"Comp: {s.complement()}")