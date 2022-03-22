from Seq0 import *

FOLDER = "../Genes/"
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
BASES = ["A", "C", "G", "T"]

for gene in GENES:
    filename = gene + ".txt"
    sequence = seq_read_fasta(FOLDER + filename)
    print(f"Gene {gene}:")
    for base in BASES:
        print(f"  {base}: {seq_count_base(sequence, base)}")
    print()