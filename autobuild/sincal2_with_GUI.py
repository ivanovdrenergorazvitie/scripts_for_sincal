import sqlite3
import csv
import pyodbc
import pandas as pd

import get_coordinates
import pl_elem
import pl_tr
import pl_pkt
import pl_load
import PySimpleGUI as sg
layout = [
    [sg.Text('Путь к БД(.db) проетка'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('Путь к БД(.mdb) трансформаторов'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('Путь к файлу исходных данных(.csv)'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('Наименование столбцов с данными')],
    [sg.Text('Тип трансформатора (ТМ-6)'), sg.InputText(), sg.Text('Мощность трансформатора, кВА'), sg.InputText(), sg.Checkbox('Автоматическое направление элементов(по умолчанию вниз)')],
    [sg.Text('Узел (ТП)'), sg.InputText(), sg.Text('Номинал предохранителей'), sg.InputText(), sg.Text('Нагрузка, кВА'), sg.InputText()],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('File Compare', layout)

def global_value():
    pl_elem.node = node
    pl_elem.a = a
    pl_elem.b = b
    pl_elem.cursorObj = cursorObj

    pl_elem.Max_Element_ID = Max_Element_ID
    pl_elem.Max_Node_ID = Max_Node_ID
    pl_elem.Max_Terminal_ID = Max_Terminal_ID
    pl_elem.Max_GraphicTerminal_ID = Max_GraphicTerminal_ID
    pl_elem.Max_GraphicText_ID = Max_GraphicText_ID
    pl_elem.Max_GraphicNode_ID = Max_GraphicNode_ID
    pl_elem.Max_GraphicElement_ID = Max_GraphicElement_ID
    pl_elem.Max_ProtSet_ID = Max_ProtSet_ID
    pl_elem.Max_ProtLoc_ID = Max_ProtLoc_ID
    pl_elem.Max_ProtPickup_ID = Max_ProtPickup_ID
    pl_elem.Max_GraphicAddTerminal_ID = Max_GraphicAddTerminal_ID

    get_coordinates.vniz = vniz

    pl_tr.a = a
    pl_tr.cursor = cursor
    pl_tr.cursorObj = cursorObj
    pl_tr.trans = trans
    pl_tr.node = node
    pl_tr.tr_s = tr_s
    pl_tr.sn = sn
    pl_tr.VoltLevel_ID = VoltLevel_ID
    pl_tr.spisok_yzlov_bez_ishodnyh_dannyh = spisok_yzlov_bez_ishodnyh_dannyh

    pl_pkt.cursorObj = cursorObj
    pl_pkt.trans = trans
    pl_pkt.pkt = pkt

    pl_load.a = a
    pl_load.sn = sn
    pl_load.node = node
    pl_load.cursorObj = cursorObj
    pl_load.VoltLevel_ID = VoltLevel_ID

    pl_elem.Max_Element_ID = Max_Element_ID
    pl_elem.Max_Node_ID = Max_Node_ID
    pl_elem.Max_Terminal_ID = Max_Terminal_ID
    pl_elem.Max_GraphicNode_ID = Max_GraphicNode_ID
    pl_elem.Max_GraphicTerminal_ID = Max_GraphicTerminal_ID
    pl_elem.Max_GraphicText_ID = Max_GraphicText_ID
    pl_elem.Max_GraphicElement_ID = Max_GraphicElement_ID
    pl_elem.Max_ProtSet_ID = Max_ProtSet_ID
    pl_elem.Max_ProtLoc_ID = Max_ProtLoc_ID
    pl_elem.Max_ProtPickup_ID = Max_ProtPickup_ID
    pl_elem.Max_GraphicAddTerminal_ID = Max_GraphicAddTerminal_ID

def global_i():
    pl_elem.i = i
    get_coordinates.i = i
    pl_tr.i = i
    pl_pkt.i = i
    pl_load.i = i

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event in ('Submit'):
        path_db = re.findall('.+:\/.+\.+.', values[0])
        path_mdb = re.findall('.+:\/.+\.+.', values[1])
        in_data = re.findall('.+:\/.+\.+.', values[2])
        trans = values[3]
        tr_s = values[4]
        vniz = values[5]
        if vniz: vniz = 1
        else: vniz = 0
        node = values[6]
        pkt = values[7]
        sn = values[8]
        con = sqlite3.connect(path_db)
        cursorObj = con.cursor()
        a = cursorObj.execute(
            "SELECT * FROM Node WHERE Name NOT LIKE '%ПС%' AND Name NOT LIKE '%N%'AND Name NOT LIKE 'РП%' AND Name NOT LIKE '0%' AND Name NOT LIKE '1%' AND Name NOT LIKE '2%' AND Name NOT LIKE '3%' AND Name NOT LIKE '4%' AND Name NOT LIKE '5%' AND Name NOT LIKE '6%' AND Name NOT LIKE '7%' AND Name NOT LIKE '8%' AND Name NOT LIKE '9%'").fetchall()
        b = []

        for i in range(len(a)):
            b.append(
                cursorObj.execute("SELECT * FROM GraphicNode WHERE Node_ID IN ({0})".format(str(a[i][0]))).fetchall())

        in_data = pd.read_csv(in_data, sep=';')
        node = list(in_data[node])
        trans = list(in_data[trans])
        tr_s = list(in_data[tr_s])
        sn = list(in_data[sn])
        pkt = list(in_data[pkt])

        conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb)};DBQ=' + path_mdb + ';')
        cursor = conn.cursor()

        Max_GraphicText_ID = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchall()[0][
            0]  # это запрос на самый большой GraphicText_ID в GraphicText
        Max_GraphicElement_ID = cursorObj.execute("SELECT MAX(GraphicElement_ID) FROM GraphicElement").fetchall()[0][
            0]  # это запрос на самый большой GraphicText_ID в GraphicText
        Max_GraphicNode_ID = cursorObj.execute("SELECT MAX(GraphicNode_ID) FROM GraphicNode").fetchall()[0][
            0]  # это запрос на самый большой GraphicText_ID в GraphicText
        Max_GraphicTerminal_ID = cursorObj.execute("SELECT MAX(GraphicTerminal_ID) FROM GraphicTerminal").fetchall()[0][
            0]  # это запрос на самый большой GraphicText_ID в GraphicText

        VoltLevel_ID = cursorObj.execute("SELECT VoltLevel_ID FROM VoltageLevel WHERE Name LIKE '0,4 кВ'").fetchall()

        Max_VoltageTran_ID = cursorObj.execute("SELECT MAX(VoltageTran_ID) FROM VoltageTransformer").fetchall()[0][
            0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
        Max_VoltageTran_ID = 1 if str(Max_VoltageTran_ID) == 'None' else Max_VoltageTran_ID

        Max_ProtPickup_ID = cursorObj.execute("SELECT MAX(ProtPickup_ID) FROM ProtPickup").fetchall()[0][
            0]  # это запрос на самый большой ProtPickup_ID в ProtPickup
        Max_ProtPickup_ID = 1 if str(Max_ProtPickup_ID) == 'None' else Max_ProtPickup_ID

        Max_ProtSet_ID = cursorObj.execute("SELECT MAX(ProtSet_ID) FROM ProtOCSetting").fetchall()[0][
            0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
        Max_ProtSet_ID = 1 if str(Max_ProtSet_ID) == 'None' else Max_ProtSet_ID

        Max_ProtLoc_ID = cursorObj.execute("SELECT MAX(ProtLoc_ID) FROM ProtLocation").fetchall()[0][
            0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
        Max_ProtLoc_ID = 1 if str(Max_ProtLoc_ID) == 'None' else Max_ProtLoc_ID

        Max_GraphicAddTerminal_ID = \
        cursorObj.execute("SELECT MAX(GraphicAddTerminal_ID) FROM GraphicAddTerminal").fetchall()[0][
            0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
        Max_GraphicAddTerminal_ID = 1 if str(Max_GraphicAddTerminal_ID) == 'None' else Max_GraphicAddTerminal_ID

        Max_Node_ID = cursorObj.execute("SELECT MAX(Node_ID) FROM Node").fetchall()[0][
            0]  # это запрос на самый большой Node_ID в Node
        Max_Terminal_ID = cursorObj.execute("SELECT MAX(Terminal_ID) FROM Terminal").fetchall()[0][
            0]  # это запрос на самый большой Terminal_ID в Terminal
        Max_Element_ID = cursorObj.execute("SELECT MAX(Element_ID) FROM Element").fetchall()[0][
            0]  # это запрос на самый большой Element_ID в Element

        number_of_err = 0
        number_yzlov = 0
        spisok_yzlov_bez_transov = []
        spisok_yzlov_bez_ishodnyh_dannyh = []

        get_coordinates.get_coordinates_value(b, cursorObj)
        global_value()

        for i in range(1, len(a) + 1):
            global_i()
            u = pl_elem.pl_elem()
            if u != 0:
                spisok_yzlov_bez_transov.append(a[i - 1][4])
                number_of_err += 1
            number_yzlov += 1

        with open('Узлы(ТП) без новых элементов.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in spisok_yzlov_bez_transov:
                csv_writer.writerow([item])
        with open('Узлы(ТП) без исходных данных.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in spisok_yzlov_bez_ishodnyh_dannyh:
                csv_writer.writerow([item])

        con.commit()  # подтверждаем изменения в БД
        con.close()
        print("Процесс завершен успешно. Измениния сохранены.")

