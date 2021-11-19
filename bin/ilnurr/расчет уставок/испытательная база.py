import sqlite3
import pandas as pd


def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()
protTerminalID = []
#   ---- ---- ОПРЕДЕЛЕНИЕ СВЯЗКИ ЛИНИЙ С ЗАЩИТАМИ 'ПКТ-10 (50 A)'
#   ---- Выбор рассматриваемой защиты             'ПКТ-10 (50 А)'
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
            '16763904', str(ptxGTerminalID[ptx3]))).fetchone()

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

stopWhileProt = 0
nextNodeID = []
listOfLastNode = []
lastNodeID = []
checkedTerminalID = []
forgottenTerminalID = []
nextTerminalID = []
for prot2 in range(len(protTerminalID)):

    usl1 = True  # False, когда закончатся forgottenTerminalID
    while usl1 is True:
        usl2 = True  # False, когда последняя шина
        if forgottenTerminalID == [] and nextTerminalID != []:
            usl1 = False
            continue
        print(usl1)
        nextTerminalID = []
        for osn1 in range(len(forgottenTerminalID)):
            nextTerminalID += [forgottenTerminalID[osn1]]
        print('\nВышли из условия\nНекст терминал:', nextTerminalID, '\n')
        while usl2 is True:
            #   Элемент
            if nextTerminalID == []:
                thisElementID = cursorObj.execute(
                    "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(protTerminalID[prot2]))).fetchall()
                thisElementID = name_changer(thisElementID)
                elementNameID = cursorObj.execute(
                    "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                        str(thisElementID[0]))).fetchall()
                print('Элемент с защитами:', thisElementID, elementNameID[0][0])

            else:
                if nextTerminalID == forgottenTerminalID:
                    removeTerminalID = nextTerminalID[0]
                    forgottenTerminalID.remove(removeTerminalID)
                    # nextTerminalID.insert(0, removeTerminalID)
                thisElementID = cursorObj.execute(
                    "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(nextTerminalID[0]))).fetchall()
                thisElementID = name_changer(thisElementID)
                elementNameID = cursorObj.execute(
                    "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                        str(thisElementID[0]))).fetchall()
                print('Просматриваемый эдемент:', thisElementID, elementNameID[0][0])
            #   Терминал конца элемента

            endTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo LIKE 2".format(
                    str(thisElementID[0]))).fetchall()
            endTerminalID = name_changer(endTerminalID)

            print('Терминал в конце элемента:', endTerminalID)
            # input('Продолжить')
            if endTerminalID == []:
                lastNodeID += [nextNodeID]
                usl2 = False
                continue
            if nextNodeID != []:
                nextNodeID0 = nextNodeID
            nextNodeID = cursorObj.execute(
                "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(endTerminalID[0]))).fetchall()
            nextNodeID = name_changer(nextNodeID)
            checkedTerminalID += (nextNodeID)
            print('Просмотренные терминалы:', checkedTerminalID)
            print('Следующий узел:', nextNodeID)
            #   Следующий терминал
            nextTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND TerminalNo IN ({1})".format(
                    str(nextNodeID[0]), '1')).fetchall()
            nextTerminalID = name_changer(nextTerminalID)
            print('Некст терминал:', nextTerminalID)
            #   ---- Если терминал не один
            if len(nextTerminalID) > 1:
                forgottenTerminalID += (nextTerminalID[1:])
            print('Оставшиеся терминалы:', forgottenTerminalID)
            print()
            #   ---- Если дальше нет терминала
            if nextTerminalID == []:
                lastNodeID += [nextNodeID]
                usl2 = False
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
                    lastNodeID += [nextNodeID]
                    usl2 = False
            print()
        print('ТО, РАДИ ЧЕГО МЫ ЗДЕСЬ СОБРАЛИСЬ:' , lastNodeID)
    print('Узлы посчитаны')
#     for prot3 in range(len(thisElementID)):
#         endTerminalID = cursorObj.execute(
#             "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND TerminalNo LIKE 2".format(
#                 str(thisElementID[prot3]))).fetchall()
#         endTerminalID = name_changer(endTerminalID)
#         print('Терминал в конце элемента:', endTerminalID)
#         if endTerminalID == []:
#             lastNodeID += [nextNodeID]
#             break
#         for prot4 in range(len(endTerminalID)):
#
#             if nextNodeID != []:
#                 nextNodeID0 = nextNodeID
#             nextNodeID = cursorObj.execute(
#                 "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
#                     str(endTerminalID[prot4]))).fetchall()
#             nextNodeID = name_changer(nextNodeID)
#
#             print('Следующий узел:', nextNodeID)
#             for prot5 in range(len(nextNodeID)):
#
#                 nextTerminalID = cursorObj.execute(
#                     "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND TerminalNo IN ({1})".format(
#                         str(nextNodeID[prot5]), '1')).fetchall()
#                 nextTerminalID = name_changer(nextTerminalID)
#
#                 #   ---- Если дальше нет терминала
#                 if nextTerminalID == []:
#                     lastNodeID += [nextNodeID]
#
#                 #   ---- Если дальше стоит предохранитель
#                 ptxLocID = cursorObj.execute(
#                         "SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0})".format(
#                             str(nextTerminalID[0]))).fetchone()
#
#                 if ptxLocID is None:
#                     continue
#                 else:
#                     ptxName = cursorObj.execute(
#                             "SELECT p_nam FROM ProtOCSetting WHERE ProtLoc_ID IN ({0})".format(
#                                 str(ptxLocID[0]))).fetchone()
#                 if ptxName[0] is None:
#                     continue
#                 else:
#                     if ptxName[0][:3] == 'ПТК':
#                         lastNodeID += [nextNodeID]
#                 print('nextTerminalID', nextTerminalID)
#     if lastNodeID != []:
#         listOfLastNode += [lastNodeID]
# print('Список конечных шин по узлам:', listOfLastNode)
