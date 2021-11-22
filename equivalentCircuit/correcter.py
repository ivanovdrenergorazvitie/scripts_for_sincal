"""
СКРИПТ ДЛЯ КОРРЕКТИРОВКИ СХЕМЫ ЗАМЕЩЕНИЯ.
Используется после создания схемы замещения.
"""
import sqlite3

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

def varID(var, flag):
    global elementID
    if flag == 1:
        elementID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Variant_ID IN ({0})".format(str(var))).fetchall()
        elementID0 = name_changer(elementID0)
        elementID = sorted(list(set(elementID).union(set(elementID0))))

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('Ввведите вариант схемы ' + str(variantID0) + ': '))
variantID = []
variantID1 = userVariantID

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

#   ---- ---- УВЕЛИЧЕНИЕ ВСЕЙ СХЕМЫ НА КОЭФФИЦИЕНТ
ksize = float(input('Коэффициент увеличения схемы (В процентах): '))/100

coord_gbpoint = cursorObj.execute("SELECT GraphicPoint_ID, PosX, PosY, Variant_ID FROM GraphicBucklePoint").fetchall()
for i in range(len(coord_gbpoint)):
    cursorObj.execute(
        "UPDATE GraphicBucklePoint SET PosX=({0}) WHERE GraphicPoint_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gbpoint[i][1] * ksize), str(coord_gbpoint[i][0]), str(coord_gbpoint[i][3])))
    cursorObj.execute(
        "UPDATE GraphicBucklePoint SET PosY=({0}) WHERE GraphicPoint_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gbpoint[i][2] * ksize), str(coord_gbpoint[i][0]), str(coord_gbpoint[i][3])))


coord_gelement = cursorObj.execute(
    "SELECT GraphicElement_ID, SymCenterX, SymCenterY, Variant_ID FROM GraphicElement").fetchall()
for i in range(len(coord_gelement)):
    cursorObj.execute(
        "UPDATE GraphicElement SET SymCenterX=({0}) WHERE GraphicElement_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gelement[i][1] * ksize), str(coord_gelement[i][0]), str(coord_gelement[i][3])))
    cursorObj.execute(
        "UPDATE GraphicElement SET SymCenterY=({0}) WHERE GraphicElement_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gelement[i][2] * ksize), str(coord_gelement[i][0]), str(coord_gelement[i][3])))

coord_gnode = cursorObj.execute(
    "SELECT GraphicNode_ID, NodeStartX, NodeStartY, NodeEndX, NodeEndY, Variant_ID FROM GraphicNode").fetchall()
for i in range(len(coord_gnode)):
    cursorObj.execute(
        "UPDATE GraphicNode SET NodeStartX=({0}) WHERE GraphicNode_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gnode[i][1] * ksize), str(coord_gnode[i][0]), str(coord_gnode[i][5])))
    cursorObj.execute(
        "UPDATE GraphicNode SET NodeStartY=({0}) WHERE GraphicNode_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gnode[i][2] * ksize), str(coord_gnode[i][0]), str(coord_gnode[i][5])))
    cursorObj.execute(
        "UPDATE GraphicNode SET NodeEndX=({0}) WHERE GraphicNode_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gnode[i][3] * ksize), str(coord_gnode[i][0]), str(coord_gnode[i][5])))
    cursorObj.execute(
        "UPDATE GraphicNode SET NodeEndY=({0}) WHERE GraphicNode_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gnode[i][4] * ksize), str(coord_gnode[i][0]), str(coord_gnode[i][5])))


coord_gterminal = cursorObj.execute(
    "SELECT GraphicTerminal_ID, PosX, PosY, Variant_ID FROM GraphicTerminal").fetchall()
for i in range(len(coord_gterminal)):
    cursorObj.execute(
        "UPDATE GraphicTerminal SET PosX=({0}) WHERE GraphicTerminal_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gterminal[i][1] * ksize), str(coord_gterminal[i][0]), str(coord_gterminal[i][3])))
    cursorObj.execute(
        "UPDATE GraphicTerminal SET PosY=({0}) WHERE GraphicTerminal_ID IN ({1}) AND Variant_ID IN ({2})".format(
            str(coord_gterminal[i][2] * ksize), str(coord_gterminal[i][0]), str(coord_gterminal[i][3])))



#   ---- ---- РАЗМЕР ТЕКСТА
cursorObj.execute("UPDATE GraphicText SET FontSize='5'")


#   ---- ---- ПОЗИЦИЯ ТЕКСТА
elementID = []
for i in variantID:
    varID(i, 1)
print(elementID)

for el1 in range(len(elementID)):
    # Определение направления
    for var in variantID:
        terminalID = cursorObj.execute(
            "SELECT TerminalNo, Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                str(elementID[el1]), str(var))).fetchall()
        if terminalID != []:
            break
    print('NO, TERMINAL_ID:', terminalID)

    if len(terminalID) > 1:

        for var in variantID:
            gterminalID1 = cursorObj.execute(
                "SELECT PosX, PosY, GraphicTerminal_ID FROM GraphicTerminal "
                "WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1}) AND GraphicArea_ID='1'".format(
                    str(terminalID[0][1]), str(var))).fetchall()[0]
            if gterminalID1 != []:
                gtx1 = gterminalID1[0]
                gty1 = gterminalID1[1]
                gterminalID1 = gterminalID1[2]
                break
        for var in variantID:
            gterminalID2 = cursorObj.execute(
                "SELECT PosX, PosY, GraphicTerminal_ID FROM GraphicTerminal "
                "WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1}) AND GraphicArea_ID='1'".format(
                    str(terminalID[1][1]), str(var))).fetchall()[0]
            if gterminalID2 != []:
                gtx2 = gterminalID2[0]
                gty2 = gterminalID2[1]
                gterminalID2 = gterminalID2[2]
                break
        print('GTERMINAL_ID NO1, NO2:', gterminalID1, gterminalID2)
        if gterminalID1 == [] and gterminalID2 == []:
            continue
        for var in variantID:
            bpointID1 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY, NoPoint FROM GraphicBucklePoint "
                "WHERE GraphicTerminal_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(gterminalID1), str(var))).fetchall()
            if bpointID1 != []:
                break
        for var in variantID:
            bpointID2 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY, NoPoint FROM GraphicBucklePoint "
                "WHERE GraphicTerminal_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(gterminalID2), str(var))).fetchall()
            if bpointID2 != []:
                break
        if bpointID1 == [] and bpointID2 == []:
            cursorObj.execute("UPDATE GraphicElement SET SymCenterX =({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (gtx1 + gtx2) / 2), str(elementID[el1])))
            cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (gty1 + gty2) / 2), str(elementID[el1])))
            # Вертикально
            if (gty1 - gty2) ** 2 > (gtx1 - gtx2) ** 2:
                kx = 0.0025
                ky = 0
            # Горизонтально
            elif (gty1 - gty2) ** 2 < (gtx1 - gtx2) ** 2:
                kx = 0
                ky = 0.0025
        elif bpointID1 == []:
            bpx2 = next(bpointID2[x] for x in range(len(bpointID2)) if bpointID2[x][3] == 1)[1]
            bpy2 = next(bpointID2[y] for y in range(len(bpointID2)) if bpointID2[y][3] == 1)[2]
            cursorObj.execute("UPDATE GraphicElement SET SymCenterX =({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (gtx1 + bpx2) / 2), str(elementID[el1])))

            # Вертикально
            if (bpx2 - gtx1) ** 2 < (bpy2 - gty1) ** 2:
                kx = 0.0025
                ky = 0
            # Горизонтально
            elif (bpx2 - gtx1) ** 2 > (bpy2 - gty1) ** 2:
                kx = 0
                ky = 0.0025

        elif bpointID2 == []:
            bpx1 = next(bpointID1[x] for x in range(len(bpointID1)) if bpointID1[x][3] == 1)[1]
            bpy1 = next(bpointID1[y] for y in range(len(bpointID1)) if bpointID1[y][3] == 1)[2]
            cursorObj.execute("UPDATE GraphicElement SET SymCenterX =({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (bpx1 + gtx2) / 2), str(elementID[el1])))
            cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (bpy1 + gty2) / 2), str(elementID[el1])))

            # Вертикально
            if (bpx1 - gtx2) ** 2 < (bpy1 - gty2) ** 2:
                kx = 0.0025
                ky = 0
            # Горизонтально
            elif (bpx1 - gtx2) ** 2 > (bpy1 - gty2) ** 2:
                kx = 0
                ky = 0.0025
        else:
            bpx1 = next(bpointID1[x] for x in range(len(bpointID1)) if bpointID1[x][3] == 1)[1]
            bpy1 = next(bpointID1[y] for y in range(len(bpointID1)) if bpointID1[y][3] == 1)[2]
            bpx2 = next(bpointID2[x] for x in range(len(bpointID2)) if bpointID2[x][3] == 1)[1]
            bpy2 = next(bpointID2[y] for y in range(len(bpointID2)) if bpointID2[y][3] == 1)[2]
            cursorObj.execute("UPDATE GraphicElement SET SymCenterX=({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (bpx1 + bpx2) / 2), str(elementID[el1])))
            cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                str(ksize * (bpy1 + bpy2) / 2), str(elementID[el1])))

            # Вертикально
            if (bpx1 - bpx2) ** 2 < (bpy1 - bpy2) ** 2:
                kx = 0.0025
                ky = 0
            # Горизонтально
            elif (bpx1 - bpx2) ** 2 > (bpy1 - bpy2) ** 2:
                kx = 0
                ky = 0.0025
        for var in variantID:
            gelementID = cursorObj.execute(
                "SELECT GraphicElement_ID FROM GraphicElement WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(elementID[el1]), str(var))).fetchone()
            if gelementID != None:
                gelementID = gelementID[0]
                break
        gtext = cursorObj.execute(
            "SELECT GraphicText_ID1 FROM GraphicElement WHERE GraphicElement_ID IN ({0})".format(
                str(gelementID))).fetchone()[0]
        cursorObj.execute("UPDATE GraphicText SET Pos1=({0}) WHERE GraphicText_ID IN ({1})".format(str(kx), str(gtext)))
        cursorObj.execute("UPDATE GraphicText SET Pos2=({0}) WHERE GraphicText_ID IN ({1})".format(str(ky), str(gtext)))
        print('BPOINT:', bpointID1, bpointID2)
nodeID = cursorObj.execute(
    "SELECT Node_ID FROM GraphicNode WHERE NodeStartX!=NodeEndX OR NodeStartY!=NodeEndY").fetchall()
nodeID = name_changer(nodeID)
print('BUSBARS: ', nodeID)

for i in range(len(nodeID)):
    nterminalID = cursorObj.execute(
        "SELECT TerminalNo, Terminal_ID FROM Terminal WHERE Node_ID IN ({0})".format(
            str(nodeID[i]))).fetchall()
    try:
        l = next('not error' for y in range(len(nterminalID)) if nterminalID[y][0] == 1)
        continue
    except:
        print(nterminalID, '- КОНЕЧНЫЙ БУСБАР')
    if nterminalID == []:
        cursorObj.execute("DELETE FROM GraphicNode WHERE Node_ID IN ({0})".format(str(nodeID[i])))
        continue

    gnodeID = cursorObj.execute(
        "SELECT GraphicNode_ID, NodeStartX, NodeStartY, NodeEndX, NodeEndY, GraphicText_ID1 "
        "FROM GraphicNode WHERE Node_ID IN ({0})".format(
            str(nodeID[i]))).fetchone()
    print(gnodeID)
    # Надпись справа
    if (gnodeID[1] - gnodeID[3]) ** 2 > (gnodeID[2] - gnodeID[4]) ** 2:
        if gnodeID[1] > gnodeID[3]:
            kx = 0.0025
            ky = 0
        elif gnodeID[1] < gnodeID[3]:
            kx = gnodeID[3] - gnodeID[1] + 0.0025
            ky = 0
    elif (gnodeID[1] - gnodeID[3]) ** 2 < (gnodeID[2] - gnodeID[4]) ** 2:
        if gnodeID[2] > gnodeID[4]:
            kx = 0
            ky = 0.0025
        if gnodeID[2] < gnodeID[4]:
            kx = 0
            ky = 0.0025 + gnodeID[4] - gnodeID[2]

    cursorObj.execute(
        "UPDATE GraphicText SET Pos1=({0}) WHERE GraphicText_ID IN ({1})".format(str(kx), str(gnodeID[5])))
    cursorObj.execute(
        "UPDATE GraphicText SET Pos2=({0}) WHERE GraphicText_ID IN ({1})".format(str(ky), str(gnodeID[5])))

    """
    ФИКС ПРЕДКОНЕЧНОШИННЫХ ЭЛЕМЕНТОВ
    """
    for i1 in range(len(nterminalID)):
        chNodeID2 = nodeID[i]
        chTerminalID2 = nterminalID[i1]
        chGTerminalID2 = cursorObj.execute(
            "SELECT GraphicTerminal_ID, PosX, PosY FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                str(chTerminalID2))).fetchone()[0]
        chElementID = cursorObj.execute(
            "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                str(chTerminalID2))).fetchone()[0]
        chTerminalID1 = cursorObj.execute(
            "SELECT Terminal_ID FROM Terminal WHERE TerminalNo='1' AND Element_ID IN ({0})".format(
                str(chElementID))).fetchone()[0]
        chGTerminalID1 = cursorObj.execute(
            "SELECT GraphicTerminal_ID, PosX, PosY FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                str(chTerminalID1))).fetchone()[0]
        print(chGTerminalID1, chGTerminalID2, chElementID, chNodeID2)
        input('SAVE')
con.commit()
con.close()

