class Seq:
    BASES_ALLOWED = ['A', 'C', 'G', 'T']
    BASES_COMPLEMENTS = {"A": "T", "C": "G", "T": "A", "G": "C"}

    @staticmethod
    def are_bases_ok(bases):
        ok = len(bases) != 0
        i = 0
        while ok and i < len(bases):
            if bases[i] not in Seq.BASES_ALLOWED:
                ok = False
            i += 1
        return ok

    def __init__(self, bases="NULL"):
        if bases == "NULL":
            self.bases = bases
            print("NULL sequence created!")
        elif Seq.are_bases_ok(bases):
            self.bases = bases
            print("New sequence created!")
        else:
            self.bases = "ERROR"
            print("INVALID sequence detected!")

    def __str__(self):
        return self.bases  # str

    def len(self):
        if self.bases == "NULL" or self.bases == "ERROR":
            return 0
        return len(self.bases)

    def count_base(self, base):
        if self.bases == "NULL" or self.bases == "ERROR":
            return 0
        return self.bases.count(base)

    def count(self):
        result = {}
        for base in Seq.BASES_ALLOWED:
            result[base] = self.count_base(base)
        return result

    def reverse(self):
        if self.bases == "NULL" or self.bases == "ERROR":
            return self.bases
        return self.bases[::-1]

    def complement(self):
        if self.bases == "NULL" or self.bases == "ERROR":
            return self.bases

        result = ""
        for base in self.bases:
            result += Seq.BASES_COMPLEMENTS[base]
        return result

    def read_fasta(self, file_name):
        from pathlib import Path

        file_contents = Path(file_name).read_text()
        lines = file_contents.splitlines()
        body = lines[1:]
        self.bases = ""
        for line in body:
            self.bases += line

    def info(self):
        result = f"Sequence: {self.bases}\n"
        result += f"Total length: {self.len()}\n"
        for base, count in self.count().items():
            result += f"{base}: {count} ({((count * 100) / self.len()):.1f}%)\n"
        return result


