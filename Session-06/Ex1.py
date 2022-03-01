class Seq:

    BASES_ALLOWED = ["A", "C", "G", "T"]

    def valid_bases(self, bases):

    def __init__(self, bases):
        self.bases = bases

    def __str__(self):
        return self.bases

    def len(self):
        return len(self.bases)

class Gene(Seq):

    def __init__(self, bases, name=""):
        super().__init__(bases)
        self.name = name
        print("New gene created")

    def __str__(self):
        return self.name + "-" + self.bases

s = Seq("AGTACACTGGT")
g = Gene("CGTAAC", "FRAT1")

print(f"Sequence: {s}")
print(f"Gene: {g}")


