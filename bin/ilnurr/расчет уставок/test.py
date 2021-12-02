#
# """
# СОСТАВЛЕНИЕ ЭКСЕЛЬ ДЛЯ УСТАВОК
# """
# import pandas as pd
# import openpyxl
#
# pd.options.mode.chained_assignment = None  # default='warn'
#
# file = 'ксымельная.xlsx'
#
#
# xl = pd.ExcelFile(file)
#
# print(xl.sheet_names)
#
# df1 = xl.parse('ProtOCSetting')
# df1.loc[0, 'I> Time t [s]'] = 0.2
# val = df1.loc[0, 'I> Time t [s]']
# print(df1)
# print(val)
# df1.to_excel('ff.xlsx', sheet_name='ProtOCSetting', index=False)

# """
# ФОРМИРОВАНИЕ ДЕРЕВА
# """
# e1 = {'El_a': 0.001}
#
# m = {}
# e2 = 'El_b'
# m[e2] = e1
# e2 = m
#
# m = {}
# e3 = 'El_c'
# m[e3] = e2
# e3 = m
#
#
# print(m)

# prices = [5, 12, 45]
# names = []
# for i, _ in enumerate(prices):
#     names.append("price"+str(i+1))
# dict = {}
# for name, price in zip(names, prices):
#     dict[name] = price
# for item in dict:
#     print(item, "=", dict[item])

#   Уставку времени
# print(z[0][0].values())


# Поиск в списке словарей
# a = [[3193, 5.40749625, -1.3530675, 3], [3193, 5.344496250000001, -1.3530675, 2], [3193, 5.344496250000001, -1.2555675, 1]]
# lstdict = [{ "name": "Klaus", "age": 32 },{ "name": "Elijah", "age": 33 },{ "name": "Kol", "age": 28 },{ "name": "Stefan", "age": 8 }]
# # print(next(x for x in lstdict if x["name"] == "Klaus"))
# print(next(a[x] for x in range(len(a)) if a[x][3] == 1))
# print(a)


#
# a = [[1], [2], [3]]
# a[0] += [{'d': [1]}]
# print(a[0])
# a = 'a'
# b = 'b'
# c = 'c'
# d = 'd'
# l = 'l'
# list = [[a, l], [a, c], [b]]
#
# i = -1
# f = 0
# usl2 = True
# while usl2 is True and i < len(list) - 1:
#     i += 1
#     if f == 1:
#         f = 0
#         continue
#     if list[i][0] == a:
#         if list[i][-1] == a:
#             list[i] += [d]
#             usl2 = False
#             break
#         else:
#             list.insert(i, [a])
#             list[i] += [d]
#             f = 1
#             usl2 = False
#             break
# print(list)




# plist = [{'a': [0.001]}, {'b': []}]
# print(str(plist[-1].keys())[12])
# if str(plist[-1].keys())[12] == 'b':
#     plist += [{'c': []}]
# print(plist)
# print(str(plist[-1].keys()).split('[')[1][:-2])
# print(plist[-1].keys())
e = [['a'], ['sda'], ['zxc'], ['as'], ['zxc'], ['a'], ['a']]
l = []
if len(e) > 1:
    c = []
    for c1 in range(len(e)):
        n = 0
        for c2 in range(len(e)):
            if e[c1] == e[c2]:
                n += 1
            if n > 1 and e[c1] == e[c2]:
                c += [c2]
    if len(c) > 1:
        c = set(c)
        c = list(c)

        for c3 in range(len(e)):
            if c3 not in c:
                l += [e[c3]]
print(l)