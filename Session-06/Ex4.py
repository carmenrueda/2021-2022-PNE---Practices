import termcolor
from P1 import Seq


def generate_seq(pattern, number):
    seq_list= []
    for _ in range(1, number + 1):
        seq_list.append(Seq(pattern * number))
    return seq_list


def print_seq(seq_list, color):
    for index, seq in enumerate(seq_list):
        termcolor.cprint(f"Sequence {index}: (Length {seq.len()}) {seq}", color)


seq_list1 = generate_seq("A", 3)
seq_list2 = generate_seq("AC", 5)

termcolor.cprint("List 1:", 'blue')
print_seq(seq_list1, 'blue')

print()
print("List 2:", 'green')
print_seq(seq_list2, 'green')