import Seq0
filename = Seq0.valid_filename()
sequence = Seq0.seq_read_fasta(filename)
reverse = Seq0.seq_reverse(sequence)
print("The reversed string of", sequence[:20], "=", reverse)




