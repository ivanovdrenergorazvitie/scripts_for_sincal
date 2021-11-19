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
    print(ProtLocID)

protElementID = []
for prot in range(len(protTerminalID)):
    protElementID0 = cursorObj.execute(
        "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
            str(protTerminalID[prot]))).fetchall()
    protElementID0 = name_changer(protElementID0)
    protElementID += [protElementID0[0]]
print('EBEYSHI SPISOK', protElementID)


# stopWhileProt = 0
allProtLastNodeID = []
for prot2 in range(len(protElementID)):
    nextNodeID = []
    listOfLastNode = []
    lastNodeID = []
    checkedTerminalID = []
    forgottenTerminalID = []
    nextTerminalID = []
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
                elementNameID = cursorObj.execute(
                    "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                        str(thisElementID[0]))).fetchall()
                print('Просматриваемый элемент:', thisElementID, elementNameID[0][0])
                try:
                    print('\n\n\n\n\n', thisElementID[0], protElementID)
                    protElementID.index(thisElementID[0])
                    usl2 = False
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
    allProtLastNodeID += [lastNodeID]
    print('Это узлы по защитам. Формирование списка надо фиксить:', allProtLastNodeID)


con.commit()  # подтверждаем изменения в БД
con.close()