def seq_count_base(seq, base):
    nucleotides = 0
    for n in seq:
        if n is ("A" or "C" or "G" or "T"):
            nucleotides += 1
    return nucleotides

seq = input("Enter a seq: ")
base = input("Enter a base: ")
print(seq_count_base(seq, base))