inplist = 47
listus = []
"""
ВВОД
"""
while inplist != ['0']:
    inplist = input('0 + Enter - остановоцка: ').split(' ')
    print(inplist)
    if inplist == ['0']:
        continue

    listus0 = []
    for i in inplist:
        inpd = {}
        inpd[i] = []
        listus0 += [inpd]
    listus0[0][inplist[0]] = [0.001]
    listus += [listus0]
    print(listus)
z = listus
"""
Список самых длинных цепочек
"""
nc = 0
l = []
nl = []
for i in range(len(z)):
    no = len(z[i])

    if no > nc:
        nc = no
        l = []
    if no == nc:
        l += [i]
print(l)
print(no)

"""
Задаем уставки самых длинных цепочек
"""
for j in l:
    for i in range(1, no):
        key = (str(z[j][i]).split(':')[0])[2:-1]
        z[j][i][key] = [float(str(0.1 * i)[:3])]
"""
Список оставшихся цепочек
"""
for i in range(len(z)):
    if i not in l:
        nl += [i]
print(nl)
"""
Задаем уставки оставшихся цепочек
"""
for j in nl:
    fKey = z[j]     # Забираем список словарей
    for i in range(1, len(z[j])):

        t1 = 0
        key1 = (str(z[j][i]).split(':')[0])[2:-1]
        for h in range(len(z)):
            if z[h] == fKey:
                continue
            else:
                for k in range(1, len(z[h])):
                    key2 = (str(z[h][k]).split(':')[0])[2:-1]
                    if z[h][k][key2] == []:
                        continue
                    if key1 == key2:
                        t1 = z[h][k][key2]
        if t1 == 0:
            if z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]] < [float(str(0.1 * i)[:3])]:
                z[j][i][key1] = [float(str(0.1 * i)[:3])]
            else:
                z[j][i][key1] = [float(z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + 0.1]
        if t1 != 0:
            z[j][i][key1] = t1
for i in z:
    print(i)
