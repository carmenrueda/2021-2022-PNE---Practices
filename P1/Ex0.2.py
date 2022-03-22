from Seq1 import Seq

str_list = ["ACCTGC", "Hello? Am I a valid sequence?"]
sequence_list = []

for st in str_list:
    if Seq.valid_sequence(st):
        sequence_list.append(Seq(st))
    else:
        sequence_list.append(Seq("ERROR"))

for i in range(0, len(sequence_list)):
    print("Sequence", str(i) + ":", sequence_list[i])


#otra forma pero sin new seq created ni invalid seq detected:

for i, seq in enumerate(str_list):
    if Seq.valid_sequence(seq):
        print(f"Sequence {i+1}: {seq}")
    else:
        print(f"Sequence {i+1}: ERROR")


