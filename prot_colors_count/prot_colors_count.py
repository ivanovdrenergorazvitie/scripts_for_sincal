import sqlite3
import pandas as pd
import openpyxl
def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

#   ---- Формирование списка groupID
# groupID0 = cursorObj.execute(
#     "SELECT Group_ID, Name FROM NetworkGroup WHERE Name NOT LIKE 'Base%Area'").fetchall()

groupID0 = cursorObj.execute(
    "SELECT Group_ID, Name FROM NetworkGroup").fetchall()
groupID = name_changer(groupID0)
df = pd.DataFrame()
df1 = pd.DataFrame()

#   ---- Попробуем сохранить подстанции
PSName0 = cursorObj.execute("SELECT Name FROM Node WHERE Name LIKE '%ПС%'").fetchall()
PSName0 = name_changer(PSName0)
PSName1 = []
for ps1 in range(len(PSName0)):
    PSName2 = PSName0[ps1].replace(' СШ', '')
    PSName3 = PSName2.replace(' 1', '')
    PSName4 = PSName3.replace(' 2', '')
    PSName1 += [PSName4.replace('ПС ', '')]
PSName = set(PSName1)
PSName = list(PSName)
PSName = sorted(PSName)

redps = 0
greenps = 0
blueps = 0

dataframeopredelitel = int(input('1 - Таблица по фидерам, 2 - Таблица по подстанциям'))



fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('Ввведите вариант схемы (' + str(fullvariantID)+ '): '))
variantID = []
variantID1 = userVariantID
nodeID = []
terminalID = []
gterminalID = []
nodeID0 = []
elementID = []
print(variantID0)
if userVariantID != 1:
    while variantID1 != 0:
        variantID += [variantID1]
        print(variantID)
        parentVariantID = cursorObj.execute(
            "SELECT ParentVariant_ID FROM Variant WHERE Variant_ID IN ({0})".format(
                str(variantID1))).fetchall()
        parentVariantID = name_changer(parentVariantID)
        parentVariantID = parentVariantID[0]
        variantID1 = parentVariantID
else:
    variantID = [1]
input('Продолжить')


def varID(var, flag):

    global nodeID, terminalID, gterminalID, elementID

    if flag == 1:
        terminalID0 = cursorObj.execute(
            "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND VARIANT_ID IN ({1})".format(
                str(elementID[osn2]), str(var))).fetchall()
        terminalID0 = name_changer(terminalID0)
        terminalID = list(set(terminalID).union(set(terminalID0)))

    elif flag == 2:
        nodeID0 = cursorObj.execute(
            "SELECT Node_ID FROM Node WHERE Group_ID IN ({0}) AND VARIANT_ID IN ({1})".format(
                str(groupID[osn1]), str(var))).fetchall()
        nodeID1 = name_changer(nodeID0)
        nodeID = list(set(nodeID).union(set(nodeID1)))

    elif flag == 3:
        gterminalID0 = cursorObj.execute(
            "SELECT GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                str(terminalID[osn3]))).fetchall()
        gterminalID0 = name_changer(gterminalID0)
        gterminalID = list(set(gterminalID).union(gterminalID0))
    elif flag == 4:
        elementID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Group_ID IN ({0}) AND VARIANT_ID IN ({1})".format(
                str(groupID[osn1]), str(var))).fetchall()
        elementID1 = name_changer(elementID0)
        elementID = list(set(elementID).union(set(elementID1)))

#   ---- Формирование списка elementID и nodeID
PSNameF = []
PSNameF0 = []
for osn1 in range(len(groupID)):
    red = 0
    green = 0
    blue = 0
    print()
    print(osn1, groupID0[osn1][1])
    elementID.clear()
    PSNameF0.clear()
    feederName = groupID0[osn1][1]
    feederName = feederName.upper()
    if osn1 != 0:
        ps1 = 0
        # for ps2 in range(len(feederName)):
        #     if feederName[ps2] == 'ф':
        #         ifps1 = ps2
        #     elif feederName[ps2] == '.':                  Стирать пока не надо
        #         ifps2 = ps2
        # if ifps2 - ifps1 == 1:
        #     feederName = feederName[:ifps1 - 1]
        # PSNameF0 += [feederName.replace('ПС ', '')]
        PSNameF0 += [feederName]
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
    for i in variantID:
        varID(i, 2)
    for i in variantID:
        varID(i, 4)
    print('elementID', elementID)
    #   ---- Формирование списка terminalID
    for osn2 in range(len(elementID)):
        terminalID.clear()
        for i in variantID:
            # varID(i, 1)
            terminal0 = cursorObj.execute(
                "SELECT Terminal_ID, Element_ID FROM Terminal WHERE Element_ID IN ({0}) AND VARIANT_ID IN ({1})".format(
                    str(elementID[osn2]), str(i))).fetchall()
            if terminal0 == []:
                continue
        terminalID0 = []
        termElID = []
        if terminal0 == []:
            continue

        for term1 in range(len(terminal0)):
            terminalID0.append(terminal0[term1][0])
            termElID.append(terminal0[term1][1])
        terminalID = list(set(terminalID).union(set(terminalID0)))

    #   ---- Формирование списка  gterminalID
        for osn3 in range(len(terminalID)):
            # indicator = 0
            # elGroupID = cursorObj.execute(
            #     "SELECT Group_ID FROM Element WHERE Element_ID IN ({0})".format(str(termElID[osn3]))).fetchone()
            # if elGroupID[0] != groupID[osn1]:
            #     indicator = 1
            # if indicator == 1:
            #     continue
            gterminalID.clear()
            for i in variantID:
                varID(i, 3)
            # chetosn5 = []
            # nechetosn5 = []
            for osn4 in range(len(gterminalID)):
                gaterminalID0 = cursorObj.execute(
                    "SELECT * FROM GraphicAddTerminal WHERE GraphicTerminal_ID IN ({0}) AND SymType IN ({1}) AND GraphicType_ID IN ({2})".format(
                        str(gterminalID[osn4]), '1', '1')).fetchall()
                #   ---- Фильтр для защиты

                for osn5 in range(len(gaterminalID0)):
                    osn6 = 0
                    indicatorOsn6 = 0
                    while osn6 < len(variantID):
                        if gaterminalID0[osn5][19] != variantID[osn6]:
                            if osn6 == len(variantID) - 1:
                                indicatorOsn6 = 1
                            osn6 += 1
                            continue
                        elif gaterminalID0 == []:
                            break
                        elif gaterminalID0[osn5][5] == 0:
                            break
                        osn6 = len(variantID)
                    if indicatorOsn6 == 1:
                        continue
                    gaterminalID = gaterminalID0[osn5][5]

                    #   ---- Переменные на две итерации
                    #                 if osn4 % 2 == 0:
                    #                     chetosn5 = gterminalID
                    #                     if chetosn5 == nechetosn5:
                    #                         gatcolor = 0
                    #                     else:
                    #                         gatcolor = gaterminalID
                    #
                    #                 elif osn4 % 2 == 1:
                    #                     nechetosn5 = gterminalID
                    #                     if nechetosn5 == chetosn5:
                    #                         gatcolor = 0
                    #                     else:
                    #                         gatcolor = gaterminalID

                    elementname = cursorObj.execute(
                        "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(str(elementID[osn2]))).fetchone()

                    gatcolor = gaterminalID

                    #   ---- Выбор максимального варианта для gaterminal
                    if gatcolor == 0:
                        continue
                    elif gatcolor == 65280:
                        green += 1
                        print('green', gterminalID, elementname[0])
                    elif gatcolor == 255:
                        red += 1
                        print('red', gterminalID, elementname[0])
                    elif gatcolor == 16763904:
                        blue += 1
                        print('blue', gterminalID, elementname[0])

    list_of_colors = [green, red, blue]
    df[groupID0[osn1][1]] = list_of_colors

    print('green; ' + str(green))
    print('blue; ' + str(blue))
    print('red; ' + str(red))

    PSNameF += [[]]
    if PSNameF0 == []:
        PSNameF[0] += ['Ненайденный фидер']
        PSNameF[-1] += [list_of_colors]
    #     continue
    else:
        PSNameF[-1] += [PSNameF0[0]]
        PSNameF[-1] += [list_of_colors]



PSName.reverse()
print(PSNameF)
print(PSName)

for ps2 in range(len(PSName)):
    for ps3 in range(len(PSNameF)):
        if PSNameF[ps3][0].find(PSName[ps2] + ' ') != -1:
            greenps += PSNameF[ps3][1][0]
            redps += PSNameF[ps3][1][1]
            blueps += PSNameF[ps3][1][2]
            list_of_colors_ps = [greenps, redps, blueps]
            df1[PSName[ps2]] = list_of_colors_ps
    greenps = 0
    redps = 0
    blueps = 0



if dataframeopredelitel == 1:
    df.to_excel('По фидерам.xlsx')
    print(df)
if dataframeopredelitel == 2:
    df1.to_excel('По ТП.xlsx')
    print(df1)
#   ЗЕЛЕНЫЙ - 0, КРАСНЫЙ - 1, СИНИЙ - 2