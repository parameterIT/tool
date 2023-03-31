def method1():
    if a:  # 1
        method1()  # 2
    else:
        pass
    for i in range(10):  # 3
        break  # 4
    while True:  # 5
        method1()  # 6


def method2():
    if a:  # 1
        method2()  # 2
    elif b:
        method2()  # 3
    else:
        method2()  # 4
    while True:  # 5
        for i in range(10):  # 6
            pass


def method3():
    pass
