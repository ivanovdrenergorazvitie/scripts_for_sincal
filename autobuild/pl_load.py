import sqlite3
VoltLevel_ID = 0
Max_Element_ID = 0
Max_Node_ID = 0
Max_Terminal_ID = 0
Max_GraphicText_ID = 0
Max_GraphicElement_ID = 0
Max_GraphicTerminal_ID = 0
node_x = 0.0
node_y = 0.0
load_x = 0.0
load_y = 0.0
i = 0
a = []
sn = []
node = []
cursorObj = 'simple text'
k = 0
tr_index = 0
def pl_load(k, j):

    #   ---- ---- ВВОД ПАРАМЕТРОВ
    #   ---- Ввод параметров нагрузки в таблицу элементов
    try:
        cursorObj.execute(
            "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'Load', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                str(Max_Element_ID + 2 * i - 1), str(VoltLevel_ID[0][0]),
                "'" + str(
                    a[i - 1][4].split()[0] + ' Н-' + str(a[i - 1][4].split()[1].split('С')[0])) + "'"),
            {'null': None})
    except:
        if j == 2:
            cursorObj.execute(
                "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'Load', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                    str(Max_Element_ID + 2 * i - 1), str(VoltLevel_ID[0][0]),
                    "'" + str(a[i - 1][4].split()[0] + ' Н') + "'"), {'null': None})
        else:
            cursorObj.execute(
                "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'Load', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                    str(Max_Element_ID + 2 * i - 1), str(VoltLevel_ID[0][0]),
                    "'" + str(a[i - 1][4].split()[0] + ' Н' + str(k)) + "'"), {'null': None})
    #   ---- Ввод параметров нагрузки
    #   ---- Условие замены запятой на точку в столбце sn
    if str(sn[tr_index]) != 'nan':
        xl = str(float(sn[tr_index].replace(',', '.')) / 1000)
    else:
        xl = 0.005
    cursorObj.execute(
        "INSERT INTO Load VALUES ({0}, 0, 1, 2, 3, 0.0, 0.0, 100.0, 0.0, {1}, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1, 0, 0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1.0, 0.0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 1, 0.0, 0.75, 0, 0, 0, 1, 1, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0.0, 0.0, 0.0, 0.0)".format(
            str(Max_Element_ID + 2 * i - 1), str(xl)))

    #   ---- Ввод параметров терминала нагрузки
    cursorObj.execute(
        "INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 1, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
            str(Max_Terminal_ID + 3 * i - 2), str(Max_Element_ID + 2 * i - 1), str(Max_Node_ID + i)))

    #   ---- ---- ИЗОБРАЖЕНИЕ

    #   ---- Текст нагрузки
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 4)))
    cursorObj.execute(
    #   ---- Текст терминала нагрузки
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 2)))

    #   ---- Изображение терминала нагрузки
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3},{4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_GraphicTerminal_ID + 3 * i - 2), str(Max_GraphicElement_ID + 2 * i - 1),
            str(Max_GraphicText_ID + 8 * i - 2), str(Max_Terminal_ID + 3 * i - 2),
            str(node_x), str(node_y)))
    #   ---- Изображение элемента нагрузки
    cursorObj.execute(
        "INSERT INTO GraphicElement VALUES ({0}, 1, 1, {1}, 0,{2}, 1, 0, -1, 0, 1, 30, {3},{4}, 13, 0, 0, 1, 1, 1, 0)".format(
            str(Max_GraphicElement_ID + 2 * i - 1), str(Max_GraphicText_ID + 8 * i - 4),
            str(Max_Element_ID + 2 * i - 1), str(load_x), str(load_y)))
