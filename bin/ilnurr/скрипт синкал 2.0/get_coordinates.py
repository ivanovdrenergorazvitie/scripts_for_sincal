vniz = 0
trans_x = 0.0
trans_y = 0.0
node_x = 0.0
node_y = 0.0
load_x = 0.0
load_y = 0.0

import pl_tr
import pl_load
import pl_elem


def get_coordinates_value(b, cursorObj, i):
    lineID = cursorObj.execute(f"SELECT Element_ID FROM Terminal WHERE Node_ID IN ({b[i - 1][0][5]}) "
                               f"AND Flag_Variant = '1'").fetchone()[0]
    lineID = cursorObj.execute(f"SELECT Element_ID FROM Element "
                               f"WHERE Element_ID IN ({lineID}) "
                               f"AND Flag_Variant = '1' AND Type = 'Line'").fetchone()[0]
    terminalID = cursorObj.execute(f"SELECT Terminal_ID FROM Terminal "
                                   f"WHERE Element_ID IN ({lineID})"
                                   f"AND Flag_Variant = '1' AND Node_ID IN ({b[i - 1][0][5]})").fetchone()[0]
    gterminalID = cursorObj.execute(f"SELECT GraphicTerminal_ID FROM GraphicTerminal "
                                    f"WHERE Terminal_ID IN ({terminalID})"
                                    f"AND Flag_Variant = '1'").fetchone()[0]
    try:
        flag_for_coords = True
        bpID = cursorObj.execute(
            f"SELECT * FROM GraphicBucklePoint "
            f"WHERE GraphicTerminal_ID IN ({gterminalID}) "
            f"AND Flag_Variant = '1'").fetchall()
        line_y = bpID[i - 1][4]
        line_x = bpID[i - 1][3]
        print(round(line_x, 6), round(line_y, 6), '- buchlePoint`s coords')
    except:
        flag_for_coords = False
        #   ---- Параметры центра линии
        gelementID = cursorObj.execute(f"SELECT GraphicElement_ID FROM GraphicElement WHERE Element_ID IN ({lineID})"
                                    f"AND Flag_Variant = '1'").fetchone()[0]
        centerID = cursorObj.execute(
            f"SELECT SymCenterX, SymCenterY FROM GraphicElement WHERE GraphicElement_ID IN ({gelementID})").fetchone()
        line_x = centerID[0]
        line_y = centerID[1]
        print('line_x and line_y: ', round(line_x, 6), round(line_y, 6))
    #   ---- Параметры координат терминала конца линии
    oldTerminalID = cursorObj.execute(
        f"SELECT PosX, PosY FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({str(gterminalID)})").fetchone()
    oldTerminal_x = oldTerminalID[0]
    oldTerminal_y = oldTerminalID[1]

    return flag_for_coords, oldTerminal_x, oldTerminal_y, line_x, line_y


def get_coordinates(k, cursorObj, b, i, j):
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
    print('nodes coords:', round(oldNodeEnd_y, 6), round(oldNodeEnd_x, 6), round(oldNodeStart_y, 6),
          round(oldNodeStart_x, 6), '- y2, x2, y1, x1')
    flag_for_coords, oldTerminal_x, oldTerminal_y, line_x, line_y = get_coordinates_value(b, cursorObj, i)
    #   ---- ---- УСЛОВИЕ
    try:
        if vniz == '1':
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