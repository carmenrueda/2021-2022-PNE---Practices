class Seq:

    BASES_ALLOWED = ["A", "C", "G", "T"] #Propiedad/Atributo de clase (estático), común a toda la clase

    @staticmethod
    def valid_bases(bases):
        i = 0
        valid = len(bases[i]) != 0
        while valid and i < len(bases):
            if bases[i] not in Seq.BASES_ALLOWED: #si saco fuera de la clase la lista de bases allowed no me hace falta poner Seq. cuando la llame
                valid = False
            i += 1
        return valid

    def __init__(self, bases):
        if Seq.valid_bases(bases):
            self.bases = bases #Propiedad/Atributo de objeto particular
            print("New seq created")
        else:
            self.bases = "ERROR"
            print("Incorrect seq")


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

