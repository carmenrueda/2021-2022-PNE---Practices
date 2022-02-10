import Seq0

FOLDER = "../Session-04/"
list_genes = ["U5", "FRAT1", "ADA", "FXN", "RNU6_269P"]
list_length = []
for l in list_genes:
    length = (len(Seq0.seq_read_fasta(FOLDER + l + ".txt")))
    list_length.append(length)

zipped = list(zip(list_genes, list_length))
for l in zipped:
    print("Gene", l[0], "---> Length:", l[1])


