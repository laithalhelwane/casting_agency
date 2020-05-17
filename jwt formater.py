def add_escape(str, long):
    ret = []
    for i in range(len(str)):
        ret.append(str[i])
        if (1+i) % long == 0:
            ret.append("\\\n")
    return "".join(ret)


'''
    script for split jwt to multi lines
'''
if __name__ == '__main__':
    long = int(input("Enter line long: "))
    str = input("Enter the JWT: ")
    print("\n\nOutput:\n\n")
    if long != 0:
        print(add_escape(str, long))
