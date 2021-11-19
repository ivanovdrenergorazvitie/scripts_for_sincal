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
a = [[3193, 5.40749625, -1.3530675, 3], [3193, 5.344496250000001, -1.3530675, 2], [3193, 5.344496250000001, -1.2555675, 1]]
lstdict = [{ "name": "Klaus", "age": 32 },{ "name": "Elijah", "age": 33 },{ "name": "Kol", "age": 28 },{ "name": "Stefan", "age": 8 }]
# print(next(x for x in lstdict if x["name"] == "Klaus"))
print(next(a[x] for x in range(len(a)) if a[x][3] == 1))
print(a)


#
# a = [[1], [2], [3]]
# a[0] += [{'d': [1]}]
# print(a[0])