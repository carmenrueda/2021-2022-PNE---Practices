from typing import List
BASES = ["A", "C", "G", "T"]
COMPLEMENTS = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

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
    from pathlib import Path
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]
    sequence = ""
    for line in body:
        sequence += line
    return sequence

def seq_len(seq): #3
    return len(seq)

def seq_count_base(seq: str, base): #4
    return seq.count(base)

def seq_count(seq): #5 malllll donde esta html
    result = {}
    for base in BASES:
        result[base] = seq_count_base(seq, base)
    return result

def seq_reverse(seq): #6
    return seq[::-1]

def seq_complement(seq): #7
    result = ""
    for base in seq:
        result += COMPLEMENTS[base]
    return result

def most_freq_base(seq): #8
    max_base = None
    max_count = 0
    for base, count in seq_count(seq).items():
        max_base += base
        max_count += count
    return max_base