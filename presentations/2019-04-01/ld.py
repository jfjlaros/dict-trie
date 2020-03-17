def lev(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)

    if a[-1] != b[-1]:
        return min(
            lev(a[:-1], b),
            lev(a, b[:-1]), 
            lev(a[:-1], b[:-1])) + 1

    return lev(a[:-1], b[:-1])


def xlev(a, b):
    d = [[i for i in range(len(b) + 1)]]
    for i in range(1, len(a) + 1):
        d.append([i] + [0] * len(b))

    for j in range(1, len(b) + 1):
        for i in range(1, len(a) + 1):
            if a[i - 1] != b[j - 1]:
                d[i][j] = min(
                    d[i - 1][j],
                    d[i][j - 1],
                    d[i - 1][j - 1]) + 1
            else:
                d[i][j] = d[i - 1][j - 1]

    for i in range(len(a) + 1):
        print(d[i])
    return d[i][j]


print(lev("ACGTTTA", "ATGTTCTA"))
print(xlev("ACGTTTA", "ATGTTCTA"))
