class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases): #dont return anything in the init function

        # Initialize the sequence with the value
        # passed as argument when creating the object
        self.strbases = strbases
        if not self.valid_sequence():
            self.strbases = "ERROR"
            print("ERROR!!")
        else:
            print("New sequence created!")

    @staticmethod #so that it doesnt expect the class but a normal argument
    def valid_sequence2(sequence): #to check if correct before instantiating the class
        valid = True
        i = 0
        while i < len(sequence):
            c = sequence[i]
            if c != "A" and c != "C" and c != "G" and c != "T":
                valid = False
            i += 1
        return valid

    def valid_sequence(self): #as long as the method is inside the the class, it doesn't matter its location bc everything compiles at once #to check if correct after instantiating the class
        valid = True
        i = 0
        while i < len(self.strbases):
            c = self.strbases[i]
            if c != "A" and c != "C" and c != "G" and c != "T":
                valid = False
            i += 1
        return valid

    def __str__(self):
        """Method called when the object is being printed"""

        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)