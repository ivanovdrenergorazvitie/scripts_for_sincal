import sqlite3

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

nodeID = cursorObj.execute("SELECT Node_ID FROM Node WHERE VoltLevel_ID='2'").fetchall()
nodeID = name_changer(nodeID)
print('Узлы 0,4 кВ:', len(nodeID), '\n', nodeID)
needtochange = []
bb = 0
k = 0
i = -1
RelLineType = cursorObj.execute("SELECT LineType_ID FROM RelLineType WHERE Name='УПР'").fetchone()[0]
print('АЙДИ УПР:', RelLineType)
while i < len(nodeID) - 1:
    i += 1
    transID = cursorObj.execute(
        "SELECT Element_ID FROM Terminal WHERE Node_ID IN ({0}) AND TerminalNo='2'".format(
            str(nodeID[i]))).fetchone()[0]
    HVBusbarID = cursorObj.execute(
        "SELECT Node_ID FROM Terminal WHERE Element_ID IN ({0}) AND Node_ID NOT IN ({1})".format(
            str(transID), str(nodeID[i]))).fetchone()[0]
    HVBusbarName = cursorObj.execute(
        "SELECT Name FROM Node WHERE Node_ID IN ({0})".format(
            str(HVBusbarID))).fetchone()[0]
    THVBusbarID = cursorObj.execute(
        "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0})".format(str(HVBusbarID))).fetchall()
    THVBusbarID = name_changer(THVBusbarID)
    for i1 in THVBusbarID:
        EHVBusbarID = cursorObj.execute(
            "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(str(i1))).fetchone()[0]
        ETHVBusbarID = cursorObj.execute(f"SELECT Type FROM Element WHERE Element_ID IN ({EHVBusbarID})"). fetchone()[0]
        if ETHVBusbarID != 'Line':
            continue
        HVBusbarID2 = cursorObj.execute(
            f'SELECT Node_ID FROM Terminal WHERE Element_ID IN ({EHVBusbarID}) AND Node_ID NOT IN ({HVBusbarID})').fetchone()[0]
        # if HVBusbarID2 == []:
        #     continue

        HVBusbarName2 = cursorObj.execute(f'SELECT Name FROM Node WHERE Node_ID IN ({HVBusbarID2})').fetchone()[0]
        if HVBusbarName2.split('-')[:-1] == HVBusbarName.split('-')[:-1] and len(HVBusbarName2.split('-')) > 2:
            ThisHVBusbars = [HVBusbarName, HVBusbarName2]
            if ThisHVBusbars[0] == ThisHVBusbars[1]:
                bb = 0
                continue
            if ThisHVBusbars[1] == bb:
                continue

            bb = HVBusbarName
            HVBElementID1 = cursorObj.execute(
                f"SELECT Element_ID FROM Terminal WHERE Node_ID IN ({HVBusbarID})").fetchall()
            HVBElementID1 = name_changer(HVBElementID1)
            HVBElementID2 = cursorObj.execute(
                f"SELECT Element_ID FROM Terminal WHERE Node_ID IN ({HVBusbarID2})").fetchall()
            HVBElementID2 = name_changer(HVBElementID2)
            for s in HVBElementID1:
                if s in HVBElementID2:
                    sectionnik = s
                    break
            print('АЙДИ СЕКЦИОННИКА И ЕГО ИМЯ:', sectionnik, cursorObj.execute(
                f"SELECT Name FROM Element WHERE Element_ID IN ({sectionnik})").fetchone()[0])
            if cursorObj.execute(f"SELECT LineType_ID FROM Line WHERE Element_ID IN ({sectionnik})").fetchone()[0] == RelLineType:
                print('MISSED ------', HVBusbarName, HVBusbarName2, '\n')
                continue

            print('ACCEPTED -------', HVBusbarName, HVBusbarName2)  # [HVBusbarID, HVBusbarID2]
            """
            УДАЛЯЕМ ВЫКЛЮЧАТЕЛЬ
            """
            sectionnikT = cursorObj.execute(f"SELECT Terminal_ID FROM Terminal "
                                            f"WHERE Element_ID IN ({sectionnik})").fetchall()
            sectionnikT = name_changer(sectionnikT)
            for b in sectionnikT:
                cursorObj.execute(f"DELETE FROM Breaker WHERE Terminal_ID IN ({b})")
                cursorObj.execute(f"DELETE FROM GraphicAddTerminal WHERE GraphicTerminal_ID IN ({b})")
                cursorObj.execute(f"UPDATE Terminal SET Flag_State='0' WHERE Terminal_ID IN ({b}) AND Flag_Switch='1'")
                TerminalNo = cursorObj.execute(f"SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({b}) AND Flag_Switch='1'").fetchone()
                print(TerminalNo)
                if TerminalNo == None:
                    continue
                elif TerminalNo[0] == 1:
                    PosX = cursorObj.execute(f"SELECT SymCenterX FROM GraphicElement WHERE GraphicElement_ID IN ({sectionnik})").fetchone()[0]
                    cursorObj.execute(f"UPDATE GraphicElement SET SymCenterX='{PosX + 0.001}' WHERE GraphicElement_ID IN ({sectionnik})")
                elif TerminalNo[0] == 2:
                    PosX = cursorObj.execute(f"SELECT SymCenterX FROM GraphicElement WHERE GraphicElement_ID IN ({sectionnik})").fetchone()[0]
                    cursorObj.execute(f"UPDATE GraphicElement SET SymCenterX='{PosX - 0.001}' WHERE GraphicElement_ID IN ({sectionnik})")

            needtochange += [[[HVBusbarName, HVBusbarID], [HVBusbarName2, HVBusbarID2]]]

            BusbarName = HVBusbarName.split('-')[0] + '-' + HVBusbarName.split('-')[1] + ' Н-' + HVBusbarName.split('-')[2]
            BusbarName2 = HVBusbarName2.split('-')[0] + '-' + HVBusbarName2.split('-')[1] + ' Н-' + HVBusbarName2.split('-')[2]

            k += 1
            if HVBusbarName == 'ТП-1081-1':
                BusbarName = 'ТП-1081-1 0,4 кВ'
                BusbarName2 = 'ТП-1081-2 0,4 кВ'
            if HVBusbarName == 'РП-1-1':
                BusbarName = 'ТП-270 Н-1'
                BusbarName2 = 'ТП-270 Н-2'
            if HVBusbarName == 'РП-4-1':
                BusbarName = 'ТП-138 Н-1'
                BusbarName2 = 'ТП-138 Н-2'
            if HVBusbarName == 'РП-8-2':
                BusbarName = 'ТП-113 Н-2'
                BusbarName2 = 'ТП-113 Н-1'
            if HVBusbarName == 'РП-10-1' or HVBusbarName == 'РП-11-1' or HVBusbarName == 'ТП-92-1':     # HVBusbarName == 'ТП-224-2' or HVBusbarName == 'ТП-6003-2' or HVBusbarName == 'ТП-114-2' or HVBusbarName == 'ТП-1081-2'
                continue
            if HVBusbarName.split('-')[-1][0] == '2':
                continue

            print(BusbarName, BusbarName2, k)
            BusbarID = cursorObj.execute(f"SELECT Node_ID FROM Node WHERE Name IN ('{BusbarName}')").fetchone()[0]
            BusbarID2 = cursorObj.execute(f"SELECT Node_ID FROM Node WHERE Name IN ('{BusbarName2}')").fetchone()[0]
            # TransNameID = cursorObj.execute(f"SELECT Name FROM Element WHERE Element_ID IN ({transID})").fetchone()[0]
            # print(TransNameID, '\n')
            GBusbarID = cursorObj.execute(
                f"SELECT GraphicNode_ID, NodeStartX, NodeStartY, NodeEndX, NodeEndY FROM GraphicNode WHERE Node_ID IN ({BusbarID})").fetchone()
            GBusbarID2 = cursorObj.execute(
                f"SELECT GraphicNode_ID, NodeStartX, NodeStartY, NodeEndX, NodeEndY FROM GraphicNode WHERE Node_ID IN ({BusbarID2})").fetchone()
            # Горизонтально
            print(GBusbarID, GBusbarID2)
            LBusbarID = cursorObj.execute(f"SELECT Element_ID FROM Terminal WHERE Node_ID IN ({BusbarID}) AND TerminalNo='1'").fetchone()[0]
            LBusbarID2 = cursorObj.execute(f"SELECT Element_ID FROM Terminal WHERE Node_ID IN ({BusbarID2}) AND TerminalNo='1'").fetchone()[0]
            GLBusbarID = cursorObj.execute(f"SELECT GraphicElement_ID, SymCenterX, SymCenterY FROM GraphicElement WHERE Element_ID IN ({LBusbarID})").fetchone()
            GLBusbarID2 = cursorObj.execute(f"SELECT GraphicElement_ID, SymCenterX, SymCenterY FROM GraphicElement WHERE Element_ID IN ({LBusbarID2})").fetchone()
            if (GBusbarID[1] - GBusbarID2[1])**2 > (GBusbarID[2] - GBusbarID2[2])**2:
                cursorObj.execute(f"UPDATE GraphicNode SET NodeStartY=('{GLBusbarID2[2] + 0.001}') WHERE GraphicNode_ID IN ({GBusbarID[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeStartY=('{GLBusbarID2[2] + 0.001}') WHERE GraphicNode_ID IN ({GBusbarID2[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeStartX=('{str(float(GBusbarID[1]) - 0.001)}') WHERE GraphicNode_ID IN ({GBusbarID[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeStartX=('{str(float(GBusbarID2[1]) - 0.002)}') WHERE GraphicNode_ID IN ({GBusbarID2[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeEndY=('{GLBusbarID2[2] + 0.001}') WHERE GraphicNode_ID IN ({GBusbarID[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeEndY=('{GLBusbarID2[2] + 0.001}') WHERE GraphicNode_ID IN ({GBusbarID2[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeEndX=('{str(float(GBusbarID[1]) + 0.002)}') WHERE GraphicNode_ID IN ({GBusbarID[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET NodeEndX=('{str(float(GBusbarID2[1]) + 0.001)}') WHERE GraphicNode_ID IN ({GBusbarID2[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET SymType='3' WHERE GraphicNode_ID IN ({GBusbarID[0]})")
                cursorObj.execute(f"UPDATE GraphicNode SET SymType='3' WHERE GraphicNode_ID IN ({GBusbarID2[0]})")


                BBTerminal = cursorObj.execute(f"SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({nodeID[i]})").fetchall()
                BBTerminal = name_changer(BBTerminal)
                cursorObj.execute(f"UPDATE GraphicTerminal SET PosY=({GBusbarID2[2] - 0.001}) WHERE Terminal_ID IN ({BBTerminal[0]})")
                cursorObj.execute(f"UPDATE GraphicTerminal SET PosY=({GBusbarID2[2] - 0.001}) WHERE Terminal_ID IN ({BBTerminal[1]})")
                print(BBTerminal, '\n')

                """
                ВЫКЛЮЧАТЕЛЬ АВР
                """
                MaxLine = cursorObj.execute("SELECT MAX(Element_ID) FROM Element").fetchone()[0]
                cursorObj.execute(f"INSERT INTO Line VALUES ({MaxLine + 1}, 3, '', 0, 0, 0.0, 0.001, 1.0, 1, 0, 1.0, 0, 0.0, 0.1, 0.4, 0.0, 10.0, 2, 1, 0.0, 10.0, 50.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1.0, 0.0, 50.0, 50.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0,	0, 0.0, 1, 3, 0.5, 1, 10.0, 10.0, 10.0, 0, 0, 1, 1, '', 0.004, 0, 0.0, 0.0, 0.0, 0)")
                cursorObj.execute("INSERT INTO Element VALUES({0}, 1, 1, 22, 1, {1}, {1}, 'Line', 263, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, '', 0.0, '', 0.0, 0.0, 4, 0, 0, 0, '', :null, 1.0, 1.0)".format(str(MaxLine + 1), str("'" + 'L' + str(MaxLine + 1) + "'")), {'null': None})
                MaxGElement = cursorObj.execute("SELECT MAX(GraphicElement_ID) FROM GraphicElement").fetchone()[0]
                MaxGText = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchone()[0]
                cursorObj.execute(f"INSERT INTO GraphicText VALUES ({MaxGText + 1}, 1, 'Arial', 16, 4, 2, 0, 0, 1, 1, 0.0, 0.00225, 0.0, 0, 0, 0, 1, 1)")
                cursorObj.execute(f"INSERT INTO GraphicElement VALUES ({MaxGElement + 1}, 1, 1, {MaxGText + 1}, 0, {MaxLine + 1}, 1, 0, -1, 0, 0, 30, {(GBusbarID2[1] + GBusbarID[3])/2}, {GBusbarID2[2] - 0.001}, 19, 0, 0, 1, 1, 1, 0)")

                MaxTerminal = cursorObj.execute("SELECT MAX(Terminal_ID) FROM Terminal").fetchone()[0]
                cursorObj.execute(f"INSERT INTO Terminal VALUES ({MaxTerminal + 1}, {MaxLine + 1}, {BusbarID}, 1, 1, 0, 0.0, 0.0, 7, 1, 0, 1, 1, 0)")
                cursorObj.execute(f"INSERT INTO Terminal VALUES ({MaxTerminal + 2}, {MaxLine + 1}, {BusbarID2}, 1, 2, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)")
                MaxGTerminal = cursorObj.execute("SELECT MAX(GraphicTerminal_ID) FROM GraphicTerminal").fetchone()[0]
                MaxGText = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchone()[0]
                cursorObj.execute(f"INSERT INTO GraphicText VALUES ({MaxGText + 1}, 1, 'Arial', 16, 4, 8, 0, 0, 1, 1, 0.0, 0.0025, -0.0025, 0, 0, 0, 1, 1)")
                cursorObj.execute(f"INSERT INTO GraphicTerminal VALUES ({MaxGTerminal + 1}, {MaxGElement + 1}, {MaxGText + 1}, {MaxTerminal + 1}, {(GBusbarID[1] + 0.002)}, {GBusbarID2[2] - 0.001}, 0, 0, 0, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)")
                cursorObj.execute(f"INSERT INTO GraphicText VALUES ({MaxGText + 2}, 1, 'Arial', 16, 4, 8, 0, 0, 1, 1, 0.0, 0.0025, -0.0025, 0, 0, 0, 1, 1)")
                cursorObj.execute(f"INSERT INTO GraphicTerminal VALUES ({MaxGTerminal + 2}, {MaxGElement + 1}, {MaxGText + 2}, {MaxTerminal + 2}, {(GBusbarID2[1] - 0.002)}, {GBusbarID2[2] - 0.001}, 0, 0, 0, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)")

                MaxGATerminal = cursorObj.execute("SELECT MAX(GraphicAddTerminal_ID) FROM GraphicAddTerminal").fetchone()[0]
                MaxGText = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchone()[0]
                cursorObj.execute(f"INSERT INTO GraphicText VALUES ({MaxGText + 1}, 1, 'Arial', 16, 4, 8, 0, 0, 1, 1, 0.0, 0.0025, -0.0025, 0, 0, 0, 1, 1)")
                cursorObj.execute(f"INSERT INTO GraphicAddTerminal VALUES ({MaxGATerminal + 1}, {MaxTerminal + 1}, 1, 1, {MaxGText + 1},  0, -1, 0, 0, '40', 4, 4, 0, {(GBusbarID2[1] + GBusbarID[3])/2}, {GBusbarID2[2] - 0.001}, 292, 65536, 0, 176, 1, 0, 10, 1, 1)") # "{GBusbarID[1] + ((GBusbarID[1] - GBusbarID2[1])/2)}
                MaxBreaker = cursorObj.execute("SELECT MAX(Breaker_ID) FROM Breaker").fetchone()[0]
                cursorObj.execute(f"INSERT INTO Breaker VALUES ({MaxBreaker + 1}, {MaxTerminal + 1}, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 1, 1, '', '', 1, 0, 0.0, 1, 0, 0, 0, 1, 1, 1, 1, 0)")


            # Вертикально
            # elif (GBusbarID[1] - GBusbarID2[1])**2 < (GBusbarID[2] - GBusbarID2[2])**2:


        else:
            continue
print(needtochange)
con.commit()
con.close()
#     sectionnikID0 = cursorObj.execute(
#         "SELECT Element_ID FROM Terminal WHERE Node_ID IN ({0})".format(
#             str(busbarID))).fetchall()
#     sectionnikID0 = name_changer(sectionnikID0)
#
#     for i1 in range(len(sectionnikID0)):
#         sectionnikname = cursorObj.execute(
#             "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(str(sectionnikID0[i1]))).fetchone()[0]
#         sectionnikID0T = cursorObj.execute(
#             "SELECT Terminal_ID, Flag_Switch FROM Terminal WHERE Element_ID IN ({0})".format(
#                 str(sectionnikID0[i1]))).fetchall()
#
#         if (sectionnikID0T[0][1] == 0 and sectionnikID0T[1][1] == 1) or (sectionnikID0T[0][1] == 1 and sectionnikID0T[1][1] == 0):
#             # print(sectionnikID0T, busbarID, sectionnikname)
#             sectionnikID1 = cursorObj.execute(
#                 "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
#                     str(sectionnikID0T[0][0]))).fetchone()[0]
#             sectionnikID1E = cursorObj.execute(
#                 "SELECT Element_ID FROM Element WHERE Element_ID IN ({0}) AND Type='Line'".format(
#                     str(sectionnikID1))).fetchone()
#             if sectionnikID1E == None:
#                 continue
#             sectionnikID1E = sectionnikID1E[0]
#             sectionniklist += [sectionnikID1E]
#             print(sectionnikID1E, sectionninkame)
# print(sectionniklist)

