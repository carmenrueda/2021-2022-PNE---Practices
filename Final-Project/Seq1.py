from pathlib import Path

class Seq:

    BASES = ['A', 'C', 'G', 'T']
    COMPLEMENTARY_BASE = {"A": "T", "C": "G", "T": "A", "G": "C"}

    @staticmethod
    def valid_bases(seq):
        if len(seq) != 0:
            valid = True
            n = 0
            while valid and n < len(seq):
                if seq[n] not in Seq.BASES:
                    valid = False
            n += 1
        return valid

    def __init__(self, seq="NULL"):
        if seq == "NULL":
            self.seq = seq
            print("NULL seq!")
        elif Seq.valid_bases(seq):
            self.seq = seq
            print("New seq!")
        else:
            self.seq = "ERROR"
            print("INVALID seq!")

    def __str__(self):
        return self.seq  # str

    def length(self):
        if self.seq == "NULL" or self.seq == "ERROR":
            return 0
        else:
            return len(self.seq)

    def count_bases(self, seq):
        if self.seq == "NULL" or self.seq == "ERROR":
            return 0
        else:
            return self.seq.count(seq)

    def count(self):
        result = {}
        for seq in Seq.BASES:
            result[seq] = self.count_bases(seq)
        return result

    def reverse(self):
        if self.seq == "NULL" or self.seq == "ERROR":
            return self.seq
        else:
            return self.seq[::-1]

    def complement(self):
        if self.seq == "NULL" or self.seq == "ERROR":
            return self.seq
        complement_seq = ""
        for nucleotide in self.seq:
            complement_seq += Seq.COMPLEMENTARY_BASE[nucleotide]
        return complement_seq

    def read_fasta(self, filename):
        contents = Path(filename).read_text()
        lines = contents.splitlines()
        body = lines[1:]
        self.seq = ""
        for line in body:
            self.seq += line

    def info(self):
        result = f"Total length: {self.length()}\n"
        most_repeated_base = None
        for nucleotide, count in self.count().items():
            result += f"{nucleotide}: {count} ({((count * 100) / self.length()):.1f}%)\n"
            if most_repeated_base:
                if count > self.count_bases(most_repeated_base):
                    most_repeated_base = nucleotide
            else:
                most_repeated_base = nucleotide
        result += f"Most frequent base: {most_repeated_base}"
        return result

    def percentage_base(self, seq):
        result = (self.count_bases(seq) * 100) / self.length()
        return round(result, 2)

