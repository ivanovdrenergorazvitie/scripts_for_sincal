vniz = 0
trans_x = 0.0
trans_y = 0.0
node_x = 0.0
node_y = 0.0
load_x = 0.0
load_y = 0.0
lT = 0
line = 0
lineList = 0
import pl_tr
import pl_load
import pl_elem
def get_coordinates_value(b, cursorObj):
    global lT, line, lineList
    nodeForCoords = []
    #   ---- Выбор узлов с линиями
    for gtc1 in range(len(b) + 1):
        try:
            nodeForCoords += [b[gtc1][0][0]]
        except:
            continue
    print(nodeForCoords, '- nodeForCoords')
    #   ---- Составление списка параметров Терминала выбранных узлов
    line0 = []
    for gtc2 in range(len(nodeForCoords) + 1):
        try:
            line0 += [cursorObj.execute(
                "SELECT * FROM Terminal WHERE Node_ID IN ({0})".format(
                    str(nodeForCoords[gtc2]))).fetchall()]
        except:
            continue
    print(line0, '- line0')
    #   ---- Вывод из тройного списка: line0[[(), ()], [(), ()], [()]] -> line1[(), (), (), (), ()]
    line1 = []
    for gtc3i in range(len(line0) + 1):
        try:
            for gtc3j in range(len(line0[gtc3i]) + 1):
                line1 += [line0[gtc3i][gtc3j]]
                print(gtc3i, gtc3j, '- line1 checking')
        except:
            continue
    print(line1, '- line1')
    #   ---- Отсеивание секционника
    line = []
    line2 = []
    # Part 1
    for gtc4 in range(len(line1) + 1):
        try:
            line2 += [line1[gtc4][1]]
        except:
            continue
    for gtc5 in range(len(line2) + 1):
        try:
            numbOfLine = line2[gtc5]
            kriteriyOfLine = line2.count(numbOfLine)  # 2 - секционник; 1 - линия
            print(line2, gtc5, numbOfLine, kriteriyOfLine, '- line2 in for')
            if kriteriyOfLine == 1:
                line += [line2[gtc5]]
        except:
            continue
    print(line, '- line')

    # Part 2 (составление того же line1 только без секционников)
    lineList = []
    mi = 0
    for gtc6 in line:
        if gtc6 == line1[mi][1]:
            lineList += [line1[mi]]
            mi += 1
        else:
            m1 = mi
            while gtc6 != line1[m1][1]:
                m1 += 1
            lineList += [line1[m1]]
    print(lineList, '- lineList')
    #   ---- Определение терминалов конца линии
    lT_ID1 = []
    for gtc7 in range(len(lineList) + 1):
        try:
            lT_ID1 += [lineList[gtc7][0]]
        except:
            continue
    print(lT_ID1, '- lT_ID1')
    # ---- Составление списка терминалов линии по ID Терминала...
    # lT1 - это как lineList, только не в таблице Terminal, а в таблице GraphicTerminal
    lT1 = []
    for gtc8 in range(len(lT_ID1) + 1):
        try:
            lT1 += [cursorObj.execute(
                "SELECT * FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({0})".format(
                    str(lT_ID1[gtc8]))).fetchone()]
        except:
            continue
    print(lT1, '- lT1')
    #   ---- Составление списка ID Терминалов в конце линии
    lT = []
    for gtc9 in range(len(lT1) + 1):
        try:
            lT += [lT1[gtc9][1]]
        except:
            continue
    print('lT:', lT)
    pl_elem.line = line
    pl_elem.lineList = lineList
    pl_elem.lT1 = lT1
    print()
    # #   ---- Отсеивание терминалов в начале линии (не пригодилось)
    # lT = []
    # # Part 1
    # for lt in range(len(lT1)):
    #     lT2 = lT1[lt]
    #     print(lT2)
    #     i += 1
    #     try:
    #         if lT2[1] == lT1[i][1]:
    #             lT += [lT2[1]]
    #     except:
    #         continue
    #
    # print(lT, '- lT')
    # # Part 2
    # lTList = []
    # mti = 0
    # for mt in lT:
    #     if mt == lT1[mti][1]:
    #         lTList += [lT1[mti]]
    #         mti += 1
    #     else:
    #         mt1 = mti
    #         while mt != lT1[mt1][1]:
    #             mt1 += 1
    #         lTList += [lT1[mt1]]
    # print(lTList, '- lTList')
def get_coordinates(k, cursorObj, b, i, j, line, lT1, lineList):
    global node_x, node_y, trans_x, trans_y, load_x, load_y
    #   ---- ---- ДАННЫЕ
    oldNodeStart_x = b[i - 1][0][11]
    oldNodeStart_y = b[i - 1][0][12]
    oldNodeEnd_x = b[i - 1][0][13]
    oldNodeEnd_y = b[i - 1][0][14]

    #   ---- Условие для верного определения начала и конца узла (Начало меньше, чем конец)
    nodeX1 = oldNodeStart_x
    nodeY1 = oldNodeStart_y
    nodeX2 = oldNodeEnd_x
    nodeY2 = oldNodeEnd_y
    if nodeX1 > nodeX2:
        oldNodeStart_x = nodeX2
        oldNodeEnd_x = nodeX1
    if nodeY1 > nodeY2:
        oldNodeStart_y = nodeY2
        oldNodeEnd_y = nodeY1
    print('nodes coords:', round(oldNodeEnd_y, 6), round(oldNodeEnd_x, 6), round(oldNodeStart_y, 6), round(oldNodeStart_x, 6), '- y2, x2, y1, x1')

    #   ---- Параметры центра линии
    line_x = cursorObj.execute(
        "SELECT SymCenterX FROM GraphicElement WHERE GraphicElement_ID IN  ({0})".format(
            str(line[i - 1]))).fetchone()
    line_y = cursorObj.execute(
        "SELECT SymCenterY FROM GraphicElement WHERE GraphicElement_ID IN ({0})".format(
            str(line[i - 1]))).fetchone()
    line_x = line_x[0]
    line_y = line_y[0]
    print('line_x and line_y: ', round(line_x, 6), round(line_y, 6))
    #   ---- Параметры координат терминала конца линии
    oldTerminal_x = cursorObj.execute(
        "SELECT PosX FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({0})".format(
            str(lT1[i - 1][0]))).fetchone()
    oldTerminal_y = cursorObj.execute(
        "SELECT PosY FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({0})".format(
            str(lT1[i - 1][0]))).fetchone()
    oldTerminal_y = oldTerminal_y[0]
    oldTerminal_x = oldTerminal_x[0] #Это тут, потому что координаты сохраняются почему-то не как числа, а как кортеж
    #   ---- ---- УСЛОВИЕ
    try:
        if vniz == '1':
            try:
                buchlePoint = cursorObj.execute(
                    "SELECT * FROM GraphicBuchlePoint WHERE GraphicTerminal_ID IN ({0})".format(
                        str(lineList[i - 1][0]))).fetchall()
                buchlePoint_y = buchlePoint[i - 1][4]
                buchlePoint_x = buchlePoint[i - 1][3]
                print(round(buchlePoint_x, 6), round(buchlePoint_y, 6), '- buchlePoint`s coords')
                if round(oldNodeStart_x, 6) == round(oldNodeEnd_x, 6) and round(oldNodeStart_y, 6) != round(oldNodeEnd_y, 6):
                    if buchlePoint_y > oldTerminal_y:
                        #   ---- Вниз
                        print('Вниз')
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y - 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y - 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y - 0.013, 4)
                    elif buchlePoint_y < oldTerminal_y:
                        #   ---- Вверх
                        print('Вверх')
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y + 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y + 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y + 0.013, 4)
                elif round(oldNodeStart_y, 6) == round(oldNodeEnd_y, 6) and round(oldNodeStart_x, 6) != round(oldNodeEnd_x, 6):
                    if buchlePoint_x < oldTerminal_x:
                        #   ---- Вправо
                        print('Вправо')
                        trans_x = round(oldNodeEnd_x + 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x + 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x + 0.013, 4)
                        load_y = trans_y
                    elif buchlePoint_x > oldTerminal_x:
                        #   ---- Влево
                        print('Влево')
                        trans_x = round(oldNodeEnd_x - 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x - 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x - 0.013, 4)
                        load_y = trans_y
            except:
                print(round(oldTerminal_x, 6), round(oldTerminal_y, 6), '- oldTerminal`s coords')
                if round(oldNodeStart_y, 6) == round(oldNodeEnd_y, 6) and round(oldNodeStart_x, 6) != round(oldNodeEnd_x, 6):
                    if line_y > oldTerminal_y:
                        #   ---- Вниз
                        print('Вниз')
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y - 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y - 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y - 0.013, 4)
                    elif line_y < oldTerminal_y:
                        #   ---- Вверх
                        print('Вверх')
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y + 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y + 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y + 0.013, 4)
                elif round(oldNodeStart_x, 6) == round(oldNodeEnd_x, 6) and round(oldNodeStart_y, 6) != round(oldNodeEnd_y, 6):
                    if line_x < oldTerminal_x:
                        #   ---- Вправо
                        print('Вправо')
                        trans_x = round(oldNodeEnd_x + 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x + 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x + 0.013, 4)
                        load_y = trans_y
                    elif line_x > oldTerminal_x:
                        #   ---- Влево
                        print('Влево')
                        trans_x = round(oldNodeEnd_x - 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x - 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x - 0.013, 4)
                        load_y = trans_y
        else:
            print('Ручной выбор направления: Вниз')
            trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
            trans_y = round(oldNodeEnd_y - 0.0075, 4)
            node_x = trans_x
            node_y = round(oldNodeEnd_y - 0.011, 4)
            load_x = trans_x
            load_y = round(oldNodeEnd_y - 0.013, 4)
    except:
        print('exc')
        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
        trans_y = round(oldNodeEnd_y - 0.0075, 4)
        node_x = trans_x
        node_y = round(oldNodeEnd_y - 0.011, 4)
        load_x = trans_x
        load_y = round(oldNodeEnd_y - 0.013, 4)
    print('j:', j, ';  k:', k)
    print('Координаты trans_x, trans_y, node_x, node_y, load_x, load_y:', trans_x, trans_y, node_x, node_y, load_x, load_y)
    print()

    pl_tr.node_x = node_x
    pl_tr.node_y = node_y
    pl_tr.trans_x = trans_x
    pl_tr.trans_y = trans_y
    pl_load.node_x = node_x
    pl_load.node_y = node_y
    pl_load.load_x = load_x
    pl_load.load_y = load_y