from Seq1 import Seq

print("---Exercise 5---")
seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, seq in enumerate(seq_list):
    print(f"Sequence {i}: (Length: {seq.len()}) {seq}")
    for base in Seq.BASES_ALLOWED:
        print(f"{base}: {seq.count_bases(base)}", end=" ")
