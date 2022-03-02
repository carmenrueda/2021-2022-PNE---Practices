from Client import Client
from Seq1 import Seq
import termcolor

PRACTICE = 2
EXERCISE = 4
FILENAME = "../Session-04"


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "127.0.0.1"
PORT = 8080
c = Client(IP, PORT)

print("Sending a message to the server...")
response = c.talk("Testing!!!")
print(f"Response: {response}")