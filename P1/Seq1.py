class Seq:
    BASES_ALLOWED = ["A", "C", "G", "T"]
    COMPLEMENT_BASES = {"A": "T", "C": "G", "T": "A", "G": "C"}

    @staticmethod
    def valid_sequence(sequence):
        valid = len(sequence) != 0
        i = 0
        while valid and i < len(sequence):
            if sequence[i] not in Seq.BASES_ALLOWED:
                valid = False
            i += 1
        return valid

    def __init__(self, sequence="NULL"):
        if sequence == "NULL":
            self.sequence = sequence
            print("NULL sequence created!")
        elif Seq.valid_sequence(sequence):
            self.sequence = sequence
            print("New sequence created!")
        else:
            self.sequence = "ERROR"
            print("Invalid sequence detected!")

    def __str__(self):
        return self.sequence

    def len(self):
        if self.sequence == "NULL" or self.sequence == "ERROR":
            return 0
        return len(self.sequence)

    def count_bases(self, bases):
        if self.sequence == "NULL" or self.sequence == "ERROR":
            return 0
        return self.sequence.count(bases)

    def count(self):
        result = {}
        if self.sequence == "NULL" or self.sequence == "ERROR":
            for base in Seq.BASES_ALLOWED:
                result[base] = 0
        else:
            for base in Seq.BASES_ALLOWED:
                result[base] = self.count_bases(base)
        return result

    def reverse(self):
        if self.sequence == "NULL" or self.sequence == "ERROR":
            return self.sequence
        return self.sequence[::-1]

    def complement(self):
        if self.sequence == "NULL" or self.sequence == "ERROR":
            return self.sequence
        result = ""
        for base in self.sequence:
            result += Seq.COMPLEMENT_BASES[base]
        return result

    def read_fasta(self, file_name):
        from pathlib import Path

        file_contents = Path(file_name).read_text()
        lines = file_contents.splitlines()
        body = lines[1:]
        self.sequence = ""
        for line in body:
            self.sequence += line
