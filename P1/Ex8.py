from Seq1 import Seq

print("---Exercise 8---")

seq_list = [Seq(), Seq("ACTGAGGTGCAA"), Seq("Invalid sequence")]
for i, seq in enumerate(seq_list):
    print(f"Sequence {i}: (Length: {seq.len()}) {seq}")
    print(f"\tBases: {seq.count()}")
    print(f"\tRev: {seq.reverse()}")
    print(f"\tComp: {seq.complement()}")