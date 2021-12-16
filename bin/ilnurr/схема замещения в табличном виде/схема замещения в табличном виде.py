import sqlite3
import pandas as pd
import xlsxwriter
def vipryamitel(l):
    h = []
    for i in range(len(l)):
        if type(l[i]) == type(l):
            print('IF', l[i])
            h += vipryamitel(l[i])
        else:
            print('ELSE', l[i])
            h += [l[i]]
    return h
def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

def inputvar():
    fullvariantID = cursorObj.execute(
        "SELECT Variant_ID FROM Variant").fetchall()
    variantID0 = name_changer(fullvariantID)

    userVariantID = int(input('Ввведите вариант схемы ' + str(variantID0) + ': '))
    variantID = []
    variantID1 = userVariantID

    if userVariantID != 1:
        while variantID1 != 0:
            variantID += [variantID1]
            # print(variantID)
            parentVariantID = cursorObj.execute(
                "SELECT ParentVariant_ID FROM Variant WHERE Variant_ID IN ({0})".format(
                    str(variantID1))).fetchall()
            parentVariantID = name_changer(parentVariantID)
            parentVariantID = parentVariantID[0]
            variantID1 = parentVariantID
    else:
        variantID = [1]
    return variantID
def h(zoneInfo, groupInfo):
    for var in variantID:
        res = []
        el = []
        for ps in range(len(zoneInfo)):
            res[ps * 2] = zoneInfo[ps][1]
            res[ps * 2 + 1] = []
        for ps in range(len(zoneInfo)):
            el = cursorObj.execute(f"SELECT Element_ID, Variant_ID, Group_ID, Zone_ID FROM Element WHERE Zone_ID IN ({zoneInfo[ps][0]}) AND (Flag_Variant='0' OR Flag_Variant='1') AND Variant_ID IN ({var})").fetchall()
            # for ps1 in range(len(zoneInfo)):
            #     if el[ps][0] ==

def group_to_zone():
    n_group = cursorObj.execute("SELECT Name, Group_ID FROM NetworkGroup").fetchall()
    data = cursorObj.execute("SELECT Group_ID, Zone_ID FROM Element").fetchall()
    print(n_group, '\n', data)

def enter_db():
    path_db = 'database.db'
    con = sqlite3.connect(path_db)
    cursorObj = con.cursor()
    return cursorObj
def podstancii(zoneInfo, groupInfo):
    PSInfo = []
    for ps in range(len(zoneInfo)):
        groupID = []
        for var in variantID:
            groupID0 = name_changer(cursorObj.execute(f"SELECT Group_ID FROM Element WHERE Zone_ID IN ({zoneInfo[ps][0]}) AND (Flag_Variant='0' OR Flag_Variant='1') AND Variant_ID IN ({var})").fetchall())
            if groupID0 != []:
                groupID = sorted(list(set(groupID).union(set(groupID0))))

        PSInfo += [[list(zoneInfo[ps]), groupID]]
    print(PSInfo)
    for ps in range(len(PSInfo)):
        for ps1 in range(len(PSInfo[ps])):
            scan = next([PSInfo[x][y], x] for x in range(len(PSInfo)) for y in range(len(PSInfo[x])) if PSInfo[x][y] != 1 and PSInfo[x][y] == PSInfo[ps][ps1])
            if PSInfo[ps][ps1] == scan[0]:


    # for i1 in range(len(elGroupID)):
    #     elGroupID[i1] = list(elGroupID[i1])
    #     elGroupID[i1][1] = next(groupInfo[x][1].split('-')[0] for x in range(len(groupInfo)) if groupInfo[x][0] == elGroupID[i1][1])

    # ouf = open('вывод переменной.txt', 'w')
    # ouf.write(str(elementID))
    # ouf.close()

    input('ds')
def element_table(eltype):
    zoneInfo = cursorObj.execute(f"SELECT Zone_ID, Name FROM NetworkZone WHERE Flag_Variant!='-2'").fetchall()
    groupInfo = cursorObj.execute(f"SELECT Group_ID, Name FROM NetworkGroup WHERE Flag_Variant!='-2'").fetchall()
    # print(str(zoneInfo) + '\n' + str(groupInfo))
    podstancii(zoneInfo, groupInfo)
    elementID = []
    table_list = []
    nodeID = []
    groupList = []
    zoneList = []
    for var in variantID:
        elementID0 = cursorObj.execute(
            f"SELECT Element_ID, Name, Zone_ID, Group_ID FROM Element "
            f"WHERE Variant_ID IN ({var}) AND Type=('{eltype}') AND (Flag_Variant='0' OR Flag_Variant='1')").fetchall()
        elementID = sorted(list(set(elementID).union(set(elementID0))))


    for i in range(len(elementID)):
        try:
            zoneList += [[next(zoneInfo[x][1] for x in range(len(zoneInfo)) if elementID[i][3] == zoneInfo[x][0])]]
        except:
            zoneList += [['Подстанция не определена']]
        groupList += [[next(groupInfo[x][1] for x in range(len(groupInfo)) if elementID[i][3] == groupInfo[x][0])]]

        for var in variantID:
            nodeID = name_changer(cursorObj.execute(f"SELECT Node_ID FROM Terminal WHERE Element_ID "
                                                    f"IN ({elementID[i][0]}) AND Variant_ID IN ({var})").fetchall())
            if nodeID != []:
                break
        nodeName = []
        for node in nodeID:
            for var in variantID:
                nodeName0 = name_changer(cursorObj.execute(f"SELECT Name FROM Node WHERE Node_ID "
                                                           f"IN ({node}) AND Variant_ID IN ({var})").fetchall())
                if nodeName0 != []:
                    nodeName += nodeName0
                    break


        if eltype == 'Line':
            r = cursorObj.execute(
                "SELECT r FROM Line WHERE Element_ID IN ({0})".format(str(elementID[i][0]))).fetchall()
            r = name_changer(r)
            r = r[0]
            l = cursorObj.execute(
                "SELECT l FROM Line WHERE Element_ID IN ({0})".format(str(elementID[i][0]))).fetchall()
            l = name_changer(l)
            l = l[0]
            if round(r * l, 5) == 0.0001 or round(r * l, 5) == 0:
                elementID[i] = []
                continue
            x = cursorObj.execute(
                "SELECT x FROM Line WHERE Element_ID IN ({0})".format(str(elementID[i][0]))).fetchall()
            x = name_changer(x)
            x = x[0]
            formula = 'z=' + str(round(r * l, 5)) + '+j' + str(round(x * l, 5))
        elif eltype == 'TwoWindingTransformer':
            uk = cursorObj.execute(
                "SELECT uk FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
                str(elementID[i][0]))).fetchall()
            uk = name_changer(uk)
            uk = uk[0]

            Un1 = cursorObj.execute("SELECT Un1 FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
                str(elementID[i][0]))).fetchall()
            Un1 = name_changer(Un1)
            Un1 = Un1[0]

            Sn = cursorObj.execute("SELECT Sn FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
                str(elementID[i][0]))).fetchall()
            Sn = name_changer(Sn)
            Sn = Sn[0]
            if Sn == 0:
                continue
            formula = ('z=' + str(round((uk * Un1 * Un1 / (Sn * 100.0)) / 33, 5)) + ' + j' + str(round(uk * Un1 * Un1 / (Sn * 100.0), 5)))
        elif eltype == 'Infeeder':
            ff = 1
            Xmax = cursorObj.execute(
                "SELECT Xmax FROM Infeeder WHERE Element_ID IN ({0})".format(str(elementID[i][0]))).fetchall()
            Xmax = name_changer(Xmax)
            Xmax = Xmax[0]

            Xmin = cursorObj.execute(
                "SELECT Xmin FROM Infeeder WHERE Element_ID IN ({0})".format(str(elementID[i][0]))).fetchall()
            Xmin = name_changer(Xmin)
            Xmin = Xmin[0]
            if Xmin == 0:
                ff = 0
                formula = 'Деление на ноль'
            if ff == 1:
                formula = str('z=' + str(Xmax) + '/' + str(Xmin) + '=' + str(round(Xmax / Xmin, 5)))
        elementID[i] = list(elementID[i])
        elementID[i] += nodeName
        elementID[i] += [formula]
        del elementID[i][0]
        del elementID[i][1]
        del elementID[i][1]




    if eltype == 'Line':
        names = [['Название', 'Узел 1', 'Узел 2', 'Сопротивление']]
    else:
        names = [['Название', 'Узел', 'Сопротивление']]


    names += elementID

    jj = 0
    while jj < len(names):
        if names[jj] == []:
            del names[jj]
        else:
            jj += 1




    with xlsxwriter.Workbook(f'{eltype}.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(names):
            worksheet.write_row(row_num, 0, data)

cursorObj = enter_db()
variantID = inputvar()

itype = input('1 - Линии, 2 - Трансформаторы, 3 - Источники: ')
if itype == '1':
    eltype = 'Line'
elif itype == '2':
    eltype = 'TwoWindingTransformer'
elif itype == '3':
    eltype = 'Infeeder'
else:
    print('Неверное значение')
    exit()


element_table(eltype)




