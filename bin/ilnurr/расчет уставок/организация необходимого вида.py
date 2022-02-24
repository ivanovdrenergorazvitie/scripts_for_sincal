# a = [['L357', 'L363'], ['L383', 'L363']]
a = [['L357', '2T3472']]
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