import Seq0
filename = Seq0.valid_filename()
sequence = Seq0.seq_read_fasta(filename)[:20]
complement = Seq0.seq_complement(sequence)
print("Frag:", sequence)
print("Comp:", complement)

