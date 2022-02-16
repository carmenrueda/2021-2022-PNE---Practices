import Seq0
filename = Seq0.valid_filename()
sequence = Seq0.seq_read_fasta(filename)
most_frequent_base = Seq0.most_freq_base(sequence)
print(most_frequent_base)