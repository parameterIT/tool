a = bool(1)
b = bool(0)
c = bool(0)
d = bool(1)


def returns_true():
    return bool(1)


def return_false():
    return bool(0)


if return_false() or returns_true():
    print(1)

if a or b or c:
    print(2)
elif b or c or d or a:
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
