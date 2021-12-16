a = [['e', 'f', 'd', 'c', 'a'], ['e', 'f', 'd', 'c', 'b'], ['k', 'g', 'd', 'c', 'a'], ['k', 'g', 'd', 'c', 'b'], ['e', 'f', 'z', 'l', 'c', 'a'], ['e', 'f', 'z', 'l', 'c', 'b'], ['k', 'g', 'z', 'l', 'c', 'a'], ['k', 'g', 'z', 'l', 'c', 'b'], ['h', 'l', 'c', 'a'], ['h', 'l', 'c', 'b']]
for i in range(len(a)):
    for j in range(len(a[i])):
        if j == 0:
            d = {}
            d[a[i][j]] = [0.001]
            a[i][j] = d
        else:
            d = {}
            d[a[i][j]] = []
            a[i][j] = d

print(a)