from P1 import *

def print_seq(seq_list):
    for index, seq in enumerate(seq_list):
        print(f"Sequence {index}: (Length {seq.len()}) {seq}")

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
print_seq(seq_list)