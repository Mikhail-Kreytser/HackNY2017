def pow_mod(m, k, c):
    result = 1
    for i in range(0, k, +1):
        result = (result * m) % c
    return result


def decrypt(s, d, c):
    if s < 0 & s >= c:
        print("Something is wrong.")
        return -1
    return pow_mod(s, d, c)


def last_step(s):
    d = 1591
    c = 4819

    string = ""
    size = int(len(s) / 5) + 1
    for i in range(0, size, +1):
        temp = s[-5:]
        s = s[:-5]
        string += chr(decrypt(int(temp), d, c))
    print("Plain URL: ", string, "\n")
last_step("