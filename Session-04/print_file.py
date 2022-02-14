from pathlib import Path
filename = input("Enter a file: ")
try:
    file_contents = Path(filename).read_text()
    print(file_contents)
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")