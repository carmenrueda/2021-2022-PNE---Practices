class Seq:

    def __init__(self, bases):
        self.bases = strbases

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

class Gene(Seq):

def __init__(self, strbases, name=""):
    super().__init__(strbases)
    self.name = name
    print("New gene created")

s1 = Seq("AGTACACTGGT")
g = Gene("CGTAAC")

print(f"Sequence 1: {s1}")
print(f"  Length: {s1.len()}")
print(f"Gene: {g}")
print(f"  Length: {g.len()}")

