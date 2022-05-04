import json
import termcolor
from pathlib import Path

# -- Read the json file
jsonstring = Path("people-1.json").read_text() #str

# Create the object person from the json string
person = json.loads(jsonstring) # dict = {'Firstname': 'Troll', 'Lastname':'Face and 'age':37}

# -- Read the Firtname
firstname = person['Firstname']
lastname = person['Lastname']
age = person['age']

# Print the information on the console, in colors
print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)