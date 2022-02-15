class Dog:
    def __init__(self, the_name, the_age):
        self.name = the_name
        self.age = the_age

    def say_ur_name(self):
        print(f"I'm {self.name}, and I'm sitting right here.")

    def say_ur_age(self):
        print(f"I'm {self.age} years old.")

    def say_what_u_like(self):
        print(f"I like aritmetic")

    def multiply(self, first_operand, second_operand):
        print(f"Easy, the result is {first_operand + second_operand}")

ares = Dog("ares", 10)
ares.say_ur_name()
ares.say_ur_age()
ares.say_what_u_like()
ares.multiply(3,2)