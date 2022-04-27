import sqlite3
node = []
spisok_yzlov_bez_ishodnyh_dannyh = []
a = []
i = 0
cursorObj = 'simple text'
VoltLevel_ID = []
node_x = 0.0
node_y = 0.0
trans_x = 0.0
trans_y = 0.0
cursor = 'simple text'
tr_s = []
trans = []
Max_Element_ID = 0
Max_Node_ID = 0
Max_Terminal_ID = 0
Max_GraphicText_ID = 0
Max_GraphicTerminal_ID = 0
Max_GraphicElement_ID = 0
Max_GraphicNode_ID = 0
def pl_tr(k, j):

    #   ---- ---- ВВОД ПАРАМЕТРОВ
    #   ---- Ввод параметров трансформатора в таблицу трансформаторов

    try:
        tr_index = node.index(a[i - 1][4])
    except:
        tr_index = node.index(a[i - 1][4] + ' Т' + str(k))
    tr_for_db = cursor.execute('select * from StdTwoWindingTransformer where TwotTyp in ({0})'.format(
        str("'" + str(trans[tr_index]).split('-')[0] + '-' + str(
            tr_s[tr_index]) + '/' +
            trans[tr_index].split('-')[1] + "'"))).fetchone()
    try:
        cursorObj.execute(
            "INSERT INTO TwoWindingTransformer VALUES ({0}, {1}, 1, {2}, 0.4, {3}, 0.0, {4}, 0.0, {5}, {6}, 1.1, 0.0, 0.0, 100.0, 0.9, 59, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0, 103.0, 98.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 3, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0, 16.0, 0.0, 0, 0, 2, 0.0, 0.0, 0.0, 0, 0.0, 0.1, 0.05, 0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 8, 0, 0, 1, 0, 0)".format(
                str(Max_Element_ID + 2 * i), str(tr_for_db.Element_ID), str(tr_for_db.Un1),
                str(tr_for_db.Sn),
                str(tr_for_db.uk), str(tr_for_db.Vfe), str(tr_for_db.i0)))
    except:
        spisok_yzlov_bez_ishodnyh_dannyh.append(a[i - 1][4])
        cursorObj.execute(
            "INSERT INTO TwoWindingTransformer VALUES ({0}, 0, 1, {1}, 0.4, 0.0001, 0.0, 8.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 100.0, 0.9, 59, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0, 103.0, 98.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 3, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0, 16.0, 0.0, 0, 0, 2, 0.0, 0.0, 0.0, 0, 0.0, 0.1, 0.05, 0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 8, 0, 0, 1, 0, 0)".format(
                str(Max_Element_ID + 2 * i), str(a[i - 1][6])))  # a[i - 1][6]
    #   ---- Ввод параметров трансформатора в таблицу элементов
    try:
        cursorObj.execute(
            "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'TwoWindingTransformer', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                str(Max_Element_ID + 2 * i), str(a[i - 1][3]),
                "'" + str(
                    a[i - 1][4].split()[0] + ' Т-' + str(a[i - 1][4].split()[1].split('С')[0])) + "'"),
            {'null': None})
    except:
        if j == 2:
            cursorObj.execute(
                "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'TwoWindingTransformer', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                    str(Max_Element_ID + 2 * i), str(a[i - 1][3]),
                    "'" + str(a[i - 1][4].split()[0] + ' Т') + "'"),
                {'null': None})
        else:
            cursorObj.execute(
                "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'TwoWindingTransformer', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
                    str(Max_Element_ID + 2 * i), str(a[i - 1][3]),
                    "'" + str(a[i - 1][4].split()[0] + ' Т' + str(k)) + "'"),
                {'null': None})
    #   ---- Ввод параметров узла в таблицу узлов
    try:
        cursorObj.execute(
            "INSERT INTO Node VALUES ({0}, 1, 1, {1}, {2}, :null, 0.4, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, '', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0, 7, 0, 2, 0.0, 0.0, :null, 0.0, 0)".format(
                str(Max_Node_ID + i), str(VoltLevel_ID[0][0]),
                "'" + str(
                    a[i - 1][4].split()[0] + ' Н-' + str(a[i - 1][4].split()[1].split('С')[0])) + "'"),
            {'null': None})
    except:
         if j == 2:
            cursorObj.execute(
                "INSERT INTO Node VALUES ({0}, 1, 1, {1}, {2}, :null, 0.4, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, '', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0, 7, 0, 2, 0.0, 0.0, :null, 0.0, 0)".format(
                    str(Max_Node_ID + i), str(VoltLevel_ID[0][0]),
                    "'" + str(a[i - 1][4].split()[0] + ' Н') + "'"),
                {'null': None})
         else:
            cursorObj.execute(
                "INSERT INTO Node VALUES ({0}, 1, 1, {1}, {2}, :null, 0.4, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, '', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0, 7, 0, 2, 0.0, 0.0, :null, 0.0, 0)".format(
                    str(Max_Node_ID + i), str(VoltLevel_ID[0][0]),
                    "'" + str(a[i - 1][4].split()[0] + ' Н' + str(k)) + "'"),
                {'null': None})

    #   ---- Ввод параметров терминала
    #   ---- Терминал конца трансформатора
    cursorObj.execute(
        "INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 2, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
            str(Max_Terminal_ID + 3 * i - 1), str(Max_Element_ID + 2 * i), str(Max_Node_ID + i)))
    #   ---- Терминал начала трансформатора
    cursorObj.execute(
        "INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 1, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
            str(Max_Terminal_ID + 3 * i), str(Max_Element_ID + 2 * i), str(a[i - 1][0])))

    #   ---- ---- ГРАФИЧЕСКИЕ ДАННЫЕ

    #   ---- Изображение текста
    #   ---- Текст узла
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 5)))
    #   ---- Текст трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 3)))
    #   ---- Текст терминала конца трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 1)))
    #   ---- Текст терминала начала трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i)))

    #   ---- Изображение схемы
    #   ---- Изображение терминала конца трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3},{4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_GraphicTerminal_ID + 3 * i - 1), str(Max_GraphicElement_ID + 2 * i),
            str(Max_GraphicText_ID + 8 * i - 1), str(Max_Terminal_ID + 3 * i - 1),
            str(node_x), str(node_y)))
    #   ---- Изображение терминала начала трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3},{4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_GraphicTerminal_ID + 3 * i), str(Max_GraphicElement_ID + 2 * i),
            str(Max_GraphicText_ID + 8 * i),
            str(Max_Terminal_ID + 3 * i),
            str(node_x), str(node_y)))
    #   ---- Изображение трансформатора
    cursorObj.execute(
        "INSERT INTO GraphicElement VALUES ({0}, 1, 1, {1}, 0,{2}, 16781825, 0, -1, 0, 1, 30, {3},{4}, 20, 0, 0, 1, 1, 1, 0)".format(
            str(Max_GraphicElement_ID + 2 * i), str(Max_GraphicText_ID + 8 * i - 3),
            str(Max_Element_ID + 2 * i),
            str(trans_x), str(trans_y)))
    #   ---- Изображение узла нагрузки
    cursorObj.execute(
        "INSERT INTO GraphicNode VALUES ({0}, 1, 1, {1}, 0, {2}, 0, -1, 0, 1, 0, {3}, {4}, {5}, {6}, 0, 0, 1, 1, 1)".format(
            str(Max_GraphicNode_ID + i), str(Max_GraphicText_ID + 8 * i - 5), str(Max_Node_ID + i),
            str(node_x), str(node_y),
            str(node_x), str(node_y)))