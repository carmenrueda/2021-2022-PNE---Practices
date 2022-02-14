from pathlib import Path
filename = input("Enter a file: ")
try:
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines()
    head = lines[0]
    print(f"Head of the {filename} file: ")
    print(head)
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")
except IndexError:
    print(f"[ERROR]: file '{filename}' is empty")