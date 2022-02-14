from pathlib import Path
filename = input("Enter a file: ")
try:
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]
    total = 0
    for line in body:
        total += len(line)
    print(f"Total number of bases {total}")
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")
except IndexError:
    print(f"[ERROR]: file '{filename}' is empty")