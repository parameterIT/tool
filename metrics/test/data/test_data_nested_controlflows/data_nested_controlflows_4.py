j = 4

match j:
    case 1:
        j += 3
    case 2:
        j += 2
    case 3:
        j += 1
    case 4:
        if j < 5:
            for i in range(j + 1):
                print(i)
                if i == j:
                    print("Hello World! This is a test for our tool BYOQM!")
    case 5:
        j -= 1
