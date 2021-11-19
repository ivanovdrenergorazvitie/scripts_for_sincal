import sqlite3


# !Исправления с 4.11: добавил flagtofixTerminal и flagtofixElement
# (можно по поиску глянуть, где они находятся и какую функцию выполняют).
# На данный момент они пропускают проблемные (у которых нет графики, насколько я понял) элементы и терминалы.
# Я не знаю как, но это работает.

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('Ввведите вариант схемы (' + str(fullvariantID) + '): '))
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
print('Парядок вариантов: ' + str(variantID) + ';')

AreaID0 = cursorObj.execute("SELECT GraphicArea_ID FROM GraphicAreaTile").fetchall()
AreaID0 = name_changer(AreaID0)
AreaID = AreaID0[1:]
ParentAreaID = AreaID0[:1]

print('Список видов: ' + str(AreaID) + '; Вид исходника: ' + str(ParentAreaID))

Max_GPointID = cursorObj.execute("SELECT MAX(GraphicPoint_ID) FROM GraphicBucklePoint").fetchone()[0]
osn2tr = 0
T_ID = 0
L_ID = 0
# TransID = 1
gnodeerror = []
for osn1 in range(len(AreaID)):
    # if AreaID[osn1] != 111:
    #     continue
    print('\n\n\n\nПЕРЕХОД К ВИДУ ' + str(AreaID[osn1]))

    ElementID = cursorObj.execute(
        "SELECT Element_ID FROM GraphicElement WHERE GraphicArea_ID IN ({0})".format(
            str(AreaID[osn1]))).fetchall()
    ElementID = name_changer(ElementID)

    NodeID = cursorObj.execute(
        "SELECT Node_ID FROM GraphicNode WHERE GraphicArea_ID IN ({0})".format(
            str(AreaID[osn1]))).fetchall()
    NodeID = name_changer(NodeID)

    TerminalID = cursorObj.execute(
        "SELECT Terminal_ID FROM GraphicTerminal WHERE GraphicArea_ID IN ({0})".format(
            str(AreaID[osn1]))).fetchall()
    TerminalID = name_changer(TerminalID)
    print(TerminalID)

    cursorObj.execute("UPDATE GraphicAddTerminal SET SymSize='50' WHERE SymType='3' OR SymType='4'")

    for osn2 in range(len(ElementID)):
        GELoadID = [0, 0]
        GETransID = [0, 0]
        ElementID1 = []
        kx = 0
        ky = 0
        flagtofixElement = 0
        LoadName = 0
        TransName = 1
        for var1 in variantID:
            GElementID = cursorObj.execute(
                "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE Element_ID IN ({0}) AND Variant_ID "
                "IN ({1}) AND GraphicArea_ID='1'".format(
                    str(ElementID[osn2]), str(var1))).fetchall()
            if GElementID != []:
                break
            if GElementID == [] and var1 == 1:
                flagtofixElement = 1
                print('ПУСТОЙ ЭЛЕМЕНТ ГРАФИКИ:', ElementID[osn2])
        if flagtofixElement == 1:
            continue
        print(GElementID)
        ElementID1 = GElementID[0]

        TransID = cursorObj.execute(
            "SELECT Element_ID, Name FROM Element WHERE Element_ID IN ({0}) "
            "AND Type='TwoWindingTransformer'".format(
                str(ElementID[osn2]))).fetchone()
        if TransID != None:
            TransName = TransID[1].split(' ')[0]
            print('NAME', TransName)
            for var1 in variantID:
                LoadID = cursorObj.execute(
                    "SELECT Element_ID, Name FROM Element WHERE Name IN ({0}) OR Name IN ({1}) AND "
                    "Variant_ID IN ({2}) AND Flag_Variant='1'".format(
                        "'" + str(TransName + ' Н') + "'", "'" + str(TransName + ' H') + "'", str(var1))).fetchone()
                if LoadID != []:
                    break
            print('VARIANT', TransID, LoadID)
            if LoadID != None:
                try:
                    if str(TransID[1])[:TransID[1].index(' ')] == str(LoadID[1])[:LoadID[1].index(' ')]:
                        usl1 = 1
                        print('TRY', TransID, LoadID)
                    else:
                        usl1 = 0
                        print('ELSE', TransID, LoadID)
                except:
                    usl1 = 0
                    print('EXPECT', TransID, LoadID)
                if usl1 == 1:
                    GETransID = cursorObj.execute(
                        "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                        "AND Element_ID IN ({0})".format(str(ElementID[osn2]))).fetchone()
                    GELoadID = cursorObj.execute(
                        "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                        "AND Element_ID IN ({0})".format(str(LoadID[0]))).fetchone()
                    # Вертикально
                    if (GELoadID[1] - GETransID[1]) ** 2 > (GELoadID[0] - GETransID[0]) ** 2:
                        # Вниз
                        if GELoadID[1] < GETransID[1]:
                            kx = 0
                            ky = -0.007
                        # Вверх
                        else:
                            kx = 0
                            ky = 0.007
                    # Горизонатльно
                    elif (GELoadID[1] - GETransID[1]) ** 2 < (GELoadID[0] - GETransID[0]) ** 2:
                        # Влево
                        if GELoadID[0] > GETransID[0]:
                            kx = -0.007
                            ky = 0
                        # Вправо
                        else:
                            kx = 0.007
                            ky = 0

        LoadID = cursorObj.execute(
            "SELECT Element_ID, Name FROM Element WHERE Element_ID IN ({0}) "
            "AND Type='Load'".format(
                str(ElementID[osn2]))).fetchone()
        if LoadID != None:

            LoadName = LoadID[1].split(' ')[0]
            for var1 in variantID:
                TransID = cursorObj.execute(
                    "SELECT Element_ID, Name FROM Element WHERE Name IN ({0}) OR Name IN ({1}) AND "
                    "Variant_ID IN ({2}) AND Flag_Variant='1'".format(
                        "'" + str(LoadName + ' Т') + "'", "'" + str(LoadName + ' T') + "'", str(var1))).fetchone()
                if TransID != []:
                    break
            if TransID != None:
                try:
                    if str(TransID[1])[:TransID[1].index(' ')] == str(LoadID[1])[:LoadID[1].index(' ')]:
                        usl2 = 1
                    else:
                        usl2 = 0
                except:
                    usl2 = 0
                if usl2 == 1:
                    GELoadID = cursorObj.execute(
                        "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                        "AND Element_ID IN ({0})".format(str(ElementID[osn2]))).fetchone()
                    GETransID = cursorObj.execute(
                        "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                        "AND Element_ID IN ({0})".format(str(TransID[0]))).fetchone()
                    # Вертикально
                    print(((GELoadID[1] - GETransID[1]) ** 2), ((GELoadID[0] - GETransID[0]) ** 2), ElementID[osn2])
                    if (GELoadID[1] - GETransID[1]) ** 2 > (GELoadID[0] - GETransID[0]) ** 2:
                        # Вниз
                        if GELoadID[1] < GETransID[1]:
                            kx = 0
                            ky = -0.0125
                        # Вверх
                        else:
                            kx = 0
                            ky = 0.0125
                    # Горизонатльно
                    elif (GELoadID[1] - GETransID[1]) ** 2 < (GELoadID[0] - GETransID[0]) ** 2:
                        # Влево
                        if GELoadID[0] > GETransID[0]:
                            kx = -0.0125
                            ky = 0
                        # Вправо
                        else:
                            kx = 0.0125
                            ky = 0

        try:
            ElementID1 = ElementID1[0]
        except:
            gnodeerror += ['Элемент', GElementID, AreaID[osn1]]
            continue

        cursorObj.execute(
            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE Element_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GElementID[0][0] - kx), str(ElementID[osn2]), str(AreaID[osn1])))
        cursorObj.execute(
            "UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GElementID[0][1] + ky), str(ElementID[osn2]), str(AreaID[osn1])))
        cursorObj.execute(
            "UPDATE GraphicElement SET SymbolSize=({0}) WHERE Element_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(100), str(ElementID[osn2]), str(AreaID[osn1])))

    for osn3 in range(len(NodeID)):
        kx = 0
        ky = 0
        GELoadID = [0, 0]
        GETransID = [0, 0]
        for var2 in variantID:
            GNodeID = cursorObj.execute(
                "SELECT NodeStartX, NodeStartY, NodeEndX, NodeEndY, SymType FROM GraphicNode WHERE Node_ID IN ({0}) AND Variant_ID "
                "IN ({1}) AND GraphicArea_ID='1'".format(
                    str(NodeID[osn3]), str(var2))).fetchall()
            if GNodeID != []:
                break
        for var2_0 in variantID:
            NElementID = cursorObj.execute(
                "SELECT Element_ID FROM Terminal WHERE Node_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(NodeID[osn3]), str(var2_0))).fetchall()
            NElementID = name_changer(NElementID)
            if NElementID != []:
                break
        usl3 = 0
        if len(NElementID) == 2:
            for var2_1 in variantID:
                Type1 = cursorObj.execute(
                    "SELECT Type FROM Element WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                        str(NElementID[0]), str(var2_1))).fetchall()
                if Type1 != []:
                    break
            Type1 = Type1[0][0]
            for var2_2 in variantID:
                Type2 = cursorObj.execute(
                    "SELECT Type FROM Element WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                        str(NElementID[1]), str(var2_2))).fetchall()
                if Type2 != []:
                    break
            Type2 = Type2[0][0]
            if Type1 == 'TwoWindingTransformer' and Type2 == 'Load':
                T_ID = NElementID[0]
                L_ID = NElementID[1]
                usl3 = 1
            if Type2 == 'TwoWindingTransformer' and Type1 == 'Load':
                T_ID = NElementID[1]
                L_ID = NElementID[0]
                usl3 = 1
            if usl3 == 1:
                GELoadID = cursorObj.execute(
                    "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                    "AND Element_ID IN ({0})".format(str(L_ID))).fetchone()
                GETransID = cursorObj.execute(
                    "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicArea_ID = '1' "
                    "AND Element_ID IN ({0})".format(str(T_ID))).fetchone()

                if (GELoadID[1] - GETransID[1]) ** 2 > (GELoadID[0] - GETransID[0]) ** 2:
                    # Вниз
                    if GELoadID[1] < GETransID[1]:
                        kx = 0
                        ky = -0.0125
                    # Вверх
                    elif GELoadID[1] > GETransID[1]:
                        kx = 0
                        ky = 0.0125
                # Горизонатльно
                elif (GELoadID[1] - GETransID[1]) ** 2 < (GELoadID[0] - GETransID[0]) ** 2:
                    # Влево
                    if GELoadID[0] > GETransID[0]:
                        kx = -0.0125
                        ky = 0
                    # Вправо
                    elif GELoadID[0] < GETransID[0]:
                        kx = 0.0125
                        ky = 0

        GNodeStartX = GNodeID[0][0] + kx
        GNodeStartY = GNodeID[0][1] + ky
        GNodeEndX = GNodeID[0][2] + kx
        GNodeEndY = GNodeID[0][3] + ky

        # if NodeID[osn3] == 3471:
        # print('КОЭФФИЦИЕНТЫ', kx, ky, GNodeStartX, GNodeStartY, GNodeEndX, GNodeEndY, GETransID, GELoadID, T_ID, L_ID, )

        try:
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeStartX=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID[0][0] - kx), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeStartY=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID[0][1] + ky), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeEndX=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID[0][2] - kx), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeEndY=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID[0][3] + ky), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET SymType=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID[0][4]), str(NodeID[osn3]), str(AreaID[osn1])))
        except:
            gnodeerror += ['Узел', GNodeID, NodeID[osn3], AreaID[osn1]]
    for osn4 in range(len(TerminalID)):
        flagtofixTerminal = 0
        for var3 in variantID:
            GTerminalID = cursorObj.execute(
                "SELECT PosX, PosY, GraphicTerminal_ID, Variant_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND Variant_ID "
                "IN ({1}) AND GraphicArea_ID='1'".format(
                    str(TerminalID[osn4]), str(var3))).fetchall()
            if GTerminalID != []:
                break
            if var3 == 1 and GTerminalID == []:
                flagtofixTerminal = 1
                print('СКРИНИМ ПОПУЩЕЙ, ВОТ ОНИ:', str(TerminalID[osn4]))
        if flagtofixTerminal == 1:
            continue
        for var3 in variantID:
            TerminalID1 = cursorObj.execute(
                "SELECT Terminal_ID, Variant_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                    str(TerminalID[osn4]))).fetchall()

            if TerminalID1 != []:
                break
            if var3 == 1 and TerminalID1 == []:
                for var3_1 in variantID:
                    TerminalID1 = cursorObj.execute(
                        "SELECT Terminal_ID, Variant_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                            TerminalID[osn4])).fetchall()
                    if TerminalID1 != []:
                        break
        try:
            TerminalID1 = TerminalID1[0]
        except:
            gnodeerror += ['Терминал', TerminalID, AreaID[osn1]]
            continue

        for var4 in variantID:
            PointID = cursorObj.execute(
                "SELECT GraphicPoint_ID, NoPoint, PosX, PosY, Flag_Variant FROM GraphicBucklePoint WHERE GraphicTerminal_ID IN ({0}) "
                "AND Variant_ID IN ({1})".format(
                    str(GTerminalID[0][2]), str(var4))).fetchall()
            if PointID != []:
                break

        cursorObj.execute(
            "UPDATE GraphicTerminal SET PosX=({0}) WHERE Terminal_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GTerminalID[0][0]), str(TerminalID[osn4]), str(AreaID[osn1])))
        cursorObj.execute(
            "UPDATE GraphicTerminal SET PosY=({0}) WHERE Terminal_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GTerminalID[0][1]), str(TerminalID[osn4]), str(AreaID[osn1])))
        GTerminalVida = cursorObj.execute(
            "SELECT GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND GraphicArea_ID IN ({1})".format(
                str(TerminalID[osn4]), str(AreaID[osn1]))).fetchone()[0]

        if PointID == []:
            continue
        for osn5 in PointID:
            Max_GPointID += 1

            cursorObj.execute("INSERT INTO GraphicBucklePoint VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(
                str(Max_GPointID), str(GTerminalVida), str(osn5[1]), str(osn5[2]), str(osn5[3]), str(userVariantID),
                str(osn5[4])))
# input('SAVE')
print('\n\n\n', gnodeerror, '\n', len(gnodeerror))
con.commit()
con.close()
