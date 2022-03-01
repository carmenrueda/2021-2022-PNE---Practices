from P1 import *

def print_seq(seq_list):
    for index, seq in enumerate(seq_list):
        print(f"Sequence {index}: (Length {seq.len()}) {seq}")

def generate_seq(pattern, number):
    seq_list= []
    bases = pattern
    for _ in range(number):
        seq_list.append(Seq(bases))
        bases += pattern
    return seq_list


seq_list1 = generate_seq("A", 3)
seq_list2 = generate_seq("AC", 5)

print("List 1:")
print_seq(seq_list1)

print()
print("List 2:")
print_seq(seq_list2)