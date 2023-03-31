def recurses():
    if recurses():
        recurses()
    else:
        recurses()

    print(recurses() + recurses())
    return recurses()


def does_neither():
    does_neither()


def nests():
    nests()
