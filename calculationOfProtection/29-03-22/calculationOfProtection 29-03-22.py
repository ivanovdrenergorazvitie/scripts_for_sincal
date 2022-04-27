"""
                               --+-СОДЕРЖАНИЕ-+--

1. НЕОБХОДИМЫЕ ФУНКЦИИ------------------------------------------------------15
2. ПЕРВОНАЧАЛЬНЫЕ МАНИПУЛЯЦИИ-----------------------------------------------156
3. СОСТАВЛЕНИЕ СПИСКА ИЗ ПОСЛЕДНИХ УЗЛОВ ДЛЯ РАСЧЕТА ТКЗ--------------------294
4. РАСЧЁТ УСТАВОК ТОКА СРАБАТЫВАНИЯ МТО, ТОВВ И МТЗ-------------------------474
5. ВЫБОР УСТАВОК ПО ВРЕМЕНИ-------------------------------------------------
"""
import sqlite3
import tkinter as tk
import p

"""-------------------------------1. НЕОБХОДИМЫЕ ФУНКЦИИ-------------------------------------------------------------"""

#   ---- Перевод кортежей в строки или списки
def name_changer(b):
    a = []
    for i in range(len(b)):
        if len(b[i]) == 1:  # *
            a.append(b[i][0])
        else:  # *
            a.append(list(b[i]))  # *
    return a


#   ---- Составление путей с линиями с реклоузерами   [['L357', 'L363'], ['L383', 'L363']]
def time1(e, a, d):
    i = -1
    f = 0
    usl3 = True
    while usl3 is True:
        i += 1
        if e == []:
            e.insert(i, [a])
            e[i] += [d]
        elif e[i][-1] == a:
            e[i] += [d]
            f += 1
        if len(e) - 1 == i:
            if f == 0:
                e.insert(i, [a])
                e[i] += [d]
            usl3 = False
    return e


#   ---- Удаление лишних путей
def timecorr(e):
    l = e  # ---- На случай, если len(e) = 1
    if len(e) > 1:
        l = []
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
    return l


#   ---- Организация необходимого вида  [[{'L357': [0.001]}, {'L363': []}], [{'L383': [0.001]}, {'L363': []}]]
def time2(a, timeprot, timesel):
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
    return a


#   ---- Расчёт уставок времени  [{'L383': ([0.001], [0.2])}, {'L363': ([0.3], [0.1], [0.001])}]
def time3(z, timeprot, timesel):
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

    """
    Задаем уставки самых длинных цепочек
    """
    for j in l:
        for i in range(nc):
            key = (str(z[j][i]).split(':')[0])[2:-1]
            if i == 0:
                if timeprot == 0:
                    z[j][i][key] = [round(timesel * nc, 1)], [0.001]
                else:
                    z[j][i][key] = [round(timesel * nc + timeprot, 1)], [0.001]
            else:
                if timeprot == 0:
                    z[j][i][key] = [float(str(timesel * (i + nc))[:3])], [0.001], [float(str(timesel * i)[:3])]
                else:
                    z[j][i][key] = [float(str(timesel * (i + nc) + timeprot)[:3])], [0.001], [
                        float(str(timesel * i + timeprot)[:3])]

    """
    Список оставшихся цепочек
    """
    for i in range(len(z)):
        if i not in l:
            nl += [i]

    """
    Задаем уставки оставшихся цепочек
    """
    for j in nl:
        fKey = z[j]  # Забираем список словарей
        for i in range(len(z[j])):
            t1 = 0
            key1 = (str(z[j][i]).split(':')[0])[2:-1]
            if i == 0:
                if timeprot == 0:
                    z[j][i][key1] = [0.001], [round(timesel * nc, 1)]
                else:
                    z[j][i][key1] = [0.001], [round(timesel * nc + timeprot, 1)]
            else:
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
                    if z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][-1] < [round(float(timesel * i), 3)]:
                        if timeprot == 0:
                            z[j][i][key1] = [float(str(timesel * (i + nc))[:3])], [0.001], [float(str(timesel * i)[:3])]
                        else:
                            z[j][i][key1] = [float(str(timesel * (i + nc) + timeprot)[:3])], [0.001], [
                                float(str(timesel * i + timeprot)[:3])]
                    else:
                        if timeprot == 0:
                            z[j][i][key1] = [float(
                                z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + timesel * nc], [
                                                0.001], [
                                                float(z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + timesel]
                        else:
                            z[j][i][key1] = [float(
                                z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + timesel * nc + timeprot], [
                                                0.001], [
                                                float(z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][
                                                          0]) + timesel + timeprot]
                if t1 != 0:
                    z[j][i][key1] = t1
    return z


#   ---- Формирование списка элементов таблицы с акутальным вариантом
def varID(var, flag, mainList, a='Не назначено', b='Не назначено'):
    if flag == 1:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Element_ID FROM Element WHERE Variant_ID IN ({var}) AND Group_ID IN ({gr})").fetchall())))))
        return mainList
    if flag == 2:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Breaker WHERE Variant_ID IN ({var}) AND Flag_State='0'").fetchall())))))
        return mainList
    if flag == 3:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({str(a)}) "
            f"AND TerminalNo='2' AND Variant_ID IN ({var}) AND Flag_Variant='1'").fetchall())))))
        return mainList
    if flag == 4:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Variant_ID IN ({var})").fetchall())))))
        return mainList
    if flag == 5:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({str(a[0])}) "
            f"AND Terminal_ID NOT LIKE ({str(b[0])}) "
            f"AND Variant_ID IN ({var}) AND Flag_Variant='1'").fetchall())))))
        return mainList
    if flag == 6:
        mainList = sorted(list(set(mainList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal "
            f"WHERE Node_ID IN ({str(a)}) AND TerminalNo='1' AND Variant_ID IN ({v})").fetchall())))))
        return mainList


"""-----------------------------2. ПЕРВОНАЧАЛЬНЫЕ МАНИПУЛЯЦИИ--------------------------------------------------------"""

"""
Обращение к базе данных SQLite
"""

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

"""
Выбор варианта
"""
print('\n\n----+-Список вариантов-+----')
var_to_print = list(cursorObj.execute("SELECT Variant_ID, Name FROM Variant").fetchall())
for v in var_to_print:
    print(v[0], '----------------', v[1])

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('\n\nВведите вариант схемы ' + str(variantID0) + ': '))
variantID = []
variantID1 = userVariantID

if userVariantID != 1:
    while variantID1 != 0:
        variantID += [variantID1]
        parentVariantID = cursorObj.execute(
            "SELECT ParentVariant_ID FROM Variant WHERE Variant_ID IN ({0})".format(
                str(variantID1))).fetchall()
        parentVariantID = name_changer(parentVariantID)
        parentVariantID = parentVariantID[0]
        variantID1 = parentVariantID
else:
    variantID = [1]
print('Последовательность вариантов:', variantID)

'''
Преды из библиотеки
'''

listOfPkt = ('ПКТ-10 (2 A)', 'ПКТ-10 (3 A)', 'ПКТ-10 (5 A)', 'ПКТ-10 (8 A)', 'ПКТ-10 (10 A)', 'ПКТ-10 (16 A)',
             'ПКТ-10 (20 A)', 'ПКТ-10 (31 A)', 'ПКТ-10 (40 A)', 'ПКТ-10 (50 A)', 'ПКТ-10 (80 A)', 'ПКТ-10 (100 A)',
             'ПКТ-10 (160 A)', 'ПКТ-6 (2 A)', 'ПКТ-6 (3 A)', 'ПКТ-6 (5 A)', 'ПКТ-6 (8 A)', 'ПКТ-6 (10 A)',
             'ПКТ-6 (16 A)', 'ПКТ-6 (20 A)', 'ПКТ-6 (31 A)', 'ПКТ-6 (40 A)', 'ПКТ-6 (50 A)', 'ПКТ-6 (63 A)',
             'ПКТ-6 (80 A)', 'ПКТ-6 (100 A)', 'ПКТ-6 (160 A)', 'ПКТ-6 (200 A)', 'ПКТ-6 (315 A)',
             'ПКТ-10 (2 А)', 'ПКТ-10 (3 А)', 'ПКТ-10 (5 А)', 'ПКТ-10 (8 А)', 'ПКТ-10 (10 А)', 'ПКТ-10 (16 А)',
             'ПКТ-10 (20 А)', 'ПКТ-10 (31 А)', 'ПКТ-10 (40 А)', 'ПКТ-10 (50 А)', 'ПКТ-10 (80 А)', 'ПКТ-10 (100 А)',
             'ПКТ-10 (160 А)', 'ПКТ-6 (2 А)', 'ПКТ-6 (3 А)', 'ПКТ-6 (5 А)', 'ПКТ-6 (8 А)', 'ПКТ-6 (10 А)',
             'ПКТ-6 (16 А)', 'ПКТ-6 (20 А)', 'ПКТ-6 (31 А)', 'ПКТ-6 (40 А)', 'ПКТ-6 (50 А)', 'ПКТ-6 (63 А)',
             'ПКТ-6 (80 А)', 'ПКТ-6 (100 А)', 'ПКТ-6 (160 А)', 'ПКТ-6 (200 А)', 'ПКТ-6 (315 А)')
"""
Определение фидеров, которые необходимо обработать
"""

NetworkGroup = cursorObj.execute("SELECT Group_ID, Name FROM NetworkGroup WHERE Flag_Variant='1'").fetchall()
NetworkGroup = name_changer(NetworkGroup)

print('\n\n----+-Список фидеров-+----')
for i in NetworkGroup:
    print(i[0], '----------------' if len(str(i[0])) == 1 else '---------------', i[1])
# ---- Список пользовательского выбора фидеров, которые необходимо обработать
gr_id = input('\n\nВведите через пробел номера фидеров, которые необходимо посчитать: ').split()

print('Ваш выбор:', gr_id)

"""
Связка подстанций и фидеров
"""
PSbusbars = []
for v in variantID:
    PSbusbars = list(set(PSbusbars).union(set(name_changer(cursorObj.execute(f"SELECT Node_ID FROM Node"
                                                                             f" WHERE Variant_ID IN ({v}) AND "
                                                                             f"Name LIKE 'ПС%'").fetchall()))))

fiederbaza = dict()
for i in PSbusbars:
    for v in variantID:
        startLine = cursorObj.execute(f"SELECT Element_ID FROM Terminal "
                                      f"WHERE Node_ID IN ({i}) AND Variant_ID IN ({v})").fetchall()
        if startLine == []:
            continue
        else:
            startLine = name_changer(startLine)
            break
    for k in startLine:
        for v in variantID:
            groupID = cursorObj.execute(f"SELECT Group_ID FROM Element "
                                        f"WHERE Element_ID IN ({k}) AND Variant_ID IN ({v})").fetchone()
            if groupID is None:
                continue
            else:
                groupID = groupID[0]
                fiederbaza[groupID] = [k, i]

                break
print('Взаимосвязь узлов и элементов с фидерами:', fiederbaza)

BTerminalList = []  # ---- Список терминалов с выключенными выключателями
for v in variantID:
    BTerminalList = varID(v, 2, BTerminalList)


#   ---- Значения в модуль
def p_values():
    p.variantID = variantID
    p.cursorObj = cursorObj
    p.protTerminalID = protTerminalID
    p.protLocID = protLocID
    p.protElementID = protElementID
    p.protElementName = protElementName
    p.protNodeID2 = protNodeID2
    p.defaultValues = defaultValues
    p.fiederbaza = fiederbaza
    p.listOfPkt = listOfPkt
    p.BTerminalList = BTerminalList


"""
Составление списка реклоузеров
"""
for gr in gr_id:  # ---- Цикл по заданным фидерам
    print(NetworkGroup, gr)
    print('\n\n\nРассматриваемый фидер:', next(x[1] for x in NetworkGroup if str(x[0]) == str(gr)))
    gr = int(gr)
    """
    Вокабуляр
    """

    protTerminalID = []  # ---- Список терминалов с необходимыми защитами
    protLocID = []  # ---- ProtLoc_ID необходимых защит
    protElementID = []  # ---- Element_ID элемента, на котором находится защита
    protElementName = []  # ---- Название элемента, на котором находится защита
    protNodeID2 = []  # ---- Список узлов после УРЗА для МТО
    defaultValues = 0  # ---- Параметр условия принятия значений по умолчанию
    p_values()

    while defaultValues != 1 and defaultValues != 2:
        defaultValues = int(input('\n\n\n\nПринимать рекомендуемые значения коэффициентов? 1 - Да, 2 - Нет: '))
        if defaultValues != 1 and defaultValues != 2:
            print('Введите корректное значение')
    printt = 0  # ---- Подробная печать. Режим отладки

    p2Boolean, dictProtInfo, protElementName, \
    protElementID, protLocID, protTerminalID, protNodeID2 = p.p2(varID, name_changer)

    if p2Boolean:
        continue

    p.protNodeID2 = protNodeID2
    p.protElementID = protElementID
    p.protElementName = protElementName
    p.protLocID = protLocID
    p.protTerminalID = protTerminalID

    """-----------------------------3. КОРРЕКТИРОВКА НПРАВЛЕНИЯ ЭЛЕМНТОВ---------------------------------------------"""

    p.p3(name_changer, varID, gr)

    """-------------------------------4. СОСТАВЛЕНИЕ СПИСКА ИЗ ПОСЛЕДНИХ УЗЛОВ ДЛЯ РАСЧЕТА ТКЗ-------------------------#
        -+-- Игнорируем элементы хотя бы без одного из двух терминалов и элементы с предохранителями --+-"""

    allProtLastNodeID, lastNodes, timeparent, timelist = p.p4(varID)
    p.allProtLastNodeID = allProtLastNodeID
    p.timeparent = timeparent
    p.lastNodes = lastNodes
    p.defaultValues = defaultValues


    """-------------------------5. РАСЧЁТ УСТАВОК ТОКА ДЛЯ ТОВВ, MTO И МТЗ-------------------------------------------"""

    timeparent = p.p5()

    """---------------------------------6. ВЫБОР УСТАВОК ПО ВРЕМЕНИ--------------------------------------------------"""
    p.dictProtInfo = dictProtInfo
    p.timeparent = timeparent
    p.timelist = timelist
    p.p6(varID, name_changer, time1, time2, time3, timecorr)
a = input('Нажмите 1, чтобы сохранить изменения')
if a == '1':
    print('Сохранено')
    con.commit()  # ---- Подтверждение изменений в БД
    con.close()
else:
    print('Не сохранено')
# ---- Последняя строчка кода
