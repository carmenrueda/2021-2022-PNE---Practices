import Seq0
filename = Seq0.valid_filename()
sequence = Seq0.seq_read_fasta(filename)
base = input("Enter a base: ")
print(Seq0.seq_count_base(sequence, base))