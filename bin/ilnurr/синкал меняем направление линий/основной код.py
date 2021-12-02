import sqlite3
import pandas as pd


def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
print(con)
cursorObj = con.cursor()
listOfPkt = ('ПКТ-10 (2 A)', 'ПКТ-10 (3 A)', 'ПКТ-10 (5 A)', 'ПКТ-10 (8 A)', 'ПКТ-10 (10 A)', 'ПКТ-10 (16 A)',
             'ПКТ-10 (20 A)', 'ПКТ-10 (31 A)', 'ПКТ-10 (40 A)', 'ПКТ-10 (50 A)', 'ПКТ-10 (80 A)', 'ПКТ-10 (100 A)',
             'ПКТ-10 (160 A)', 'ПКТ-6 (2 A)', 'ПКТ-6 (3 A)', 'ПКТ-6 (5 A)', 'ПКТ-6 (8 A)', 'ПКТ-6 (10 A)',
             'ПКТ-6 (16 A)', 'ПКТ-6 (20 A)', 'ПКТ-6 (31 A)', 'ПКТ-6 (40 A)', 'ПКТ-6 (50 A)', 'ПКТ-6 (63 A)',
             'ПКТ-6 (80 A)', 'ПКТ-6 (100 A)', 'ПКТ-6 (160 A)', 'ПКТ-6 (200 A)', 'ПКТ-6 (315 A)')
infElementID = cursorObj.execute(
    "SELECT Element_ID FROM Element WHERE Type == 'Infeeder'").fetchall()
infElementID = name_changer(infElementID)
print(infElementID)
allProtLastNodeID = []
allChangingTerminals = []
for napr1 in range(len(infElementID)):
    nextNodeID = []
    listOfLastNode = []
    lastNodeID = []
    checkedNodeID = []
    forgottenTerminalID = []
    nextTerminalID = []
    usl1 = True
    while usl1 is True:
        usl2 = True
        if forgottenTerminalID == [] and nextTerminalID != []:
            usl1 = False  #    ---- если закончатся Терминалы, которые нужно рассмотреть
            continue
        print(usl1)
        nextTerminalID = []
        for osn1 in range(len(forgottenTerminalID)):
            nextTerminalID += [forgottenTerminalID[osn1]]
            # if nextTerminalID[0] == 130:
            #     input('КОРРЕКТИВЫ')
        print('\nВышли из условия\nНекст терминал:', nextTerminalID, '\n')
        while usl2 is True:
            usl3 = 1
            if nextTerminalID == []: #  ---- первый вход в цикл while, где берется терминал источника

                #    [ ]    <- в роли энд терминала выступает источник
                #    _|_    <- хапаем энд терминал
                #    А затем и узел
                endTerminalID = cursorObj.execute(
                    "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0})".format(
                        str(infElementID[napr1]))).fetchall()   #   ---- собсна эндтерминал, потому что находится перед следующим узлом после элемента
                endTerminalID = name_changer(endTerminalID)
                nextNodeID = cursorObj.execute(
                    "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(endTerminalID[0]))).fetchall()
                nextNodeID = name_changer(nextNodeID)
                checkedNodeID += [nextNodeID[0]]   #   ---- добавляем узел в просмотренный (он в формате [49], поэтому индексируем)
                print('Просмотренные терминалы:', checkedNodeID)
                print('Следующий узел:', nextNodeID)
                nodeName = cursorObj.execute(
                    "SELECT Name FROM Node WHERE Node_ID IN ({0})".format(str(nextNodeID[0]))).fetchone()[0]
                print(nodeName)

                #   Следующий терминал
                #     _|_
                #      | <- собсна некст терминал (TerminalNo = 1)
                nextTerminalID0 = cursorObj.execute(
                    "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND Terminal_ID NOT LIKE ({1})".format(
                        str(nextNodeID[0]), str(endTerminalID[0]))).fetchall()
                nextTerminalID = name_changer(nextTerminalID0)
                if len(nextTerminalID) > 1:
                    forgottenTerminalID += (nextTerminalID[1:]) #   ---- Если терминалов несколько, хапаем их в список (всех, кроме первого - с первым работаем)
                print('Оставшиеся терминалы:', forgottenTerminalID)
                print()
                # for napr2 in range(len(nextTerminalID)):
                #     numbNextTerminal = cursorObj.execute(
                #         "SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({0})".format(
                #             str(nextTerminalID[napr2]))).fetchall()
                #     numbNextTerminal = name_changer(numbNextTerminal)   #   ---- Берем направление терминала, где 1 - начало элемента, 2 - конец
                #     if numbNextTerminal == [2]: #   ---- Так как это некст терминал, а не энд терминал, направление должно быть 1
                #         cursorObj.execute(
                #             "UPDATE Terminal SET TerminalNo=({0}) WHERE Terminal_ID IN ({1})".format(
                #                 '1', str(nextTerminalID[napr2])))
                #         allChangingTerminals += [nextTerminalID[napr2], numbNextTerminal]

            if nextTerminalID == forgottenTerminalID:
                removeTerminalID = nextTerminalID[0]
                forgottenTerminalID.remove(removeTerminalID)
            if len(nextTerminalID) > 1:
                usl3 = 0
                #    _|_
                #    ||| <- несколько некст терминалов фиксируем как usl3, чтобы использовать в условиях конечных узлов
            thisElementID = cursorObj.execute(
                "SELECT Element_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(nextTerminalID[0]))).fetchall()
            thisElementID = name_changer(thisElementID)
            elementNameID = cursorObj.execute(
                "SELECT Name FROM Element WHERE Element_ID IN ({0})".format(
                    str(thisElementID[0]))).fetchall()[0]
            print('Просматриваемый элемент:', thisElementID, elementNameID[0])
            #   Терминал конца элемента
            #   _|_ <- энд терминал (TerminalNo = 2)
            #    |
            endTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND Terminal_ID NOT LIKE ({1})".format(
                    str(thisElementID[0]), str(nextTerminalID[0]))).fetchall()
            endTerminalID = name_changer(endTerminalID)
            print('Терминал в конце элемента:', endTerminalID)
            for napr3 in range(len(endTerminalID)):
                numbEndTerminal = cursorObj.execute("SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(endTerminalID[napr3]))).fetchall()
                numbEndTerminal = name_changer(numbEndTerminal)
                if numbEndTerminal == [1]:
                    cursorObj.execute(
                        "UPDATE Terminal SET TerminalNo=({0}) WHERE Terminal_ID IN ({1})".format(
                            '2', str(endTerminalID[napr3])))
                    startTerminalID = cursorObj.execute(
                        "SELECT Terminal_ID FROM Terminal WHERE Element_ID IN ({0}) AND Terminal_ID NOT LIKE ({1})".format(
                            str(thisElementID[0]), str(endTerminalID[napr3]))).fetchall()
                    startTerminalID = name_changer(startTerminalID)
                    cursorObj.execute(
                        "UPDATE Terminal SET TerminalNo=({0}) WHERE Terminal_ID IN ({1})".format(
                            '1', str(startTerminalID[0])))
                    allChangingTerminals += [nextTerminalID[napr3], numbEndTerminal]
            #   ---- ---- УСЛОВИЯ КОНЕЧНЫХ УЗЛОВ И УЗЛОВ С АЛЬТЕРНАТИВНЫМ ПРОДОЛЖЕНИЕМ
            #   ---- Нагрузка и отсутствие
            #
            #       _|_
            #        |
            #        * <- у нагрузок нет конечного терминала
            if endTerminalID == []:
                if usl3 == 1:
                    lastNodeID += [nodeName] #  ---- соответственно, если нет дополнительных терминалов, то мы записываем узел как конечный
                usl2 = False
                continue
            # if nextNodeID != []:
            #     nextNodeID0 = nextNodeID  <--- не уверен, что это условие жизненно необходимо
            nextNodeID = cursorObj.execute(
                "SELECT Node_ID FROM Terminal WHERE Terminal_ID IN ({0})".format(
                    str(endTerminalID[0]))).fetchall()
            nextNodeID = name_changer(nextNodeID)

            checkedNodeID += (nextNodeID)
            print('Просмотренные терминалы:', checkedNodeID)
            print('Следующий узел:', nextNodeID)
            nodeName = cursorObj.execute(
                "SELECT Name FROM Node WHERE Node_ID IN ({0})".format(str(nextNodeID[0]))).fetchone()[0]
            print('Имя этого узла:', nodeName)

            #   Следующий терминал
            #   Следующий терминал
            #     _|_
            #      | <- собсна некст терминал (TerminalNo = 1)
            nextTerminalID = cursorObj.execute(
                "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0}) AND Terminal_ID NOT LIKE ({1})".format(
                    str(nextNodeID[0]), str(endTerminalID[0]))).fetchall()
            nextTerminalID = name_changer(nextTerminalID)
            print('Некст терминал:', nextTerminalID)
            usl3 = 1
            if len(nextTerminalID) > 1:
                usl3 = 0
                forgottenTerminalID += (nextTerminalID[1:])

            for napr4 in range(len(nextTerminalID)):
                numbNextTerminal = cursorObj.execute(
                    "SELECT TerminalNo FROM Terminal WHERE Terminal_ID IN ({0})".format(
                        str(nextTerminalID[napr4]))).fetchall()
                name_changer(numbNextTerminal)

                # if numbNextTerminal == [2]:
                #     cursorObj.execute(
                #         "UPDATE Terminal SET TerminalNo=({0}) WHERE Terminal_ID IN ({1})".format(
                #             '1', str(nextTerminalID[napr4])))
                #     allChangingTerminals += [nextTerminalID[napr4], numbNextTerminal]
            print('Оставшиеся терминалы:', forgottenTerminalID)
            print()
            #   ---- Если дальше нет терминала
            #       _|_ <- тупиковая шина
            if nextTerminalID == []:
                lastNodeID += [nodeName]
                usl2 = False
                continue
            #   ---- Если дальше стоит предохранитель
            #           _|_
            #           [|] <- предохранитель
            #   За предохранителями линий обычно больше нет, и смотреть дальше бессмысленно
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
                        lastNodeID += [nodeName]    #   ---- Если нет альтернативных терминалов, то это конечный терминал
                        print('alonetermwithptx', nodeName)
                    usl2 = False
            print()
    allProtLastNodeID += lastNodeID
print('Число конечных узлов:', len(allProtLastNodeID))
print('Конечные узлы:', allProtLastNodeID)
print('Коррективы:', allChangingTerminals)
con.commit()  # подтверждаем изменения в БД
con.close()
