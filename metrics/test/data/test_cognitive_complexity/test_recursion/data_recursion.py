def recurses():
    recurses()  # 1
    recurses()  # 2
    recurses()  # 3

    print(recurses() + recurses())  # 4 5

    return recurses()  # 6


def does_neither():
    does_neither()


def nests():
    nests()
