def nesting1():
    x = 2
    if x:
        print("first nest")
        for i in range(10):
            print("second nest")
            while x:
                x -= 1
                print("third nest")
                if i == 0:
                    print("fourth nest")
    x = 3
    try:
        print("first nest")
        for i in range(10):
            print("second nest")
            while x:
                x -= 1
                print("third nest")
                if i == 0:
                    print("fourth nest")
    except:
        print("nope")
