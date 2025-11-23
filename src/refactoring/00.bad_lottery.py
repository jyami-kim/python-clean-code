import random

n = []
for i in range(6):
    x = random.randint(1, 45)
    while x in n:
        x = random.randint(1, 45)
    n.append(x)

m = []
for i in range(6):
    y = int(input("num: "))
    while y < 1 or y > 45 or y in m:
        print("bad num")
        y = int(input("num: "))
    m.append(y)

c = 0
for i in n:
    if i in m:
        c += 1

print("result:", n)
print("mine:", m)
if c == 6:
    print("1st")
elif c == 5:
    print("2nd")
elif c == 4:
    print("3rd")
elif c == 3:
    print("4th")
else:
    print("fail")

