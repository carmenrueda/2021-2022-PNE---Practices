N= 11
n1 = 0
n2 = 1
print(n1, end=" ")
print(n2, end=" ")
for i in range(2, N):
    num = n1 + n2
    print(num, end="")
    n1 = n2
    n2 = num
print()