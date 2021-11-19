import sqlite3
import pandas as pd
import math

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a
def name_chanfer_dlya_pointov(b):
    a = []
    for i in range(len(b)):
        a += [b[i]]
        print(b[i])
    return a
path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('Ввведите вариант схемы (' + str(fullvariantID)+ '): '))
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
print('Список видов: ' + str(AreaID) +'; Вид исходника: ' + str(ParentAreaID))

Max_GPointID = cursorObj.execute("SELECT MAX(GraphicPoint_ID) FROM GraphicBucklePoint").fetchone()[0]

gnodeerror = []
for osn1 in range(len(AreaID)):
    print('\n\n\n\nПЕРЕХОД К ВИДУ ' + str(AreaID[osn1]))
    # if AreaID[osn1] == 15:
    #     input('ds')
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

    for osn2 in range(len(ElementID)):
        NameEl = cursorObj.execute("SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
            str(ElementID[osn2]))).fetchone()[0]
        ElementID1 = []
        for var1 in variantID:
            ElementID1 = cursorObj.execute(
                "SELECT Element_ID, Variant_ID FROM Element WHERE Element_ID NOT LIKE ({0}) AND Name IN ({1}) AND Variant_ID IN ({2})".format(
                    str(ElementID[osn2]), str("'" + NameEl + "'"), str(var1))).fetchall()
            if ElementID1 != []:
                break
            if var1 == 1 and ElementID1 == []:
                for var1_1 in variantID:
                    ElementID1 = cursorObj.execute(
                        "SELECT Element_ID, Variant_ID FROM Element WHERE Name IN ({0}) AND Variant_ID IN ({1})".format(
                            str("'" + NameEl + "'"), str(var1))).fetchall()
                    if ElementID1 != []:
                        break

        try:
            ElementID1 = ElementID1[0]
        except:
            gnodeerror += ['Элемент', ElementID1, NameEl, AreaID[osn1]]
            continue

        GElementID1 = cursorObj.execute(
            "SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                str(ElementID1[0]), str(ElementID1[1]))).fetchone()

        cursorObj.execute(
            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE Element_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GElementID1[0]), str(ElementID[osn2]), str(AreaID[osn1])))
        cursorObj.execute(
            "UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(GElementID1[1]), str(ElementID[osn2]), str(AreaID[osn1])))


    for osn3 in range(len(NodeID)):
        NameNd = cursorObj.execute("SELECT Node_ID FROM GraphicNode WHERE GraphicArea_ID IN ({0})".format(
            str(AreaID[osn1]))).fetchone()[0]
        NodeID1 = []
        for var2 in variantID:
            NodeID1 = cursorObj.execute(
                "SELECT NodeStartX, NodeStartY, NodeEndX, NodeEndY FROM GraphicNode WHERE Node_ID IN ({0})"
                " AND Variant_ID IN ({1} AND GraphicArea_ID IN ({2}))".format(
                    str(NameNd), str(var2), str('1'))).fetchall()
            if NodeID1 != []:
                break
            # if var2 == 1 and NodeID1 == []:
            #     for var2_1 in variantID:
            #         NodeID1 = cursorObj.execute(
            #             "SELECT Node_ID, Variant_ID FROM Node WHERE Name IN ({0}) AND Variant_ID IN ({1})".format(
            #                 str("'" + NameNd + "'"), str(var2_1))).fetchall()
            #         if NodeID1 != []:
            #             break
        # try:
        #     NodeID1 = NodeID1[0]
        # except:
        #     print(NameNd, var2)
        #     gnodeerror += ['Узел1', NodeID1, AreaID[osn1]]
        #
        #
        # GNodeID1 = cursorObj.execute(
        #     "SELECT NodeStartX, NodeStartY, NodeEndX, NodeEndY FROM GraphicNode WHERE Node_ID IN ({0}) AND Variant_ID IN ({1})".format(
        #         str(NodeID1[0]), str(NodeID1[1]))).fetchone()
        GNodeID1 = NodeID1
        try:
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeStartX=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID1[0]), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeStartY=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID1[1]), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeEndX=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID1[2]), str(NodeID[osn3]), str(AreaID[osn1])))
            cursorObj.execute(
                "UPDATE GraphicNode SET NodeEndY=({0}) WHERE Node_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                    str(GNodeID1[3]), str(NodeID[osn3]), str(AreaID[osn1])))
        except:
            gnodeerror += ['Узел', NodeID1, NodeID[osn3], AreaID[osn1]]
    for osn4 in range(len(TerminalID)):
        GTerminalID = cursorObj.execute(
            "SELECT GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND GraphicArea_ID IN ({1})".format(
                str(TerminalID[osn4]), str(AreaID[osn1]))).fetchone()[0]
        TerminalID1 = []
        for var3 in variantID:
            TerminalID1 = cursorObj.execute(
                "SELECT Terminal_ID, Variant_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1}) AND GraphicTerminal_ID NOT LIKE ({2})".format(
                    str(TerminalID[osn4]),  str(var3), str(GTerminalID))).fetchall()

            if TerminalID1 != []:
                break
            if var3 == 1 and TerminalID1 == []:
                for var3_1 in variantID:
                    TerminalID1 = cursorObj.execute(
                        "SELECT Terminal_ID, Variant_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1})".format(
                            TerminalID[osn4], str(var3_1))).fetchall()
                    if TerminalID1 != []:
                        break
        try:
            TerminalID1 = TerminalID1[0]
        except:
            gnodeerror += ['Терминал', TerminalID, AreaID[osn1]]
            continue


        GTerminalID1 = cursorObj.execute(
            "SELECT PosX, PosY, GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1})".format(
                str(TerminalID1[0]), str(TerminalID1[1]))).fetchone()

        # print('ТЕРМИНАЛЫ1', GTerminalID, TerminalID1)

        PointID = cursorObj.execute(
            "SELECT GraphicPoint_ID, NoPoint, PosX, PosY FROM GraphicBucklePoint WHERE GraphicTerminal_ID IN ({0})".format(
                str(GTerminalID1[2]))).fetchall()
        print('ПОИНТ АЙДИ  ', PointID)

        cursorObj.execute(
            "UPDATE GraphicTerminal SET PosX=({0}) WHERE Terminal_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(round(int(GTerminalID1[0]), 8)), str(TerminalID[osn4]), str(AreaID[osn1])))
        cursorObj.execute(
            "UPDATE GraphicTerminal SET PosY=({0}) WHERE Terminal_ID IN ({1}) AND GraphicArea_ID IN ({2})".format(
                str(round(int(GTerminalID1[1]), 8)), str(TerminalID[osn4]), str(AreaID[osn1])))


        for osn5 in PointID:
            Max_GPointID += 1
            print(osn5)

            cursorObj.execute("INSERT INTO GraphicBucklePoint VALUES ({0}, {1}, {2}, {3}, {4}, {5}, 1)".format(
                str(Max_GPointID), str(GTerminalID1[2]), str(osn5[1]), str(osn5[2]), str(osn5[3]), str(userVariantID)))


print('\n\n\n', gnodeerror, '\n', len(gnodeerror))
con.commit()
con.close()