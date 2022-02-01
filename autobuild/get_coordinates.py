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
    #   ---- Составление списка параметров Терминала выбранных узлов
    line0 = []
    for gtc2 in range(len(nodeForCoords) + 1):
        try:
            line0 += [cursorObj.execute(
                "SELECT * FROM Terminal WHERE Node_ID IN ({0})".format(
                    str(nodeForCoords[gtc2]))).fetchall()]
        except:
            continue
    #   ---- Вывод из тройного списка: line0[[(), ()], [(), ()], [()]] -> line1[(), (), (), (), ()]
    line1 = []
    for gtc3i in range(len(line0) + 1):
        try:
            for gtc3j in range(len(line0[gtc3i]) + 1):
                line1 += [line0[gtc3i][gtc3j]]
                print(gtc3i, gtc3j, '- line1 checking')
        except:
            continue
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
    #   ---- Определение терминалов конца линии
    lT_ID1 = []
    for gtc7 in range(len(lineList) + 1):
        try:
            lT_ID1 += [lineList[gtc7][0]]
        except:
            continue
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
    #   ---- Составление списка ID Терминалов в конце линии
    lT = []
    for gtc9 in range(len(lT1) + 1):
        try:
            lT += [lT1[gtc9][1]]
        except:
            continue
    pl_elem.line = line
    pl_elem.lineList = lineList
    pl_elem.lT1 = lT1

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

    #   ---- Параметры центра линии
    line_x = cursorObj.execute(
        "SELECT SymCenterX FROM GraphicElement WHERE GraphicElement_ID IN  ({0})".format(
            str(line[i - 1]))).fetchone()
    line_y = cursorObj.execute(
        "SELECT SymCenterY FROM GraphicElement WHERE GraphicElement_ID IN ({0})".format(
            str(line[i - 1]))).fetchone()
    line_x = line_x[0]
    line_y = line_y[0]
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
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y - 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y - 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y - 0.013, 4)
                    elif buchlePoint_y < oldTerminal_y:
                        #   ---- Вверх
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y + 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y + 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y + 0.013, 4)
                elif round(oldNodeStart_y, 6) == round(oldNodeEnd_y, 6) and round(oldNodeStart_x, 6) != round(oldNodeEnd_x, 6):
                    if buchlePoint_x < oldTerminal_x:
                        #   ---- Вправо
                        trans_x = round(oldNodeEnd_x + 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x + 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x + 0.013, 4)
                        load_y = trans_y
                    elif buchlePoint_x > oldTerminal_x:
                        #   ---- Влево
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
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y - 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y - 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y - 0.013, 4)
                    elif line_y < oldTerminal_y:
                        #   ---- Вверх
                        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                        trans_y = round(oldNodeEnd_y + 0.0075, 4)
                        node_x = trans_x
                        node_y = round(oldNodeEnd_y + 0.011, 4)
                        load_x = trans_x
                        load_y = round(oldNodeEnd_y + 0.013, 4)
                elif round(oldNodeStart_x, 6) == round(oldNodeEnd_x, 6) and round(oldNodeStart_y, 6) != round(oldNodeEnd_y, 6):
                    if line_x < oldTerminal_x:
                        #   ---- Вправо
                        trans_x = round(oldNodeEnd_x + 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x + 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x + 0.013, 4)
                        load_y = trans_y
                    elif line_x > oldTerminal_x:
                        #   ---- Влево
                        trans_x = round(oldNodeEnd_x - 0.0075, 4)
                        trans_y = round(oldNodeStart_y + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                        node_x = round(oldNodeEnd_x - 0.011, 4)
                        node_y = trans_y
                        load_x = round(oldNodeEnd_x - 0.013, 4)
                        load_y = trans_y
        else:
            trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
            trans_y = round(oldNodeEnd_y - 0.0075, 4)
            node_x = trans_x
            node_y = round(oldNodeEnd_y - 0.011, 4)
            load_x = trans_x
            load_y = round(oldNodeEnd_y - 0.013, 4)
    except:
        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
        trans_y = round(oldNodeEnd_y - 0.0075, 4)
        node_x = trans_x
        node_y = round(oldNodeEnd_y - 0.011, 4)
        load_x = trans_x
        load_y = round(oldNodeEnd_y - 0.013, 4)

    pl_tr.node_x = node_x
    pl_tr.node_y = node_y
    pl_tr.trans_x = trans_x
    pl_tr.trans_y = trans_y
    pl_load.node_x = node_x
    pl_load.node_y = node_y
    pl_load.load_x = load_x
    pl_load.load_y = load_y