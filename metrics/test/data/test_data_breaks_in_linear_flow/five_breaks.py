for i in range(10):
    print(i)

while True:
    print("looping...")

if False:
    print("True")
    if "nested" == "if":
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
except:
    print("failed")
