import Seq0

FOLDER = "../Session-04/"
list_genes = ["U5", "FRAT1", "ADA", "FXN", "RNU6_269P"]
for l in list_genes:
    print(len(Seq0.seq_read_fasta(FOLDER + l + ".txt")))
