def seq_ping(): #1
    print("Ok")

def valid_filename(): #2
    exit = False
    while not exit:
        filename = input("What file do you want to open? ")
        try:
            f = open(filename, "r")
            exit = True
            return filename
        except FileNotFoundError:
            print("File does not exist. Provide another file.")

def seq_read_fasta(filename): #2
    seq = open(filename, "r").read()
    seq = seq[seq.find("\n"):].replace("\n", "")
    return seq

def seq_count_base(seq): #4
    seq = seq[seq.find("\n"):].replace("\n", "")
    nucleotides = 0
    for n in seq:
        if n is ("A" or "C" or "G" or "T"):
            nucleotides += 1
    return nucleotides

def seq_count(seq): #5
    seq = seq[seq.find("\n"):].replace("\n", "")
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for n in seq:
        d[n] += 1
    return d

def seq_reverse(seq): #6
    seq = seq[seq.find("\n"):].replace("\n", "")
    seq = seq[:20]
    reverse_seq = seq[len(seq)::-1]
    return reverse_seq

def seq_complement(seq): #7
    base_complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    new_seq = ""
    for e in seq:
        for k in base_complement:
            if k == e:
                new_seq += base_complement[k]
    return new_seq

def most_freq_base(seq): #8
    seq = seq[seq.find("\n"):].replace("\n", "")
    seq = list(seq)
    dict = {}
    count, base = 0, ''
    for n in seq:
        dict[n] = dict.get(n, 0)
        if dict[n] >= count:
            count, base = dict[n], n
    return n
