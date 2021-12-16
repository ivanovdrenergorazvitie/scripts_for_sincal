import sqlite3
import pandas as pd


def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

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
def timecorr(e):
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
    return l
def time2(a):
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
def time3(z):
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
        for i in range(nc):
            key = (str(z[j][i]).split(':')[0])[2:-1]
            if i == 0:
                z[j][i][key] = [0.001], [round(0.1 * nc, 1)]
            else:
                z[j][i][key] = [float(str(0.1 * (i + nc))[:3])], [float(str(0.1 * i)[:3])], [0.001]
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
        fKey = z[j]  # Забираем список словарей
        for i in range(len(z[j])):
            t1 = 0
            key1 = (str(z[j][i]).split(':')[0])[2:-1]
            if i == 0:
                z[j][i][key1] = [0.001], [round(0.1 * nc, 1)]
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
                    if z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][-1] < [round(float(0.1 * i), 3)]:
                        z[j][i][key1] = [float(str(0.1 * (i + nc))[:3])], [float(str(0.1 * i)[:3])], [0.001]
                    else:
                        z[j][i][key1] = [float(z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + 0.1 * nc], [
                            float(z[j][i - 1][(str(z[j][i - 1]).split(':')[0])[2:-1]][0]) + 0.1], [0.001]
                if t1 != 0:
                    z[j][i][key1] = t1
    return z


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()
protTerminalID = []

"""
СОСТАВЛЕНИЕ СПИСКА РЕКЛОУЗЕРОВ
"""

#   ---- ---- ОПРЕДЕЛЕНИЕ СВЯЗКИ ЛИНИЙ С ЗАЩИТАМИ 'ПКТ-10 (50 A)'
#   ---- Выбор рассматриваемой защиты             'ПКТ-10 (50 A)'
listOfPkt = ('ПКТ-10 (2 A)', 'ПКТ-10 (3 A)', 'ПКТ-10 (5 A)', 'ПКТ-10 (8 A)', 'ПКТ-10 (10 A)', 'ПКТ-10 (16 A)',
             'ПКТ-10 (20 A)', 'ПКТ-10 (31 A)', 'ПКТ-10 (40 A)', 'ПКТ-10 (50 A)', 'ПКТ-10 (80 A)', 'ПКТ-10 (100 A)',
             'ПКТ-10 (160 A)', 'ПКТ-6 (2 A)', 'ПКТ-6 (3 A)', 'ПКТ-6 (5 A)', 'ПКТ-6 (8 A)', 'ПКТ-6 (10 A)',
             'ПКТ-6 (16 A)', 'ПКТ-6 (20 A)', 'ПКТ-6 (31 A)', 'ПКТ-6 (40 A)', 'ПКТ-6 (50 A)', 'ПКТ-6 (63 A)',
             'ПКТ-6 (80 A)', 'ПКТ-6 (100 A)', 'ПКТ-6 (160 A)', 'ПКТ-6 (200 A)', 'ПКТ-6 (315 A)')
protInfo = []

protInfo0 = cursorObj.execute(
    "SELECT ProtLoc_ID FROM ProtOCSetting WHERE p_nam NOT LIKE '%ПКТ-6%' AND p_nam NOT LIKE '%ПКТ-10%'").fetchall()
protInfo = name_changer(protInfo0)

print('protInfo', protInfo)

ptxTerminalID = []
for ptx1 in range(len(protInfo)):
    ptxTerminalID0 = cursorObj.execute(
        "SELECT Terminal_ID FROM ProtLocation WHERE ProtLoc_ID IN ({0})".format(
            str(protInfo[ptx1]))).fetchone()
    ptxTerminalID += [ptxTerminalID0[0]]
print('ptxTerminalID', ptxTerminalID)
ptxGTerminalID = []
for ptx2 in range(len(ptxTerminalID)):
    ptxGTerminalID0 = cursorObj.execute(
        "SELECT GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
            str(ptxTerminalID[ptx2]))).fetchone()
    if ptxGTerminalID0 == []:
        continue
    elif ptxGTerminalID0 is None:
        continue
    else:
        ptxGTerminalID += [ptxGTerminalID0[0]]
print('ptxGTerminalID', ptxGTerminalID)
allProtGTerminalID = []
for ptx3 in range(len(ptxGTerminalID)):
    allProtGTerminalID0 = cursorObj.execute(
        "SELECT GraphicTerminal_ID FROM GraphicAddTerminal WHERE SymType LIKE 1 AND FrgndColor LIKE ({0}) AND GraphicTerminal_ID IN ({1})".format(
            '255', str(ptxGTerminalID[ptx3]))).fetchone()

    if allProtGTerminalID0 == []:
        continue
    elif allProtGTerminalID0 is None:
        continue
    else:
        allProtGTerminalID += [allProtGTerminalID0[0]]
print('GТерминалы с защитами:', allProtGTerminalID)
#   ---- Terminal_ID, в котором находится защита
for prot1 in range(len(allProtGTerminalID)):
    protTerminalID0 = cursorObj.execute(
        "SELECT Terminal_ID FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({0})".format(
            str(allProtGTerminalID[prot1]))).fetchall()
    protTerminalID0 = name_changer(protTerminalID0)
    if protTerminalID0 == []:
        continue
    elif protTerminalID0 is None:
        continue
    else:
        protTerminalID += protTerminalID0
print('Терминалы с защитами:', protTerminalID)
protLocID = []
for prot2 in range(len(protTerminalID)):
    ProtLocID = cursorObj.execute(
        "SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0})".format(
            str(protTerminalID[prot2]))).fetchone()[0]
    cursorObj.execute(
        "UPDATE ProtOCSetting SET ProtCharP_ID='4095' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    cursorObj.execute(
        "UPDATE ProtOCSetting SET ProtCharE_ID='4095' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    cursorObj.execute(
        "UPDATE ProtOCSetting SET p_nam='Сириус-2-Л INV' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    cursorObj.execute(
        "UPDATE ProtOCSetting SET e_nam='Сириус-2-Л INV' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    cursorObj.execute(
        "UPDATE ProtOCSetting SET sw2='1' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    cursorObj.execute(
        "UPDATE ProtOCSetting SET sw3='1' WHERE ProtLoc_ID IN ({0})".format(str(ProtLocID)))
    protLocID += [ProtLocID]
    print(ProtLocID)

protElementID = []
protElementName = []
for prot in range(len(protTerminalID)):
    protElementID0 = cursorObj.execute(
        "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
            str(protTerminalID[prot]))).fetchall()
    protElementID0 = name_changer(protElementID0)
    protElementID += [protElementID0[0]]
    protElementName0 = cursorObj.execute(
        "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(protElementID0[0])).fetchone()[0]
    protElementName += [protElementName0]
print('EBEYSHI SPISOK', protElementID, protElementName)
dictProtInfo = zip(protElementName, protElementID, protLocID)
"""
СОСТАВЛЕНИЕ СПИСКА ИЗ ПОСЛЕДНИХ УЗЛОВ
Игнорируем элементы хотя бы без одного из двух терминалов и элементы с предохранителями
"""

# stopWhileProt = 0
allProtLastNodeID = []
timeinfo = []
timelist = []
timeparent = []
for prot2 in range(len(protElementID)):
    nextNodeID = []
    listOfLastNode = []
    lastNodeID = []
    checkedTerminalID = []
    forgottenTerminalID = []
    nextTerminalID = []
    usl1 = True  # False, когда закончатся forgottenTerminalID - Когда надо перейти к следующей защите
    FlagParent = ['НЕТ РЕКЛОУЗЕРА НА ПУТИ', 0]

    while usl1 is True:

        usl2 = True  # False, когда последняя шина - Когда надо вернуться к пропущенному терминалу
        if forgottenTerminalID == [] and nextTerminalID != []:
            usl1 = False
            continue
        print(usl1)
        nextTerminalID = []

        for osn1 in range(len(forgottenTerminalID)):
            nextTerminalID += [forgottenTerminalID[osn1]]
        print('\nВышли из условия\nНекст терминал:', nextTerminalID, '\n')
        while usl2 is True:
            usl3 = 1
            flagForProt2 = 1
            #   Элемент
            if nextTerminalID == []:
                protTerminalNo = cursorObj.execute(
                    "SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(protTerminalID[prot2]))).fetchall()
                protTerminalNo = name_changer(protTerminalNo)
                if protTerminalNo == [1]:
                    thisElementID = cursorObj.execute(
                        "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                            str(protTerminalID[prot2]))).fetchall()
                    thisElementID = name_changer(thisElementID)
                    elementNameID = cursorObj.execute(
                        "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                            str(thisElementID[0]))).fetchall()
                    print('Элемент с защитами:', thisElementID, elementNameID[0][0])
                elif protTerminalNo == [2]:
                    flagForProt2 = 0
                else:
                    print('Ну капуц')
            else:
                if nextTerminalID == forgottenTerminalID:
                    removeTerminalID = nextTerminalID[0]
                    forgottenTerminalID.remove(removeTerminalID)
                if len(nextTerminalID) > 1:
                    usl3 = 0

                thisElementID = cursorObj.execute(
                    "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(nextTerminalID[0]))).fetchall()
                thisElementID = name_changer(thisElementID)
                elementName = cursorObj.execute(
                    "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                        str(thisElementID[0]))).fetchall()
                print('Просматриваемый элемент:', thisElementID, elementName[0][0])
                try:
                    print('\n\n\n\n\n', thisElementID[0], protElementID)
                    protElementID.index(thisElementID[0])
                    usl2 = False
                    FlagParent = ['ЕСТЬ РЕКЛОУЗЕР НА ПУТИ', 1]
                    continue
                except:
                    usl2 = True
            #   Терминал конца элемента
            if flagForProt2 == 1:
                endTerminalID = cursorObj.execute(
                    "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo LIKE 2".format(
                        str(thisElementID[0]))).fetchall()
                endTerminalID = name_changer(endTerminalID)

                print('Терминал в конце элемента:', endTerminalID)
                # input('Продолжить')
                if endTerminalID == []:
                    if usl3 == 1:
                        lastNodeID += [['load', nodeName, nextNodeID[0]]]
                    usl2 = False
                    continue
                if nextNodeID != []:
                    nextNodeID0 = nextNodeID
            if flagForProt2 == 1:
                nextNodeID = cursorObj.execute(
                    "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(endTerminalID[0]))).fetchall()
            elif flagForProt2 == 0:
                nextNodeID = cursorObj.execute(
                    "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(protTerminalID[prot2]))).fetchall()
            nextNodeID = name_changer(nextNodeID)
            checkedTerminalID += (nextNodeID)
            print('Просмотренные терминалы:', checkedTerminalID)
            print('Следующий узел:', nextNodeID)
            nodeName = cursorObj.execute(
                "SELECT Name FROM Node WHERE Node_ID IN ({0})".format(str(nextNodeID[0]))).fetchone()[0]
            print('Рассматриваемый узел', nodeName)

            #   Следующий терминал
            nextTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND TerminalNo IN ({1})".format(
                    str(nextNodeID[0]), '1')).fetchall()
            nextTerminalID = name_changer(nextTerminalID)
            print('Некст терминал:', nextTerminalID)

            #   ---- Если терминал не один
            usl3 = 1
            if len(nextTerminalID) > 1:
                usl3 = 0
                forgottenTerminalID += (nextTerminalID[1:])
            print('Оставшиеся терминалы:', forgottenTerminalID)
            print()

            #   ---- Если дальше нет терминала
            if nextTerminalID == []:
                lastNodeID += [['пустая шина', nodeName, nextNodeID[0]]]
                usl2 = False
                continue
            #   ---- Если дальше стоит предохранитель
            ptxLocID = cursorObj.execute(
                "SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0})".format(
                    str(nextTerminalID[0]))).fetchone()
            if ptxLocID is None:
                continue
            else:
                ptxName = cursorObj.execute(
                    "SELECT p_nam FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
                        str(ptxLocID[0]))).fetchone()
            if ptxName[0] is None:
                continue
            else:
                if ptxName[0] in listOfPkt:
                    if usl3 == 1:
                        lastNodeID += [['pkt', nodeName, nextNodeID[0]]]
                        print('alonetermwithptx')
                    usl2 = False
            print()

    print('ТО, РАДИ ЧЕГО МЫ ЗДЕСЬ СОБРАЛИСЬ:', lastNodeID)
    allProtLastNodeID += [lastNodeID, FlagParent, protTerminalID[prot2], protElementID[prot2]]
    print('Это узлы по защитам. Формирование списка надо фиксить:', allProtLastNodeID)

    """
    РАСЧЁТ УСТАВОК
    """

    # timeLastNode = {}
    if FlagParent[1] == 0:
        # t0Prot = cursorObj.execute("SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0})".format(
        #     str(protTerminalID[prot2]))).fetchone()[0]
        # cursorObj.execute("UPDATE ProtOCSetting SET tp_2g='0.001' WHERE ProtLoc_ID IN ({0})".format(str(t0Prot)))
        # print('В данную защиту вбито значение выдержки времени 0,001с:', t0Prot)
        # timeLastNode[protElementName[prot2]] = [0.001]
        # timeinfo += [[timeLastNode]]
        timeparent += [[protElementName[prot2]]]
        print(timeparent)

    #   ---- ---- ВВОД УСТАВОК
    kttList = {'75/5': 15, '100/5': 20, '150/5': 30, '200/5': 40, '300/5': 60, '400/5': 80, '600/5': 120}
    for key, value in kttList.items():
        print(key, '-', value, end='; ')
        print()
    ktt = input('Введите коэфициент кратности трансформатора тока на Линии ' + str(
        protElementName[prot2]) + ' (примеры в таблице выше):')
    #   ---- Ток короткого замыкания в конце защищаемого участка
    Ik3l = []
    for ust1 in range(len(lastNodeID)):
        Ik3_ = cursorObj.execute(
            "SELECT Ik2 FROM SC3NodeResult WHERE Node_ID IN ({0})".format(
                str(lastNodeID[ust1][2]))).fetchone()[0]
        Ik3l += [Ik3_]
    print(Ik3l)
    Ik3 = min(Ik3l)
    Ik3 = Ik3 * 1000
    print('Ik3', Ik3)

    # usl1 = input('Коэффициент надежности равен 1.3? 1 - Да, 2 - Ввести свое значение:')
    usl1 = 1

    if int(usl1) == 2:
        knto = input('Введите коэффициент надежности токовой отсечки:')
    elif int(usl1) == 1:
        knto = 1.3
    else:
        print('Вы ввели некорректное значение, коэффициент трансформации был принят за 1.3')
        knto = 1.3

    Iszto = Ik3 * float(knto) / float(ktt)
    print('Ток срабатывания ТО', Iszto)
    #   ---- ProtLoc_ID рассматриваемой защиты
    print(protTerminalID)
    protTerminalID0 = protTerminalID[prot2]
    protLocID0 = cursorObj.execute(
        "SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0})".format(
            str(protTerminalID0))).fetchall()
    protLocID0 = name_changer(protLocID0)

    #   ---- Просмотр значения sw (0 или 1)
    protLocID = protLocID0[0]
    sw1 = cursorObj.execute(
        "SELECT sw1 FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
            str(protLocID))).fetchall()
    sw1 = name_changer(sw1)
    sw2 = cursorObj.execute(
        "SELECT sw2 FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
            str(protLocID))).fetchall()
    sw2 = name_changer(sw2)
    sw3 = cursorObj.execute(
        "SELECT sw3 FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
            str(protLocID))).fetchall()
    sw3 = name_changer(sw3)

    sw4 = cursorObj.execute(
        "SELECT sw4 FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
            str(protLocID))).fetchall()
    sw4 = name_changer(sw4)

    sw1 = sw1[0]
    sw2 = sw2[0]
    sw3 = sw3[0]
    sw4 = sw4[0]

    #   ---- Условие не обработанной защиты
    if sw1 == 0 and sw2 == 0 and sw3 == 0 and sw4 == 0:
        print('Параметры защиты не введены')
        continue

    #   ---- Условие наличия третьей ступени
    Iszto = round(Iszto, 3)
    print('protLocID, Iszto: ' + str(protLocID) + ', ' + str(Iszto))
    if sw4 == 0:
        print('2-х ступенчатая токовая защита')
        # Ввод в ip_2g
        cursorObj.execute(
            "UPDATE ProtOCSetting SET ip_2g=({0}) WHERE ProtLoc_ID=({1})".format(str(Iszto), str(protLocID)))

        print('Значение ip_2g заменено на:', Iszto)
    elif sw4 == 1:
        print('3-х ступенчатая токовая защита')
        # Ввод в ip_3g
        cursorObj.execute(
            "UPDATE ProtOCSetting SET ip_3g=({0}) WHERE ProtLoc_ID=({1})".format(str(Iszto), str(protLocID)))

        print('Значение ip_3g заменено на:', Iszto)

    #   ---- ---- МАКСИМАЛЬНАЯ ТОКОВАЯ ЗАЩИТА
    #   ---- Ток срабатывания

    #   ---- Рабочий максимальный ток
    Imtz = cursorObj.execute(
        "SELECT I FROM QueryResultLFBranch WHERE Terminal1_ID IN ({0})".format(str(protTerminalID[prot2]))).fetchall()
    Imtz = name_changer(Imtz)
    Imtz = Imtz[0] * 1000
    Imtz = round(Imtz, 3)

    print('\nРабочий максимальный ток:', Imtz)

    #   ---- Ввод коэффициентов
    #     usl2 = input('Коэффициенты надежности, самозапуска и возврата равны соответственно: 1.3, 1.5 и 0.95?'
    #                  '1 - Да, 2 - Ввести свое значение ')
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

    for key, value in kttList.items():
        print(key, '-', value, end='; ')
        print()

    Iszmtz = (float(knmtz) * float(kszpmtz) * float(Imtz)) / float(kvmtz) / float(ktt)
    Iszmtz = round(Iszmtz, 3)
    print()
    print('Значение срабатывания МТЗ', Iszmtz)
    print('Значение срабатывания ТО', Iszto)

    cursorObj.execute(
        "UPDATE ProtOCSetting SET ip_g=({0}) WHERE ProtLoc_ID=({1})".format(str(Iszmtz), str(protLocID)))
# timeparent = []
# for parentProt in timelist:
#     timeparent += [parentProt]
"""
ВЫБОР УСТАВКИ ВРЕМЕНИ
"""
checkingProtElementID = []
for sirotaprot in range(len(allProtLastNodeID)//4):
    if allProtLastNodeID[sirotaprot * 4 + 1][1] == 0:
        checkingProtElementID += [allProtLastNodeID[sirotaprot * 4 + 3]]
print('Защиты начала сканера:', checkingProtElementID)
prot3 = -1
InfeederID = cursorObj.execute("SELECT Element_ID FROM Element WHERE Type='Infeeder'").fetchall()
InfeederID = name_changer(InfeederID)
print('Источник(и):', InfeederID)
while len(checkingProtElementID) != 0:
    print('\n\n\n', timeparent, '\n\n\n')
    nextNodeID = []
    nextElementID = []
    checkedTerminalID = []
    forgottenElementID = ['START']
    # thisPElName = cursorObj.execute(
    #     "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
    #         str(parentProt[prot3]))).fetchone()[0]
    usl1 = True  # False, когда следующий элемент - источник
    while usl1 is True:
        if nextElementID == [] and forgottenElementID == ['START']:
            if checkingProtElementID == []:
                usl1 = False
                break
            thisTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo='1'".format(
                    str(checkingProtElementID[prot3]))).fetchone()[0]
            forgottenElementID = []
            checkingProtElementID = checkingProtElementID[:prot3]

        else:
            if nextElementID != []:
                thisTerminalID = cursorObj.execute(
                    "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo='1'".format(
                        str(nextElementID[prot3]))).fetchone()[0]
                if len(nextElementID) > 1:
                    forgottenElementID += nextElementID[:prot3]
                nextElementID = []
            elif nextElementID == [] and forgottenElementID != []:
                thisTerminalID = cursorObj.execute(
                    "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo='1'".format(
                        str(forgottenElementID[prot3]))).fetchone()[0]
                forgottenElementID = forgottenElementID[:prot3]
            else:
                usl1 = False
                break

        nextNodeID = cursorObj.execute(
            "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                str(thisTerminalID))).fetchone()[0]
        nextTerminalID = cursorObj.execute(
            "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND TerminalNo='2'".format(
                str(nextNodeID))).fetchall()
        nextTerminalID = name_changer(nextTerminalID)
        flagFeeder = 0
        for prot4 in range(len(nextTerminalID)):
            thisElementID = cursorObj.execute(
                "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(nextTerminalID[prot4]))).fetchone()[0]
            print('Проссматриваемый элемент:', thisElementID)
            nextElementID += [thisElementID]

            if thisElementID in InfeederID:
                flagFeeder = 1
                break
            if thisElementID in protElementID:
                elementName = cursorObj.execute(
                    "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                        str(thisElementID))).fetchone()[0]
                print('То, с чем он заходит: \n Список существующих цепей:', timelist, ', Родительская защита:', timeparent[prot3][0], ', Айди Элемента с защитой: ', elementName)
                timelist = time1(timelist, timeparent[prot3][0], elementName)
                timeparent = timeparent[:prot3]
        if flagFeeder == 1:
            print('\nИСТОЧНИК:', thisElementID)
            usl1 = False
            parentProt = timeparent[:prot3]
            break

timelist = timecorr(timelist)
timelist = time2(timelist)
timeInfo = time3(timelist)
print('timeInfo', timeInfo)
dpi = list(dictProtInfo)
print('Названия линий и их АЙДИ:', dpi)
for k in range(len(timeInfo)):
    print(list(dpi))
    for l in range(len(timeInfo[k])):
        ti = list(timeInfo[k][l].items())
        print('Уставки времени:', ti[0])
        print('Протлоки рассматриваемых защит:', next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0]))

        if len(ti[0][1]) == 2:
            cursorObj.execute(f"UPDATE ProtOCSetting SET tp_2g=({ti[0][1][0][0]}) WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
            cursorObj.execute(f"UPDATE ProtOCSetting SET tp_g=({ti[0][1][1][0]}) WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
        else:
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET tp_2g=({ti[0][1][1][0]}) WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET sw4='1' WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET tp_3g=({ti[0][1][2][0]}) WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
            cursorObj.execute(
                f"UPDATE ProtOCSetting SET tp_g=({ti[0][1][0][0]}) WHERE ProtLoc_ID IN ({next(dpi[x][2] for x in range(len(dpi)) if dpi[x][0] == ti[0][0])})")
input('Засейвить?')
con.commit()  # подтверждаем изменения в БД
con.close()
