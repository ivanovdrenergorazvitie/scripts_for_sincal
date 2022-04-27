"""
                               --+-СОДЕРЖАНИЕ-+--

1. НЕОБХОДИМЫЕ ФУНКЦИИ------------------------------------------------------15
2. ПЕРВОНАЧАЛЬНЫЕ МАНИПУЛЯЦИИ-----------------------------------------------156
3. СОСТАВЛЕНИЕ СПИСКА ИЗ ПОСЛЕДНИХ УЗЛОВ ДЛЯ РАСЧЕТА ТКЗ--------------------294
4. РАСЧЁТ УСТАВОК ТОКА СРАБАТЫВАНИЯ МТО, ТОВВ И МТЗ-------------------------474
5. ВЫБОР УСТАВОК ПО ВРЕМЕНИ-------------------------------------------------
"""
import sqlite3
import pandas as pd

"""
#######################################################################################################################
#---------------------------------1. НЕОБХОДИМЫЕ ФУНКЦИИ--------------------------------------------------------------#
#######################################################################################################################
"""
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
    l = e # ---- На случай, если len(e) = 1
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


#   ---- Расчёт уставок времени
#   -+-- [{'L357': ([0.001], [0.2])}, {'L363': ([0.3], [0.1], [0.001])}]
#   -+-- [{'L383': ([0.001], [0.2])}, {'L363': ([0.3], [0.1], [0.001])}]
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

def varID(var, flag):
    global ElementIDforPr, nextTerminalID, BTerminalList, allActualTerminalID
    if flag == 1:
        ElementIDforPr = sorted(list(set(ElementIDforPr).union(set(name_changer(cursorObj.execute(
            f"SELECT Element_ID FROM Element WHERE Variant_ID IN ({var}) AND Group_ID IN ({gr})").fetchall())))))
        return ElementIDforPr
    if flag == 2:
        BTerminalList = sorted(list(set(BTerminalList).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Breaker WHERE Variant_ID IN ({var}) AND Flag_State='0'").fetchall())))))
        return BTerminalList
    if flag == 3:
        nextTerminalID = sorted(list(set(nextTerminalID).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({str(nextNodeID)}) "
            f"AND TerminalNo='2' AND Variant_ID IN ({var}) AND Flag_Variant='1'").fetchall())))))
        return nextTerminalID
    if flag == 4:
        allActualTerminalID = sorted(list(set(allActualTerminalID).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Variant_ID IN ({var})").fetchall())))))
        return allActualTerminalID
    if flag == 5:
        nextTerminalID = sorted(list(set(nextTerminalID).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({str(nextNodeID[0])}) "
            f"AND Terminal_ID NOT LIKE ({str(endTerminalID[0])}) "
            f"AND Variant_ID IN ({var}) AND Flag_Variant='1'").fetchall())))))
        return nextTerminalID
    if flag == 6:
        nextTerminalID = sorted(list(set(nextTerminalID).union(set(name_changer(cursorObj.execute(
            f"SELECT Terminal_ID FROM Terminal "
            f"WHERE Node_ID IN ({str(nextNodeID)}) AND TerminalNo='1' AND Variant_ID IN ({v})").fetchall())))))
        return nextTerminalID


"""
########################################################################################################################
#-------------------------------2. ПЕРВОНАЧАЛЬНЫЕ МАНИПУЛЯЦИИ----------------------------------------------------------#
########################################################################################################################
"""

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
    print(v[0],'----------------', v[1])

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

# """
# Корректировка направления элементов
# """
# wcflag = input('Провести корректировку направления? (1 - Да): ')
# if wcflag:
#     allActualTerminalID = []
#     waycorr()
#     con.commit()
#     con.close()
#     path_db = 'database.db'
#     con = sqlite3.connect(path_db)
#     cursorObj = con.cursor()
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

allChangingTerminals = []           # ---- Список всех измененных в результате корректирвоки терминалов
BTerminalList = []                  # ---- Список терминалов с выключенными выключателями
for v in variantID:
    BTerminalList = varID(v, 2)

for gr in gr_id:  # ---- Цикл по заданным фидерам
    print(NetworkGroup, gr)
    print('\n\n\nРассматриваемый фидер:', next(x[1] for x in NetworkGroup if str(x[0]) == str(gr)))
    gr = int(gr)
    """
    Вокабуляр
    """
    ElementIDforPr = []             # ---- Список элементов рассматриваемого фидера
    TerminalIDForPr = []            # ---- Список терминалов рассматриваемого фидера
    protInfo = []                   # ---- Список ProtLoc_ID всех защит без учёта предохранителей
    ptxTerminalID = []              # ---- Список терминалов с защитами
    protTerminalID = []             # ---- Список терминалов с необходимыми защитами
    ptxGTerminalID = []             # ---- Список графики терминалов с защитами
    allProtGTerminalID = []         # ---- Список графики терминалов с необходимыми защитами
    protLocID = []                  # ---- ProtLoc_ID необходимых защит
    ProtLocID = []                  # ---- ProtLoc_ID и Variant_ID рассматриваемой защиты
    protElementID = []              # ---- Element_ID элемента, на котором находится защита
    protElementName = []            # ---- Название элемента, на котором находится защита
    protNodeID2 = []                # ---- Список узлов после УРЗА для МТО
    defaultValues = 0               # ---- Параметр условия принятия значений по умолчанию
    infElementID = []               # ---- Источник рассматриваемого фидера
    while defaultValues != 1 and defaultValues != 2:
        defaultValues = int(input('\n\n\n\nПринимать рекомендуемые значения коэффициентов? 1 - Да, 2 - Нет: '))
        if defaultValues != 1 and defaultValues != 2:
            print('Введите корректное значение')
    printt = 1                      # ---- Подробная печать. Режим отладки



    """
    Составление списка реклоузеров
    """

    #   ---- Список существующих предохранителей (из библиотеки)
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

    for v in variantID:
        ElementIDforPr = varID(v, 1)                    # ---- Список элементов фидера
                         # ---- Список Терминалов с выключенным выключателем


    """
    Информация о реклоузерах
    """
    for i in ElementIDforPr:
        for v in variantID:
            TerminalIDForPr0 = cursorObj.execute(f"SELECT Terminal_ID FROM Terminal "
                                                 f"WHERE Flag_Switch='1' AND Element_ID IN({i}) "
                                                 f"AND Variant_ID IN ({v})").fetchone()
            if TerminalIDForPr0 is None:
                continue
            else:
                TerminalIDForPr += [TerminalIDForPr0[0]]   # ---- Список терминалов фидера
                TerminalIDForPr = sorted(list(set(TerminalIDForPr)))
                break


    for j in variantID:
        protInfo0 = cursorObj.execute(f"SELECT ProtLoc_ID FROM ProtOCSetting "
                                      f"WHERE p_nam NOT LIKE '%ПКТ-6%' "
                                      f"AND p_nam NOT LIKE '%ПКТ-10%' "
                                      f"AND Variant_ID IN ({j})").fetchall()
        if protInfo0 is None:
            continue
        else:
            protInfo += name_changer(protInfo0)        # ---- Список ProtLoc_ID всех защит без учёта предохранителей
            protInfo = sorted(list(set(protInfo)))
            break

    #   ---- Список терминалов с защитами
    for i in TerminalIDForPr:
        for ptx1 in range(len(protInfo)):
            for v in variantID:
                ptxTerminalID0 = cursorObj.execute(
                    f"SELECT Terminal_ID FROM ProtLocation "
                    f"WHERE  Terminal_ID IN ({i}) "
                    f"AND ProtLoc_ID IN ({protInfo[ptx1]}) "
                    f"AND Variant_ID IN ({v})").fetchone()
                if ptxTerminalID0 is None:
                    continue
                else:
                    ptxTerminalID += [ptxTerminalID0[0]]
                    ptxTerminalID = sorted(list(set(ptxTerminalID)))
                    break
    print('ptxTerminalID:', ptxTerminalID)

    #   ---- Список графики терминалов с защитами
    for ptx2 in range(len(ptxTerminalID)):
        for v in variantID:
            ptxGTerminalID0 = cursorObj.execute(
                f"SELECT GraphicTerminal_ID FROM GraphicTerminal "
                f"WHERE Terminal_ID IN ({str(ptxTerminalID[ptx2])}) "
                f"AND Variant_ID IN ({v})").fetchone()
            if ptxGTerminalID0 is None:
                continue
            else:
                ptxGTerminalID += [ptxGTerminalID0[0]]
                ptxGTerminalID = sorted(list(set(ptxGTerminalID)))
                break
    print('ptxGTerminalID:', ptxGTerminalID)

    #   ---- Список графики терминалов с необходимыми защитами
    for ptx3 in range(len(ptxGTerminalID)):
        for v in variantID:
            allProtGTerminalID0 = cursorObj.execute(
                f"SELECT GraphicTerminal_ID FROM GraphicAddTerminal "
                f"WHERE SymType LIKE 1 AND FrgndColor LIKE 255 "
                f"AND GraphicTerminal_ID IN ({str(ptxGTerminalID[ptx3])}) AND Variant_ID IN ({v})").fetchone()
            if allProtGTerminalID0 is None:
                continue
            else:
                allProtGTerminalID += [allProtGTerminalID0[0]]
                allProtGTerminalID = sorted(list(set(allProtGTerminalID)))
                break
    print('GТерминалы с защитами:', allProtGTerminalID)

    #   ---- Terminal_ID, в котором находится необходимая защита
    for prot1 in range(len(allProtGTerminalID)):
        for v in variantID:
            protTerminalID0 = cursorObj.execute(
                f"SELECT Terminal_ID FROM GraphicTerminal "
                f"WHERE GraphicTerminal_ID IN ({allProtGTerminalID[prot1]})"
                f"AND Variant_ID IN ({v})").fetchone()
            if protTerminalID0 is None:
                continue
            else:
                for vv in variantID:
                    if cursorObj.execute(f"SELECT Flag_State FROM Breaker "
                                         f"WHERE Terminal_ID IN ({protTerminalID0[0]}) "
                                         f"AND Variant_ID IN ({vv})").fetchone() == (1,):
                        protTerminalID += [protTerminalID0[0]]
                        protTerminalID = sorted(list(set(protTerminalID)))
                        break

    print('Терминалы с защитами:', protTerminalID)
    skipMainIter = 0
    # ---- Ввод необходимых параметров защиты для доступа записи уставок в терминал
    for prot2 in range(len(protTerminalID)):
        for v in variantID:
            ProtLocID0 = cursorObj.execute(
                f"SELECT ProtLoc_ID, Variant_ID FROM ProtLocation "
                f"WHERE Terminal_ID IN ({protTerminalID[prot2]}) "
                f"AND Variant_ID IN ({v})").fetchone()
            if ProtLocID0 is None:
                continue
            else:
                ProtLocID += [list(ProtLocID0)]
                break
        # ---- Условие отсутствия данных
        if cursorObj.execute(f"SELECT p_nam FROM ProtOCSetting WHERE ProtLoc_ID='{str(ProtLocID[prot2][0])}' "
                             f"AND Variant_ID='{ProtLocID[prot2][1]}'").fetchone()[0] == '':
            cursorObj.execute(
                "UPDATE ProtOCSetting SET ProtCharP_ID='4095' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET ProtCharE_ID='4095' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET p_nam='Сириус-2-Л INV' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET e_nam='Сириус-2-Л INV' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET sw2='1' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET sw3='1' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
            cursorObj.execute(
                "UPDATE ProtOCSetting SET sw4='1' "
                "WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID[prot2][0]), str(ProtLocID[prot2][1])))
        else:
            print('\n\n\n!!!На фидере есть защита с установленными параметрами: '
                  + str(protTerminalID[prot2]) + '\n\n\n')
            protTerminalID = []
            # protElementID = []
            # protTerminalID = []
            # skipMainIter = 1
            break
        protLocID += [ProtLocID[prot2][0]]

    print('protLocID:', protLocID)
    if protTerminalID == []:
        continue
    for prot in range(len(protTerminalID)):
        for v in variantID:
            protElementID0 = cursorObj.execute(
                f"SELECT Element_ID FROM Terminal "
                f"WHERE Terminal_ID IN ({str(protTerminalID[prot])}) AND Variant_ID IN ({v})").fetchone()
            if protElementID0 is None:
                continue
            else:
                protElementID += [protElementID0[0]]
                break
        for v in variantID:
            protElementName0 = cursorObj.execute(
                f"SELECT Name FROM Element WHERE Element_ID IN ({protElementID[prot]}) "
                f"AND Variant_ID IN ({v})").fetchone()
            if protElementName0 is None:
                continue
            else:
                protElementName += [protElementName0[0]]
                break
        for v in variantID:
            protNodeID20 = cursorObj.execute(
                f"SELECT Node_ID FROM Terminal "
                f"WHERE Element_ID='{protElementID[0]}' AND Terminal_ID!='{protTerminalID[prot]}' "
                f"AND Variant_ID IN ({v})").fetchone()
            if protNodeID20 is None:
                continue
            else:
                protNodeID2 += [protNodeID20[0]]
                protNodeID2 = sorted(list(set(protNodeID2)))
                break
    print('Список с информацией о защите:', protElementID, protElementName)
    dictProtInfo = zip(protElementName, protElementID, protLocID)
    """
    ####################################################################################################################
    #-------------------------------3. КОРРЕКТИРОВКА НПРАВЛЕНИЯ ЭЛЕМНТОВ-----------------------------------------------#
    ####################################################################################################################
    """
    checkedTerm = []
    checkedEl = []
    nextNodeID = []
    listOfLastNode = []
    lastNodeID = []
    checkedNodeID = []
    forgottenTerminalID = []
    nextTerminalID = []
    usl1 = True
    while usl1 is True:
        usl2 = True
        print('usl1:', usl1)
        nextTerminalID = []
        for osn1 in range(len(forgottenTerminalID)):
            nextTerminalID += [forgottenTerminalID[osn1]]
            # if nextTerminalID[0] == 130:
            #     input('КОРРЕКТИВЫ')
        print('\nВышли из условия\nНекст терминал:', nextTerminalID, '\n')
        while usl2 is True:
            usl3 = 1

            if nextTerminalID == [] and forgottenTerminalID == [] and checkedTerm == []:  # ---- первый вход в цикл while, где берется терминал источника

                # #   Первый терминал
                # #     _|_
                # #      | <- собсна некст терминал (TerminalNo = 1)
                for v in variantID:
                    nextTerminalID = cursorObj.execute(
                        f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({str(fiederbaza.get(gr)[1])}) "
                        f"AND Element_ID IN ({str(fiederbaza.get(gr)[0])}) AND Variant_ID IN ({v})").fetchall()
                    if nextTerminalID == []:
                        continue
                    else:
                        nextTerminalID = name_changer(nextTerminalID)
                        break
                if len(nextTerminalID) > 1:
                    forgottenTerminalID += (nextTerminalID[
                                            1:])    # ---- Если терминалов несколько, хапаем их в список
                                                    # ---- (все, кроме первого - с первым работаем)
                # print('Оставшиеся терминалы:', forgottenTerminalID)
                # print()
            if nextTerminalID == [] and forgottenTerminalID == []:
                usl2 = False
                usl1 = False
                break
            if nextTerminalID[0] in checkedTerm:
                try:
                    nextTerminalID[0] = forgottenTerminalID[0]
                except: # ---- Если не осталось терминалов
                    usl1 = False
                    usl2 = False
                    break


            if nextTerminalID[0] in forgottenTerminalID:
                removeTerminalID = nextTerminalID[0]
                forgottenTerminalID.remove(removeTerminalID)
            if len(nextTerminalID) > 1:
                usl3 = 0
                #    _|_
                #    ||| <- несколько некст терминалов фиксируем как usl3, чтобы использовать в условиях конечных узлов
            if nextTerminalID[0] in BTerminalList:
                usl2 = False
                continue
            skippflag = 0           # ---- Фидер Элемента отличается от рассматриваемого

            checkedTerm += [nextTerminalID[0]]
            # print('checkedTerm', checkedTerm)
            for v in variantID:
                thisElementID = cursorObj.execute(
                    f"SELECT Element_ID FROM Terminal "
                    f"WHERE Terminal_ID IN ({str(nextTerminalID[0])}) "
                    f"AND Variant_ID IN ({v})").fetchall()
                if thisElementID == []:
                    continue
                else:
                    thisElementID = name_changer(thisElementID)

                    for elem in thisElementID:
                        for vv in variantID:
                            eltestgr = cursorObj.execute(f"SELECT Group_ID FROM Element "
                                                         f"WHERE Element_ID IN ({elem}) "
                                                         f"AND Variant_ID IN ({vv})").fetchone()
                            if eltestgr is None:
                                continue
                            else:
                                eltestgr = eltestgr[0]
                                if eltestgr != gr:
                                    try:
                                        del nextTerminalID[0]
                                        nextTerminalID += [forgottenTerminalID[0]]
                                    except:
                                        pass
                                    skippflag = 1
                                    break
                    break
            if skippflag == 1:
                continue

            for v in variantID:
                elementName = cursorObj.execute(
                    f"SELECT Name FROM Element "
                    f"WHERE Element_ID IN ({str(thisElementID[0])}) "
                    f"AND Variant_ID IN ({v}) AND Group_ID IN ({gr})").fetchone()
                if elementName is None:
                    continue
                else:
                    elementName = elementName[0]

                    break
            checkedEl += [elementName]
            # print('checkedEl', checkedEl)

            print('Просматриваемый элемент:', thisElementID, elementName)
            # if thisElementID[0] == 1286:
            #     input('das')
            #   Терминал конца элемента
            #   _|_ <- энд терминал (TerminalNo = 2)
            #    |
            for v in variantID:
                endTerminalID = cursorObj.execute(
                    f"SELECT Terminal_ID FROM Terminal "
                    f"WHERE Element_ID IN ({str(thisElementID[0])}) "
                    f"AND Terminal_ID NOT LIKE ({str(nextTerminalID[0])}) AND Variant_ID IN ({v})").fetchall()
                if endTerminalID == []:
                    continue
                else:
                    endTerminalID = name_changer(endTerminalID)
                    break
            try:
                if endTerminalID[0] in checkedTerm:
                    continue
            except:
                continue
            # print('Терминал в конце элемента:', endTerminalID)

            for napr3 in range(len(endTerminalID)):
                for v in variantID:
                    numbEndTerminal = cursorObj.execute(
                        f"SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({str(endTerminalID[napr3])}) "
                        f"AND Variant_ID IN ({v})").fetchone()
                    if numbEndTerminal is None:
                        continue
                    else:
                        numbEndTerminal = numbEndTerminal[0]
                        break
                if numbEndTerminal == 1:
                    for v in variantID:
                        cursorObj.execute(
                            f"UPDATE Terminal SET TerminalNo='2' "
                            f"WHERE Terminal_ID IN ({str(endTerminalID[napr3])}) AND Variant_ID IN ({v})")
                    print('Поменяно2:', endTerminalID[napr3], v)
                    for v in variantID:
                        startTerminalID = cursorObj.execute(
                            f"SELECT Terminal_ID FROM Terminal "
                            f"WHERE Element_ID IN ({str(thisElementID[0])}) "
                            f"AND Terminal_ID NOT LIKE ({str(endTerminalID[napr3])}) "
                            f"AND Variant_ID IN ({v})").fetchall()
                        if startTerminalID == []:
                            continue
                        else:
                            startTerminalID = name_changer(startTerminalID)
                            break
                    for v in variantID:
                        cursorObj.execute(
                            f"UPDATE Terminal SET TerminalNo='1' "
                            f"WHERE Terminal_ID IN ({str(startTerminalID[0])}) AND Variant_ID IN ({v})")
                    print('Поменяно1:', startTerminalID[napr3], v)
                    allChangingTerminals += [nextTerminalID[napr3], numbEndTerminal]
                if endTerminalID[napr3] in BTerminalList:
                    usl2 = False
                    continue

            '''
            ---- ---- УСЛОВИЯ КОНЕЧНЫХ УЗЛОВ И УЗЛОВ С АЛЬТЕРНАТИВНЫМ ПРОДОЛЖЕНИЕМ                  
            '''
            # ---- Нагрузка и отсутствие
            #       _|_
            #        |
            #        * <- у нагрузок нет конечного терминала
            if endTerminalID == []:
                if usl3 == 1:
                    lastNodeID += [
                        nodeName]  # ---- соответственно, если нет дополнительных терминалов, то мы записываем узел как конечный
                usl2 = False
                continue
            # if nextNodeID != []:
            #     nextNodeID0 = nextNodeID  <--- не уверен, что это условие жизненно необходимо
            # if endTerminalID[0] == '2669':
            #     input('das')
            for v in variantID:
                nextNodeID = cursorObj.execute(
                    f"SELECT Node_ID FROM Terminal "
                    f"WHERE Terminal_ID IN ({str(endTerminalID[0])}) AND Variant_ID IN ({v})").fetchall()
                if nextNodeID == []:
                    continue
                else:
                    nextNodeID = name_changer(nextNodeID)
                    break
            checkedNodeID += (nextNodeID)
            # print('Просмотренные терминалы:', checkedNodeID)
            # print('Следующий узел:', nextNodeID)
            for v in variantID:
                nodeName = cursorObj.execute(
                    f"SELECT Name FROM Node WHERE Node_ID IN ({str(nextNodeID[0])}) "
                    f"AND Variant_ID IN ({v}) AND Group_ID IN ({gr})").fetchone()
                if nodeName is None:
                    continue
                else:
                    nodeName = nodeName[0]
                    break
            # print('Имя этого узла:', nodeName)

            #   Следующий терминал
            #   Следующий терминал
            #     _|_
            #      | <- собсна некст терминал (TerminalNo = 1)
            nextTerminalID = []
            for v in variantID:
                varID(v, 5)

            # for fff in nextTerminalID:
            #     if fff in BTerminalList:
            #         del fff

            # print('Некст терминал:', nextTerminalID)
            usl3 = 1
            if len(nextTerminalID) > 1:
                usl3 = 0
                forgottenTerminalID += (nextTerminalID[1:])
                usl1 = True
                # for ft in forgottenTerminalID:
                #     if ft
            # for napr4 in range(len(nextTerminalID)):
            #     for v in variantID:
            #         numbNextTerminal = cursorObj.execute(
            #             f"SELECT TerminalNo FROM Terminal "
            #             f"WHERE Terminal_ID IN ({str(nextTerminalID[napr4])}) AND Variant_ID IN ({v})").fetchone()
            #         if numbNextTerminal is None:
            #             continue
            #         else:
            #             numbNextTerminal = numbNextTerminal[0]
            #             break

            # print('Оставшиеся терминалы:', forgottenTerminalID)
            print()
            #   ---- Если дальше нет терминала
            #       _|_ <- тупиковая шина
            if nextTerminalID == []:
                lastNodeID += [nodeName]
                nextTerminalID += forgottenTerminalID[0]
                usl2 = False
                continue
            #   ---- Если дальше стоит предохранитель
            #           _|_
            #           [|] <- предохранитель
            #   За предохранителями линий обычно больше нет, и смотреть дальше бессмысленно
            for v in variantID:
                ptxLocID = cursorObj.execute(
                    f"SELECT ProtLoc_ID FROM ProtLocation "
                    f"WHERE Terminal_ID IN ({str(nextTerminalID[0])}) AND Variant_ID IN ({v})").fetchone()
                if ptxLocID is None:
                    continue
                else:
                    ptxLocID = ptxLocID[0]
                    break
            if ptxLocID is None:
                continue
            else:
                for v in variantID:
                    ptxName = cursorObj.execute(
                        f"SELECT p_nam FROM ProtOCSetting "
                        f"WHERE ProtLoc_ID IN ({str(ptxLocID)}) AND Variant_ID IN ({v})").fetchone()
                    if ptxName is None:
                        continue
                    else:
                        ptxName = ptxName[0]
                        break
            if ptxName is None:
                continue
            else:
                if ptxName in listOfPkt:
                    if usl3 == 1:
                        lastNodeID += [
                            nodeName]  # ---- Если нет альтернативных терминалов, то это конечный терминал
                        # print('alonetermwithptx', nodeName)
                    usl2 = False
            # print()
    # continue
    # con.commit()  # ---- Подтверждение изменений в БД
    """
    ####################################################################################################################
    #---------------------------------4. СОСТАВЛЕНИЕ СПИСКА ИЗ ПОСЛЕДНИХ УЗЛОВ ДЛЯ РАСЧЕТА ТКЗ-------------------------#
    ####################################################################################################################
        -+-- Игнорируем элементы хотя бы без одного из двух терминалов и элементы с предохранителями --+-
    """

    """
    Вокабуляр
    """
    allProtLastNodeID = []                  # ---- Конечные узлы (Node_ID, информация о наличии защиты далее, Terminal_ID, Element_ID)
    timelist = []                           # ---- Список для операций с расчетом уставок времени
    timeinfo = []                           # ---- Итоговый список для введения уставок времени
    timeparent = []                         # ----
    nnProt = []                             # ---- список ProtLoc_ID защит без названия
    protInWay = 0                           # ---- Режим рассмотрения участка других защит при расчете ТКЗ
    lastNodes = []                          # ---- Список Node_ID всех конечных узлов
    allFlagParent = []                      # ---- Список информации с наличием других реклоузеров

    for prot2 in range(len(protElementID)):
        """
        СКАНЕР 1. От элементов с защитой до крайних узлов
        """
        nextNodeID = []                     # ---- Узел (узлы) конца рассматриваемого элемента
        lastNodeID = []                     # ---- Конечные узлы [что идет за узлом, название узла, айди]
        checkedTerminalID = []              # ---- Просмотренные узлы с защитами
        forgottenTerminalID = []            # ---- Terminal_ID, которые необходимо рассмотреть в следующих итерациях
        nextTerminalID = []                 # ---- Следующий Terminal_ID, который будет рассмотрен
        notInLibrPtx = []                   # ---- Не предохранитель или предохранитель не из библиотеки
        FlagParent = ['НЕТ РЕКЛОУЗЕРА НА ПУТИ', 0]

        usl1 = True  # False, когда закончатся forgottenTerminalID - Переход к следующей защите
        while usl1:

            if forgottenTerminalID == [] and nextTerminalID != []:  # ---- Условие конца рассматриваемой защиты
                usl1 = False
                continue
            nextTerminalID = []     # ---- При каждой итерации в этом списке находится один рассматриваемый Terminal_ID

            # ---- Наполнение рассматриваемого терминала (при НЕпервых итерациях)
            for osn1 in range(len(forgottenTerminalID)):
                nextTerminalID += [forgottenTerminalID[osn1]]
            if printt == 1:
                print('\nПросматриваемый терминал:', nextTerminalID, '\n')

            usl2 = True             # False, когда последняя шина/                     }
            # когда на пути встречается защита(protInWay = 1)  }Возврат к пропущенному терминалу
            # когда на пути встречается выключенный выключатель}
            while usl2:

                usl3 = 1            # ---- Условие единственного элемента в списке nextTerminalID
                flagForProt2 = 1    # ---- Переход к терминалу конца элемента

                # ---- ПЕРВАЯ ИТЕРАЦИЯ
                if nextTerminalID == []:
                    for v in variantID:
                        protTerminalNo = cursorObj.execute(
                            f"SELECT TerminalNo FROM Terminal "
                            f"WHERE Terminal_ID IN ({str(protTerminalID[prot2])}) AND Variant_ID IN ({v})").fetchone()
                        if protTerminalNo is None:
                            continue
                        else:
                            protTerminalNo = protTerminalNo[0]
                            if printt == 1:
                                print('protTerminalNo, protTerminalID[prot2]:', protTerminalNo, protTerminalID[prot2])
                            if protTerminalNo == 1:  # ---- Защита в начале элемента
                                thisElementID = cursorObj.execute(
                                    f"SELECT Element_ID FROM Terminal "
                                    f"WHERE Terminal_ID IN ({str(protTerminalID[prot2])}) "
                                    f"AND Variant_ID IN ({v})").fetchone()[0]
                                # if thisElementID == 1286:
                                #     input('das')
                                for vv in variantID:
                                    elementName = cursorObj.execute(
                                        f"SELECT Name FROM Element "
                                        f"WHERE Element_ID IN ({str(thisElementID)}) "
                                        f"AND Variant_ID IN ({vv})").fetchone()
                                    if elementName is None:
                                        continue
                                    else:
                                        elementName = elementName[0]
                                        break
                                if printt == 1:
                                    print('Элемент с защитами:', thisElementID, elementName)
                            elif protTerminalNo == 2:   # ---- Защита в конце элемента
                                flagForProt2 = 0        # ---- Переход на терминал начала элемента

                            else:
                                if printt == 1:
                                    print('Ошибка 526. Невозможная ошибка. ProtTerminalNo не существует')
                            break

                # ---- ПОСЛЕДУЮЩИЕ ИТЕРАЦИИ
                else:

                    # ---- Удаление рассматриваемого Terminal_ID из списка нерассмотренных
                    if nextTerminalID[0] in forgottenTerminalID:
                        removeTerminalID = nextTerminalID[0]
                        forgottenTerminalID.remove(removeTerminalID)
                    # ---- Условие множества элементов в списке nextTerminalID
                    if len(nextTerminalID) > 1:
                        usl3 = 0

                    for v in variantID:
                        thisElementID = cursorObj.execute(
                            f"SELECT Element_ID FROM Terminal "
                            f"WHERE Terminal_ID IN ({str(nextTerminalID[0])}) "
                            f"AND Variant_ID IN ({v})").fetchone()
                        if thisElementID is None:
                            continue
                        else:
                            thisElementID = thisElementID[0]
                            break
                    # if str(thisElementID) == '1346':  # 1346
                    #     input('das')
                    for v in variantID:
                        elementName = cursorObj.execute(
                            f"SELECT Name FROM Element WHERE Element_ID IN ({str(thisElementID)}) "
                            f"AND Variant_ID IN ({v})").fetchone()
                        if elementName is None:
                            continue
                        else:
                            elementName = elementName[0]
                            break
                    if printt == 1:
                        print('Просматриваемый элемент:', thisElementID, elementName)
                    # if elementName == 'L1278':
                    #     input('das')
                    # ---- Наличие защиты в рассматриваемом Terminal_ID
                    try:
                        if printt == 1:
                            print('\n\n', thisElementID, protElementID)
                        # if thisElementID == 1286 or thisElementID == 4826:
                        #     input('das')
                        protElementID.index(thisElementID)

                        for v in variantID:
                            if cursorObj.execute(f"SELECT Flag_State FROM Breaker "
                                                 f"WHERE Terminal_ID IN ({str(nextTerminalID[0])}) "
                                                 f"AND Variant_ID IN ({v})").fetchone() == (1,):
                                FlagParent = ['ЕСТЬ РЕКЛОУЗЕР НА ПУТИ', 1]
                        if protInWay == 1:
                            usl2 = False
                            continue
                    except:
                        usl2 = True
                if nextTerminalID in BTerminalList:
                    usl2 = False
                    break
                #   Терминал конца элемента
                if flagForProt2 == 1:  # ---- Условие терминала конца элемента
                    for v in variantID:
                        endTerminalID = cursorObj.execute(
                            f"SELECT Terminal_ID FROM Terminal "
                            f"WHERE Element_ID IN ({str(thisElementID)}) "
                            f"AND TerminalNo='2' AND Variant_ID IN ({v})").fetchone()
                        if endTerminalID is None:
                            continue
                        else:
                            endTerminalID = endTerminalID[0]
                            print(cursorObj.execute(f"SELECT TerminalNo FROM Terminal "
                                                    f"WHERE Terminal_ID IN ({endTerminalID})").fetchone()[0])
                            break
                    if printt == 1:
                        print('Терминал в конце элемента:', endTerminalID)
                    if endTerminalID is None:
                        if usl3 == 1:
                            lastNodeID += [['load', nodeName, nextNodeID]]
                        usl2 = False
                        continue
                    if endTerminalID in BTerminalList:
                        usl2 = False
                        break
                    if nextNodeID != []:
                        nextNodeID0 = nextNodeID

                if flagForProt2 == 1:  # ---- Условие терминала конца элемента
                    for v in variantID:
                        nextNodeID = cursorObj.execute(
                            f"SELECT Node_ID FROM Terminal "
                            f"WHERE Terminal_ID IN ({str(endTerminalID)}) AND Variant_ID IN ({v})").fetchone()
                        if nextNodeID is None:
                            continue
                        else:
                            nextNodeID = nextNodeID[0]
                            # if nextNodeID == '1781':
                            #     input('das')
                            break

                elif flagForProt2 == 0:  # ---- Условие терминала начала элемента (Только при первой итерации)
                    for v in variantID:
                        nextNodeID = cursorObj.execute(
                            f"SELECT Node_ID FROM Terminal "
                            f"WHERE Terminal_ID IN ({str(protTerminalID[prot2])}) AND Variant_ID IN ({v})").fetchone()
                        if nextNodeID is None:
                            continue

                        else:
                            nextNodeID = nextNodeID[0]
                            for vv in variantID:
                                nodeName = cursorObj.execute(
                                    f"SELECT Name FROM Node "
                                    f"WHERE Node_ID IN ({str(nextNodeID)}) AND Variant_ID IN ({vv})").fetchone()
                                if nodeName is None:
                                    continue
                                else:
                                    nodeName = nodeName[0]
                                    break
                            break
                checkedTerminalID += [nextNodeID]
                if printt == 1:
                    print('Рассмотренные терминалы:', checkedTerminalID)
                    print('Следующий узел:', nextNodeID)
                if printt == 1:
                    print('Рассматриваемый узел', nodeName)

                #   Следующий терминал
                nextTerminalID = []
                for v in variantID:
                    varID(v, 6)

                if printt == 1:
                    print('Некст терминал:', nextTerminalID)

                #   ---- Если терминал не один
                usl3 = 1
                if len(nextTerminalID) > 1:
                    usl3 = 0
                    forgottenTerminalID += nextTerminalID[1:]
                if printt == 1:
                    print('Оставшиеся терминалы:', forgottenTerminalID)
                    print()

                #   ---- Если дальше нет терминала
                if nextTerminalID == []:
                    lastNodeID += [['пустая шина', nodeName, nextNodeID]]
                    usl2 = False
                    continue

                # ---- Запрос на проверку предохранителя
                for v in variantID:
                    ptxLocID = cursorObj.execute(
                        f"SELECT ProtLoc_ID FROM ProtLocation "
                        f"WHERE Terminal_ID IN ({str(nextTerminalID[0])}) AND Variant_ID IN ({v})").fetchone()
                    if ptxLocID is None:
                        continue
                    else:
                        ptxLocID = ptxLocID[0]
                        for vv in variantID:
                            ptxName = cursorObj.execute(
                                f"SELECT p_nam FROM ProtOCSetting "
                                f"WHERE ProtLoc_ID IN ({str(ptxLocID)}) AND Variant_ID IN ({vv})").fetchone()
                            if ptxName is None:
                                continue
                            else:
                                ptxName = ptxName[0]
                                break
                        break
                # ---- Если дальше не стоит предохранитель
                if ptxLocID is None:
                    continue

                # ---- Если дальше стоит предохранитель


                if ptxName is None:
                    print('УСТРОЙСТВО ЗАЩИТЫ БЕЗ НАЗВАНИЯ')
                    nnProt += [ptxLocID]
                    continue
                else:

                    # ---- Проверка соответствия названия предохранителя с названием преда
                    if ptxName in listOfPkt:
                        if usl3 == 1:
                            lastNodeID += [['pkt', nodeName, nextNodeID]]
                            if printt == 1:
                                print('alonetermwithptx')
                        usl2 = False
                    else:
                        notInLibrPtx += [[ptxLocID, ptxName]]
                if printt == 1:
                    print()
        lastNodes += [[]]
        for i in range(len(lastNodeID)):
            lastNodes[prot2] += [lastNodeID[i][2]]

        allProtLastNodeID += [lastNodeID, FlagParent, protTerminalID[prot2], protElementID[prot2]]
    print(lastNodes)
    print(checkedTerm)
    print('УЗЛЫ ПО ЗАЩИТАМ:', allProtLastNodeID)
    print()

    """
   #####################################################################################################################
   #---------------------------5. РАСЧЁТ УСТАВОК ТОКА ДЛЯ ТОВВ, MTO И МТЗ----------------------------------------------#
   #####################################################################################################################
   """

    for prot2 in range(len(protElementID)):
        print('УСТАВКИ ДЛЯ УРЗА НА ЭЛЕМЕНТЕ: ', protElementName[prot2])
        # ---- Элементы с двухступенчатыми токовыми защитами
        print(allProtLastNodeID)
        if allProtLastNodeID[prot2 * 4 + 1][1] == 0:
            timeparent += [[protElementName[prot2]]]

        # ---- Выбор коэффициента кратности для УРЗА
        kttList = {'75/5': 15, '100/5': 20, '150/5': 30, '200/5': 40, '300/5': 60, '400/5': 80, '600/5': 120}
        for key, value in kttList.items():
            print(key, '-', value, end='; ')
            print()
        ktt = input('Введите коэфициент кратности трансформатора тока на Линии ' + str(
            protElementName[prot2]) + ' (примеры в таблице выше):')

        '''
       ТОКОВАЯ ОТСЕЧКА С ВЫДЕРЖКОЙ ВРЕМЕНИ
       '''
        # ---- Ток короткого замыкания в конце защищаемого участка
        Ik3l = []
        for ust1 in range(len(lastNodes[prot2])):
            for v in variantID:
                Ik3_ = cursorObj.execute(
                    f"SELECT Ik2 FROM SC3NodeResult "
                    f"WHERE Node_ID IN ({str(lastNodes[prot2][ust1])}) AND Variant_ID IN ({v})").fetchone()
                if Ik3_ is None:
                    continue
                else:
                    Ik3_ = Ik3_[0]
                    break
            Ik3l += [Ik3_]
        print('Значения тока в конечных узлах:', Ik3l)
        Ik3 = min(Ik3l)
        Ik3 = Ik3 * 1000
        print('Минимальный ток:', Ik3)

        # ---- Определение коэффициента надежности для расчёта токовой отсечки
        if defaultValues == 2:
            usl1 = input('Коэффициент надежности равен 1.3? 1 - Да, 2 - Ввести свое значение:')
        else:
            usl1 = 1

        if int(usl1) == 2:
            knto = input('Введите коэффициент надежности токовой отсечки:')
        elif int(usl1) == 1:
            knto = 1.3
        else:
            print('Вы ввели некорректное значение, коэффициент трансформации был принят за 1.3')
            knto = 1.3

        # ---- Расчётная формула ТО
        Isztovv = Ik3 * float(knto) / float(ktt)
        print('Ток срабатывания ТО', Isztovv)

        # ---- ProtLoc_ID рассматриваемой защиты
        protTerminalID0 = protTerminalID[prot2]
        for v in variantID:
            protLocID = cursorObj.execute(
                f"SELECT ProtLoc_ID FROM ProtLocation "
                f"WHERE Terminal_ID IN ({str(protTerminalID0)}) AND Variant_ID IN ({v})").fetchone()
            if protLocID is None:
                continue
            else:
                protLocID = protLocID[0]
                break

        #   ---- Просмотр значения sw (0 или 1)
        for v in variantID:
            sw1 = cursorObj.execute(
                f"SELECT sw1 FROM ProtOCSetting "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN  ({v})").fetchone()
            sw2 = cursorObj.execute(
                f"SELECT sw2 FROM ProtOCSetting "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN  ({v})").fetchone()
            sw3 = cursorObj.execute(
                f"SELECT sw3 FROM ProtOCSetting "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN  ({v})").fetchone()
            sw4 = cursorObj.execute(
                f"SELECT sw4 FROM ProtOCSetting "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN  ({v})").fetchone()
            if sw1 is None:
                continue
            else:
                sw1 = sw1[0]
                sw2 = sw2[0]
                sw3 = sw3[0]
                sw4 = sw4[0]
                break

        #   ---- Условие не обработанной защиты
        if sw1 == 0 and sw2 == 0 and sw3 == 0 and sw4 == 0:
            print('Параметры защиты не введены')
            continue

        #   ---- Условие наличия третьей ступени
        Isztovv = round(Isztovv, 3)
        print('protLocID, Isztovv: ' + str(protLocID) + ', ' + str(Isztovv))

        """
        МГНОВЕННАЯ ТОКОВАЯ ОТСЕЧКА
        """
        for v in variantID:
            Imto = cursorObj.execute(
                f"SELECT Ik2 FROM SC3NodeResult "
                f"WHERE Node_ID='{protNodeID2[prot2]}' AND Variant_ID IN ({v})").fetchone()
            if Imto is None:
                continue
            else:
                Imto = Imto[0]
                break
        Imto = Imto * 1000
        Iszmto = float(Imto) * float(knto) / float(ktt)
        Iszmto = round(Iszmto, 3)

        """
        МАКСИМАЛЬНАЯ ТОКОВАЯ ЗАЩИТА
        """
        # ---- Рабочий максимальный ток (ТУТ НУЖНО УБЕДИТЬСЯ ВЕРНЫ ЛИ НАПРАВЛЕНИЯ ЭЛЕМЕНТОВ)
        for v in variantID:
            Imtz = cursorObj.execute(
                f"SELECT I FROM QueryResultLFBranch "
                f"WHERE Terminal1_ID IN ({str(protTerminalID[prot2])}) AND Variant_ID IN ({v})").fetchone()
            if Imtz is None:
                continue
            else:
                Imtz = Imtz[0]
                break
        Imtz = Imtz * 1000
        Imtz = round(Imtz, 3)

        print('Рабочий максимальный ток:', Imtz)

        # ---- Ввод коэффициентов
        if defaultValues == 2:
            usl2 = input('Коэффициенты надежности, самозапуска и возврата равны соответственно: 1.3, 1.5 и 0.95?'
                         '1 - Да, 2 - Ввести свое значение ')
        else:
            usl2 = 1
        if int(usl2) == 2:
            knmtz = input('Введите коэффициент надежности максимальной токовой защиты(Как правило, 1.3):')
            kszpmtz = input('Введите коэффициент самозапуска максимальной токовой защиты(Как правило, 1.5):')
            kvmtz = input('Введите коэффициент возврата максимальной токовой защиты(Как правило, 0.95):')
        if int(usl2) == 1:
            knmtz = 1.3
            kszpmtz = 1.5
            kvmtz = 0.95
        else:
            print('Вы ввели некорректное значение, коэффициенты были приняты по умолчанию')
            knmtz = 1.3
            kszpmtz = 1.5
            kvmtz = 0.95

        # ---- Расчётная формула уставки срабатывания МТЗ
        Iszmtz = (float(knmtz) * float(kszpmtz) * float(Imtz)) / float(kvmtz) / float(ktt)
        Iszmtz = round(Iszmtz, 3)

        print('Значение срабатывания МТЗ', Iszmtz)
        print('Значение срабатывания МТО', Iszmto)
        print('Значение срабатывания ТОВВ', Isztovv)

        """
        Ввод уставок по току
        """
        for v in variantID:
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET ip_g=({str(Iszmtz)}) "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN ({v})")
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET ip_2g=({str(Iszmto)}) "
                f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN ({v})")
            if cursorObj.execute(f"SELECT ip_2g FROM ProtOCSetting "
                                 f"WHERE ProtLoc_ID IN ({str(protLocID)}) "
                                 f"AND Variant_ID IN ({v})").fetchone() == (str(Iszmto),):
                break
        if allProtLastNodeID[prot2 * 4 + 1][1] == 1:
            # Ввод в ip_3g
            for v in variantID:
                cursorObj.execute(
                    f"UPDATE ProtOCSetting SET ip_3g=({str(Isztovv)}) "
                    f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN ({v})")
                print('3-х ступенчатая токовая защита')
                if cursorObj.execute(f"SELECT ip_3g FROM ProtOCSetting "
                                     f"WHERE ProtLoc_ID IN ({str(protLocID)}) "
                                     f"AND Variant_ID IN ({v})").fetchone() == (str(Isztovv),):
                    break
        else:
            # Ввод в ip_2g
            # cursorObj.execute(
            #     "UPDATE ProtOCSetting SET ip_2g=({0}) WHERE ProtLoc_ID=({1})".format(str(Isztovv), str(protLocID)))
            for v in variantID:
                cursorObj.execute(f"UPDATE ProtOCSetting SET sw4='0' "
                                  f"WHERE ProtLoc_ID IN ({str(protLocID)}) AND Variant_ID IN ({v})")
            for v in variantID:
                if cursorObj.execute(f"SELECT sw4 FROM ProtOCSetting "
                                     f"WHERE ProtLoc_ID IN ({str(protLocID)}) "
                                     f"AND Variant_ID IN ({v})").fetchone() == (0,):
                    break
            print('2-х ступенчатая токовая защита')
        print()

    """
    ####################################################################################################################
    #-----------------------------------6. ВЫБОР УСТАВОК ПО ВРЕМЕНИ----------------------------------------------------#
    ####################################################################################################################
    """

    """
    Формирование необходимых списков
    """
    checkingProtElementID = []

    for sirotaprot in range(len(allProtLastNodeID) // 4):
        if allProtLastNodeID[sirotaprot * 4 + 1][1] == 0 and protElementID != []:
            checkingProtElementID += [allProtLastNodeID[sirotaprot * 4 + 3]]
    print('Защиты начала сканера:', checkingProtElementID)
    prot3 = -1
    InfeederID = []
    for v in variantID:
        InfeederID0 = cursorObj.execute(f"SELECT Element_ID FROM Element "
                                        f"WHERE Type='Infeeder' "
                                        f"AND Variant_ID IN ({v})").fetchall()
        InfeederID += name_changer(InfeederID0)
        InfeederID = sorted(list(set(InfeederID)))
    print('Источник(и):', InfeederID)
    while len(checkingProtElementID) != 0:
        print('\n\n\n', timeparent, '\n\n\n')

        """
        Вокабуляр
        """
        nextElementID = []              # ---- Рассматриваемый элемент
        forgottenElementID = ['START']  # ---- Элементы, которые необходимо рассмотреть
        nextTerminalID = []

        """
        Первичное заполнение timelist
        """
        usl1 = True  # False, когда следующий элемент - источник
        while usl1 is True:
            # ---- ПЕРВАЯ ИТЕРАЦИЯ
            if nextElementID == [] and forgottenElementID == ['START']:
                if checkingProtElementID == []:
                    usl1 = False
                    break
                for v in variantID:
                    thisTerminalID = cursorObj.execute(
                        f"SELECT Terminal_ID FROM Terminal "
                        f"WHERE Element_ID IN ({str(checkingProtElementID[prot3])}) "
                        f"AND TerminalNo='1' AND Variant_ID IN ({v})").fetchone()
                    if thisTerminalID is None:
                        continue
                    else:
                        thisTerminalID = thisTerminalID[0]
                        break
                forgottenElementID = [] # ---- Больше незачем использовать эту переменную в качестве флага начала
                checkingProtElementID = checkingProtElementID[:prot3] # ---- отсекаем последний элемент из списка защит

            # ---- ПОСЛЕДУЮЩИЕ ИТЕРАЦИИ
            else:
                # ---- Условие наличия рассматриваемых элементов
                if nextElementID != []:
                    for v in variantID:
                        thisTerminalID = cursorObj.execute(
                            f"SELECT Terminal_ID FROM Terminal "
                            f"WHERE Element_ID IN ({str(nextElementID[prot3])}) "
                            f"AND TerminalNo='1' AND Variant_ID IN ({v}) AND Flag_Variant='1'").fetchone()
                        if thisTerminalID is None:
                            continue
                        else:
                            thisTerminalID = thisTerminalID[0]
                            break
                    # ---- Условие нескольких элементов за узлом
                    if len(nextElementID) > 1:
                        forgottenElementID += nextElementID[:prot3]
                    nextElementID = []

                # ---- Условия перехода на элемент, который необходимо рассмотреть
                elif nextElementID == [] and forgottenElementID != []:
                    for v in variantID:
                        thisTerminalID = cursorObj.execute(
                            f"SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({str(forgottenElementID[prot3])}) "
                            f"AND TerminalNo='1' AND Variant_ID IN ({v}) AND Flag_Variant='1'").fetchone()
                        if thisTerminalID is None:
                            continue
                        else:
                            thisTerminalID = thisTerminalID[0]
                            break
                    forgottenElementID = forgottenElementID[:prot3]

                # ---- Условие конца
                else:
                    usl1 = False
                    break

            for v in variantID:
                nextNodeID = cursorObj.execute(
                    f"SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({str(thisTerminalID)})"
                    f"AND Variant_ID IN ({v}) AND Flag_Variant='1'").fetchone()
                if nextNodeID is None:
                    continue
                else:
                    nextNodeID = nextNodeID[0]
                    break
            nextTerminalID = []
            for v in variantID:
                nextTerminalID = varID(v, 3)

            flagFeeder = 0  # ---- Флаг на наличие inфидера

            for prot4 in range(len(nextTerminalID)):
                for v in variantID:
                    thisElementID = cursorObj.execute(
                        f"SELECT Element_ID FROM Terminal "
                        f"WHERE Terminal_ID IN ({str(nextTerminalID[prot4])}) AND Variant_ID IN ({v}) "
                        f"AND Flag_Variant='1'").fetchone()
                    if thisElementID is None:
                        continue
                    else:
                        thisElementID = thisElementID[0]
                        break
                print('Проссматриваемый элемент:', thisElementID)
                if thisElementID != None:
                    nextElementID += [thisElementID]

                # ---- Условие прекращения итерации при появлении inфидера
                if thisElementID in InfeederID:
                    flagFeeder = 1
                    break

                # ----
                if thisElementID in protElementID:
                    for v in variantID:
                        elementName = cursorObj.execute(
                            f"SELECT Name FROM Element "
                            f"WHERE Element_ID IN ({str(thisElementID)}) AND Variant_ID IN ({v})").fetchone()
                        if elementName is None:
                            continue
                        else:
                            elementName = elementName[0]
                            break
                    print('То, с чем он заходит: \n Список существующих цепей:', timelist, ', Родительская защита:',
                          timeparent[prot3], ', Название элемента с защитой: ', elementName)
                    timelist = time1(timelist, timeparent[prot3][0], elementName)
                    timeparent = timeparent[:prot3]
            if flagFeeder == 1:
                print('\nИСТОЧНИК:', thisElementID)
                usl1 = False
                parentProt = timeparent[:prot3]
                break
        if timelist == []:
            timelist += [timeparent[prot3]]
    if timelist == []:
        print('На фидере нет защит')
        continue
    timelist = timecorr(timelist)  # ---- Вторичное заполнение timelist
    if defaultValues == 1:
        timeprot = 0.2
        timesel = 0.1
    else:
        timeprot = round(float(input('Введите максимальное время сгорания предохранителя (при отсутствии - 0): ')), 1)
        timesel = round(float(input('Введите ступень селективности: ')), 1)
    timelist = time2(timelist, timeprot, timesel)  # ---- Третичное заполнение timelist
    timeInfo = time3(timelist, timeprot, timesel)  # ---- Формирование итогового списка для введения уставок времени
    if defaultValues == 1:
        timeprot = 0.2
    else:
        timeprot = float(input('Введите максимальное время сгорания предохранителя: '))

    print('timeInfo', timeInfo)
    dpi = list(dictProtInfo)
    print('Названия линий и их ID:', dpi)

    for k in range(len(timeInfo)):
        print(list(dpi))
        for l in range(len(timeInfo[k])):
            ti = list(timeInfo[k][l].items())
            print('Уставки времени:', ti[0])
            print('Протлоки рассматриваемых защит:', next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0]))

            """
            Заполнение уставок времени в бд
            """
            if len(ti[0][1]) == 2:
                for v in variantID:
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET tp_g=({ti[0][1][0][0]}) "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET tp_2g=({ti[0][1][1][0]}) "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
            else:
                for v in variantID:
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET tp_g=({ti[0][1][0][0]}) "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET tp_2g=({ti[0][1][1][0]}) "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET tp_3g=({ti[0][1][2][0]}) "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
                    cursorObj.execute(
                        f"UPDATE ProtOCSetting SET sw4='1' "
                        f"WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})"
                        f"AND Variant_ID IN ({v})")
            print()

a = input('Нажмите 1, чтобы сохранить изменения')
if a == '1':
    print('Сохранено')
    con.commit()  # ---- Подтверждение изменений в БД
    con.close()
else:
    print('Не сохранено')
# ---- Последняя строчка кода