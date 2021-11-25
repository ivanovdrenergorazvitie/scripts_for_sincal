
import sqlite3

def centrovka(elementID, cursorObj, variantID):
    print('\n\n\n\n ЦЕНТРОВКА СИМВОЛОВ ЭЛЕМЕНТА')
    for el1 in range(len(elementID)):
        # Определение направления
        for var in variantID:
            terminalID = cursorObj.execute(
                "SELECT TerminalNo, Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(elementID[el1]), str(var))).fetchall()
            if terminalID != []:
                print(terminalID)
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
                    str((gtx1 + gtx2) / 2), str(elementID[el1])))
                cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                    str((gty1 + gty2) / 2), str(elementID[el1])))
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
                    str((gtx1 + bpx2) / 2), str(elementID[el1])))

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
                    str((bpx1 + gtx2) / 2), str(elementID[el1])))
                cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                    str((bpy1 + gty2) / 2), str(elementID[el1])))

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
                    str((bpx1 + bpx2) / 2), str(elementID[el1])))
                cursorObj.execute("UPDATE GraphicElement SET SymCenterY=({0}) WHERE Element_ID IN ({1})".format(
                    str((bpy1 + bpy2) / 2), str(elementID[el1])))

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
            cursorObj.execute(
                "UPDATE GraphicText SET Pos1=({0}) WHERE GraphicText_ID IN ({1})".format(str(kx), str(gtext)))
            cursorObj.execute(
                "UPDATE GraphicText SET Pos2=({0}) WHERE GraphicText_ID IN ({1})".format(str(ky), str(gtext)))
            print('BPOINT:', bpointID1, bpointID2)


def size(ksize, cursorObj, variantID):
    print('\n\n\n\n УВЕЛИЧЕНИЕ СХЕМЫ')
    coord_gbpoint = cursorObj.execute(
        "SELECT GraphicPoint_ID, PosX, PosY, Variant_ID FROM GraphicBucklePoint").fetchall()
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


def nodes_texts(nodeID, cursorObj, variantID):
    print('\n\n\n\n РАССТАНОВКА УЗЛОВ И ТЕКСТА')
    for i in range(len(nodeID)):
        ff7 = 1
        nterminalID = cursorObj.execute(
            "SELECT TerminalNo, Terminal_ID FROM Terminal WHERE Node_ID IN ({0})".format(
                str(nodeID[i]))).fetchall()
        print(nodeID[i])
        try:
            l = next('not error' for y in range(len(nterminalID)) if nterminalID[y][0] == 1)
            ff7 = 0
        except:
            print(nterminalID, '- КОНЕЧНЫЙ БУСБАР')
        if nterminalID == []:
            cursorObj.execute("DELETE FROM GraphicNode WHERE Node_ID IN ({0})".format(str(nodeID[i])))
            continue

        for i1 in range(len(nterminalID)):
            chNodeID2 = nodeID[i]
            chTerminalID2 = nterminalID[i1]
            chGTerminalID2 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                    str(chTerminalID2[1]))).fetchall()[0]
            chElementID = cursorObj.execute(
                "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(chTerminalID2[1]))).fetchone()[0]
            chGElementID = cursorObj.execute(
                "SELECT GraphicElement_ID, SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicElement_ID IN ({0})".format(
                    str(chElementID))).fetchall()[0]
            chTerminalID1 = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE TerminalNo='1' AND Element_ID IN ({0})".format(
                    str(chElementID))).fetchone()[0]
            chGTerminalID1 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
                    str(chTerminalID1))).fetchall()[0]
            gnodeID = cursorObj.execute(
                "SELECT GraphicNode_ID, NodeStartX, NodeStartY, NodeEndX, NodeEndY, GraphicText_ID1 "
                "FROM GraphicNode WHERE Node_ID IN ({0})".format(
                    str(nodeID[i]))).fetchall()[0]
            BPointID1 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY, NoPoint FROM GraphicBucklePoint "
                "WHERE GraphicTerminal_ID IN ({0})".format(
                    str(chGTerminalID1[0]))).fetchall()
            BPointID2 = cursorObj.execute(
                "SELECT GraphicTerminal_ID, PosX, PosY, NoPoint FROM GraphicBucklePoint "
                "WHERE GraphicTerminal_ID IN ({0})".format(
                    str(chGTerminalID2[0]))).fetchall()


            if BPointID1 != [] or BPointID2 != []:
                ff7 = 0
            if len(nterminalID) > 1:
                print(nterminalID, 'НТЕРМИНАЛИД ИСКЛЮЧЕНИЕ')
                ff7 = 0
            if (chGTerminalID1[1] - chGTerminalID2[1] > 0.0005 or chGTerminalID1[1] - chGTerminalID2[1] < -0.0005) and (chGTerminalID1[2] - chGTerminalID2[2] > 0.0005 or chGTerminalID1[2] - chGTerminalID2[2] < -0.0005):
                print(chGTerminalID1[1] - chGTerminalID2[1], chGTerminalID1[2] - chGTerminalID2[2], 'ГНОДЕИД ИСКЛЮЧЕНИЕ')
                ff7 = 0


            # Надпись справа
            if (gnodeID[1] - gnodeID[3]) ** 2 > (gnodeID[2] - gnodeID[4]) ** 2:
                # Смотрит вверх
                print(chGTerminalID1)
                if chGElementID[2] < chGTerminalID2[2]:
                    print('ВВЕРХ')
                    if ff7 == 1:
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosX=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[1]), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosY=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.02), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[1]), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterY=({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.01), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartX=({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndX=({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartY=({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndY=({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.02), str(gnodeID[0])))
                    kx = 0.0025
                    ky = 0

                # Смотрит вниз
                elif chGElementID[2] > chGTerminalID2[2]:
                    print('ВНИЗ')
                    if ff7 == 1:
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosX=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[1]), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosY=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.02), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[1]), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterY = ({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.01), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] - 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] - 0.02), str(gnodeID[0])))
                    kx = gnodeID[3] - gnodeID[1] + 0.0025
                    ky = 0

            elif (gnodeID[1] - gnodeID[3]) ** 2 < (gnodeID[2] - gnodeID[4]) ** 2:
                # Смотрит вправо
                if chGElementID[1] < chGTerminalID2[1]:
                    print('ВПРАВО')
                    if ff7 == 1:
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosX=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.02), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosY=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[2]), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.01), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterY = ({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[2]), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] + 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] - 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.002), str(gnodeID[0])))
                    kx = 0
                    ky = 0.0025

                # Смотрит влево
                if chGElementID[1] > chGTerminalID2[1]:
                    print('ВЛЕВО')
                    if ff7 == 1:
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosX=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.02), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicTerminal SET PosY=({0}) WHERE GraphicTerminal_ID IN ({1})".format(
                                str(chGTerminalID1[2]), str(chGTerminalID2[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterX=({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.01), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicElement SET SymCenterY = ({0}) WHERE GraphicElement_ID IN ({1})".format(
                                str(chGTerminalID1[2]), str(chGElementID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndX = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[1] - 0.02), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeStartY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] + 0.002), str(gnodeID[0])))
                        cursorObj.execute(
                            "UPDATE GraphicNode SET NodeEndY = ({0}) WHERE GraphicNode_ID IN ({1})".format(
                                str(chGTerminalID1[2] - 0.002), str(gnodeID[0])))
                    kx = 0
                    ky = 0.0025 + gnodeID[4] - gnodeID[2]
            print(kx, ky, gnodeID[5])
            cursorObj.execute(
                "UPDATE GraphicText SET Pos1=({0}) WHERE GraphicText_ID IN ({1})".format(str(kx), str(gnodeID[5])))
            cursorObj.execute(
                "UPDATE GraphicText SET Pos2=({0}) WHERE GraphicText_ID IN ({1})".format(str(ky), str(gnodeID[5])))