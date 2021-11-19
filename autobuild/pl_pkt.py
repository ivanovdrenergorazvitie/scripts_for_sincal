import sqlite3
trans = []
tr_index = 0
pkt = []
cursorObj = 'simple text'
i = 0
Max_GraphicText_ID = 0
Max_Terminal_ID = 0
Max_ProtSet_ID = 0
Max_ProtLoc_ID = 0
Max_ProtPickup_ID = 0
Max_GraphicAddTerminal_ID = 0

def pl_pkt():

    #   ---- ---- ВВОД ПАРАМЕТРОВ
    #   ---- Выбор предохранителя
    try:
        if int(trans[tr_index].split('-')[1]) == 6:
            pktV = 6
            if int(pkt[tr_index]) == 2:
                pktI = 2
                pktchar = 3450
            elif int(pkt[tr_index]) == 3:
                pktI = 3
                pktchar = 3449
            elif int(pkt[tr_index]) >= 4 and int(pkt[tr_index]) <= 6:
                pktI = 5
                pktchar = 3448
            elif int(pkt[tr_index]) >= 7 and int(pkt[tr_index]) <= 8:
                pktI = 8
                pktchar = 3445
            elif int(pkt[tr_index]) >= 9 and int(pkt[tr_index]) <= 12:
                pktI = 10
                pktchar = 3429
            elif int(pkt[tr_index]) >= 13 and int(pkt[tr_index]) <= 17:
                pktI = 16
                pktchar = 3430
            elif int(pkt[tr_index]) >= 18 and int(pkt[tr_index]) <= 24:
                pktI = 20
                pktchar = 3431
            elif int(pkt[tr_index]) >= 25 and int(pkt[tr_index]) <= 34:
                pktI = 31
                pktchar = 3432
            elif int(pkt[tr_index]) >= 35 and int(pkt[tr_index]) <= 44:
                pktI = 40
                pktchar = 3433
            elif int(pkt[tr_index]) >= 45 and int(pkt[tr_index]) <= 59:
                pktI = 50
                pktchar = 3434
            elif int(pkt[tr_index]) >= 60 and int(pkt[tr_index]) <= 87:
                pktI = 80
                pktchar = 3435
            elif int(pkt[tr_index]) >= 88 and int(pkt[tr_index]) <= 115:
                pktI = 100
                pktchar = 3436
            else:
                pktI = 160
                pktchar = 3467
        else:
            pktV = 10
            if int(pkt[tr_index]) == 2:
                pktI = 2
                pktchar = 3454
            elif int(pkt[tr_index]) == 3:
                pktI = 3
                pktchar = 3453
            elif int(pkt[tr_index]) >= 4 and int(pkt[tr_index]) <= 6:
                pktI = 5
                pktchar = 3452
            elif int(pkt[tr_index]) >= 7 and int(pkt[tr_index]) <= 8:
                pktI = 8
                pktchar = 3451
            elif int(pkt[tr_index]) >= 9 and int(pkt[tr_index]) <= 12:
                pktI = 10
                pktchar = 3437
            elif int(pkt[tr_index]) >= 13 and int(pkt[tr_index]) <= 17:
                pktI = 16
                pktchar = 3438
            elif int(pkt[tr_index]) >= 18 and int(pkt[tr_index]) <= 24:
                pktI = 20
                pktchar = 3439
            elif int(pkt[tr_index]) >= 25 and int(pkt[tr_index]) <= 34:
                pktI = 31
                pktchar = 3440
            elif int(pkt[tr_index]) >= 35 and int(pkt[tr_index]) <= 44:
                pktI = 40
                pktchar = 3441
            elif int(pkt[tr_index]) >= 45 and int(pkt[tr_index]) <= 59:
                pktI = 50
                pktchar = 3442
            elif int(pkt[tr_index]) >= 60 and int(pkt[tr_index]) <= 87:
                pktI = 80
                pktchar = 3443
            elif int(pkt[tr_index]) >= 88 and int(pkt[tr_index]) <= 115:
                pktI = 100
                pktchar = 3444
            else:
                pktI = 160
                pktchar = 3455
        #   ---- Ввод параметров предохранителя в таблицу
        cursorObj.execute(
            "INSERT INTO ProtOCSetting VALUES ({0}, {1}, {2}, {2}, {3}, {3}, 0.0, 1.8, 0.0, 0.0, 0.0, {4}, 0, 135.0, 315.0, -45.0, 135.0, 1, 0.0, 0.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 4, 0, 0.0, 4)".format(
                str(Max_ProtSet_ID + i), str(Max_ProtLoc_ID + i), str(pktchar),
                str("'ПКТ-" + str(pktV) + " (" + str(pktI) + ")'"), str(pktI)))
    except:

        cursorObj.execute(
            "INSERT INTO ProtOCSetting VALUES ({0}, {1}, 0, 0, :null, :null, 0.0, 1.8, 0.0, 0.0, 0.0, 0.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0.0, 0.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 4, 0, 0.0, 4)".format(
                str(Max_ProtSet_ID + i), str(Max_ProtLoc_ID + i)), {'null': None})
        print('Предохранитель не из библиотеки')

    #   ---- Ввод данных в таблицы с параметрами предохранителей
    cursorObj.execute(
        "INSERT INTO ProtPickup VALUES ({0}, {1}, 2, 0, 0, 0.0, 0, 0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 1, 1, 0.0, 90.0, 0.0, 90.0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)".format(
            str(Max_ProtPickup_ID + i), str(Max_ProtLoc_ID + i)))
    cursorObj.execute(
        "INSERT or IGNORE INTO ProtMinMax VALUES ({0}, {1}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)".format(
            str(Max_ProtSet_ID + i), str(Max_ProtLoc_ID + i)))
    cursorObj.execute(
        "INSERT INTO ProtLocation VALUES ({0}, 0, 0, {1}, 0, 1, :null, 1, 0, 0, 0, 0, 0, 0, 0.0, 1, 1, 2, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 135.0, -45.0, 315.0, 135.0, 1, 135.0, -45.0, 315.0, 135.0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0, :null, 0.0, 0, 0, 0, 0, 0, :null, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0)".format(
            str(Max_ProtLoc_ID + i), str(Max_Terminal_ID + 3 * i)), {'null': None})

    #   ---- ---- ИЗОБРАЖЕНИЕ
    #   ---- Изображение текста
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 8 * i - 6)))
    #   ---- Изображение предохранителя
    cursorObj.execute(
        "INSERT INTO GraphicAddTerminal VALUES ({0}, {1}, 1, 1, {2}, 0, -1, 0, 1, 25, 1, 4, 0, 0.0, 0.0, 292, 4, 2, 86, 1, 0, 10.0, 1, 1)".format(
            str(Max_GraphicAddTerminal_ID + i), str(Max_Terminal_ID + 3 * i), str(Max_GraphicText_ID + 8 * i - 6)))

