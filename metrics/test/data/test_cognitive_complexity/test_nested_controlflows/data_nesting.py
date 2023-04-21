def method1():
    x = 2
    if x: #1
        print("first nest")
        for i in range(10): #2
            print("second nest")
            while x: #3
                x -= 1
                print("third nest")
                if i == 0: #4
                    print("VIOLATION") #5
                    
def method2():
    if a: #1
        if k: #2
            print("NOT A VIOLATION")
    else:
        if b: #3
            print("NOT A VIOLATION")
        else:
            if c: #4
                print("NOT A VIOLATION")
            else:
                if d: #5
                    print("VIOLATION") #6
                    
def method3():
    if a: #1
        if b: #2
            if c: #3
                if d: #4
                    print("VIOLATION")
    if k: #6
        print("NOT A VIOLATION")

def method4():
    if a: #1
        try:
            if (k): #2
                print("NOT A VIOLATION")
        except: #3
            if b: #4
                print("NOT A VIOLATION")
            elif c:
                if d: #5
                    print("VIOLATION") #6
            
def method5():
    if a: #1
        try:
            if b: #2
                print("NOT A VIOLATION")
            elif c:
                if d: #3
                    print("VIOLATION") #4
        except: #5
            if (k): #6
                print("NOT A VIOLATION")
            
def method6():
    for i in range(10): #1
        while True: #2
            try:
                print("NOT A VIOLAITON")
            except: #3
                if a: #4
                    print("VIOLATION")
    if (b): #6
        print("NOT A VIOLATION")