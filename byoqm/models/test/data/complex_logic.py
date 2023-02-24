a = bool(1)
b = bool(0)
c = bool(0)
d = bool(1)

if a or b or c:
    print(2)
elif b or c or d:
    print(3)

while b or c:
    print(3)


def method1():
    print(1)
    if a or b:
        print(1)

    if a and b or c:
        print(2)


method1()
