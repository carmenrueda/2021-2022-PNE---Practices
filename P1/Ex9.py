from Seq1 import Seq
import os

print("---Exercise 9---")


gene_list = ["U5", "FRAT1", "FXN", "ADA", "RNU6_269P"]
for gene in gene_list:
    s = Seq()
    filename = os.path.join("..", "Genes", f"{gene}.txt")
    s.read_fasta(filename)

    print(f"Gene: {gene}")
    print(f"Sequence: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev: {s.reverse()}")
    print(f"\tComp: {s.complement()}")
