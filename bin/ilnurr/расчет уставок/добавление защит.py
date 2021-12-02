# a = 'a'
# b = 'b'
# c = 'c'
# d = 'd'
# l = 'l'
# list = [[a, l], [a, c], [b]]

usl1 = int(input('0 - полуавтоматический ввод данных, 1 - заранее вбитые данные: '))
usl2 = usl1

"""
Сюда вставляем данные, если они есть
"""
list = [['L383', 'L363']]
a = 'L357'
d = 'L363'
if usl1 == 0:
    list = []

while usl1 == 0:
    inplist = input('Составление цепей защит(0 + Enter - остановоцка): ').split(' ')
    if inplist == ['']:
        iplist = []
        usl1 = 1
        continue
    print(inplist)
    if inplist == ['0']:
        usl1 = 1
        continue


    listus0 = []
    listus0 += [inplist]
    list += listus0
    print(list)

while usl2 == 0:
    inplist = input('Первое значение - родительская защита, второе - новообнаруженное (0 + Enter - остановоцка): ').split(' ')
    if inplist == ['0']:
        usl2 = 1
        continue
    a = inplist[0]
    d = inplist[1]
    print(a, d)


i = -1
f = 0
usl3 = True
while usl3 is True:
    i += 1
    if list == []:
        list.insert(i, [a])
        list[i] += [d]
    elif list[i][-1] == a:
        list[i] += [d]
        f += 1

    if len(list) - 1 == i:
        if f == 0:
            list.insert(i, [a])
            list[i] += [d]
        usl3 = False
print(list)