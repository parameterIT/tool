def method1(arg1, arg2, arg3):
    pass


def method2(arg1, arg2, arg3, arg4):
    pass


print("this line should not matter")


##This one violates.
def method3(arg1, arg2, arg3, arg4, arg5):
    pass


##This one violates.
def method1(arg1, arg2, arg3, arg4, arg5, arg6):
    pass


def do_something(arg1, arg2, arg3):
    if True:
        i = 4
        i += 1
        if i <= 5:
            i += 1
