from Seq0 import *

FOLDER = "../Genes/"
filename = input("Enter a filename: ")
print(f"DNA file: {filename}")
sequence = seq_read_fasta(FOLDER + filename)
print(f"The first 20 bases are: {sequence[:20]}")
