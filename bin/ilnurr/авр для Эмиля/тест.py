a = [('a',),('b',)]
for i in a:
    if 'a' in i[0]:
        print('Есть', i)
    else:
        print('Нет', i)