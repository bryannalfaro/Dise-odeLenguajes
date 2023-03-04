a = [[1,2],[3,4]]
b= [[1],[2]]
for i in range(0, len(a)):
    if i==0:
        a[i] = []
        b.extend(a)


print(a)
print(b)