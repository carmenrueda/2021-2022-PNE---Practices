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


