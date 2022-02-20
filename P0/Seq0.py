from typing import List


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

def seq_count_base(seq, base): #4
    list_bases = ["A", "C", "G", "T"]
    for n in list_bases:
        seq_count = n.count(seq)
    return seq_count


def seq_count(seq): #5
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for n in seq:
        d[n] += 1
    return d


def seq_reverse(seq): #6
    seq = seq[:20]
    rev = ""
    for i in reversed(seq):
        rev += i
    return rev

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
