import json
import termcolor
from pathlib import Path


jsonstring = Path("people-2.json").read_text() #str
person = json.loads(jsonstring) #dict

print()

termcolor.cprint("Name: ", 'green', end="")
print(person['Firstname'], person['Lastname'])

termcolor.cprint("Age: ", 'green', end="")
print(person['age'])

phoneNumbers = person['phoneNumber'] #list
termcolor.cprint("Phone numbers: ", 'green', end='')
print(len(phoneNumbers))


for i, num in enumerate(phoneNumbers):
    termcolor.cprint("  Phone {}:".format(i), 'blue', end='')
    print(num)
