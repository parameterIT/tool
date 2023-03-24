for i in range(10):  # 1
    break  # 2

while True:  # 3
    continue  # 4

if False:  # 5
    print("True")
    if "nested" == "if":  # 6
        pass
    elif "nested" == "elif":
        pass
    else:
        pass
elif True:
    print("False")
else:
    print("Neither true nor false")

try:
    print("will fail")
    raise ValueError
except:  # 7
    print("failed")
