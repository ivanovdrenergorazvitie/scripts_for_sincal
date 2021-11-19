import sqlite3
import csv
import pyodbc
import pandas as pd

import get_coordinates
import pl_elem
# import global_value
# import global_i
import pl_tr
import pl_pkt
import pl_load
path_db = 'database.db'

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

con = sqlite3.connect(path_db)
cursorObj = con.cursor()
a = cursorObj.execute(
    "SELECT * FROM Node WHERE Name NOT LIKE '%ПС%' AND Name NOT LIKE '%N%'AND Name NOT LIKE 'РП%' AND Name NOT LIKE '0%' AND Name NOT LIKE '1%' AND Name NOT LIKE '2%' AND Name NOT LIKE '3%' AND Name NOT LIKE '4%' AND Name NOT LIKE '5%' AND Name NOT LIKE '6%' AND Name NOT LIKE '7%' AND Name NOT LIKE '8%' AND Name NOT LIKE '9%'").fetchall()
b = []

# nodeStartX = 0
# nodeStartY = 0
# nodeEndX = 0
# nodeEndY = 0
for i in range(len(a)):
    b.append(cursorObj.execute("SELECT * FROM GraphicNode WHERE Node_ID IN ({0})".format(str(a[i][0]))).fetchall())
    # get all graphic node from node with name like 'ТП'
print(b)
# b = cursorObj.execute("SELECT * FROM GraphicNode WHERE Node_ID IN ({0})".format(cursorObj.execute("SELECT Node_ID FROM Node WHERE Name LIKE 'ТП%'").fetchall())).fetchall()
in_data = pd.read_csv('inpkt.csv', sep=';')
node = list(in_data['node'])
trans = list(in_data['trans'])
tr_s = list(in_data['tr_s'])
sn = list(in_data['sn'])
pkt = list(in_data['pkt'])

# prot = list(in_data['prot'])
# number = list(in_data['number'])

# conn = pyodbc.connect(
#     r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\user\Desktop\Денис\pySincall\baza\baza.mdb;')

conn = pyodbc.connect(
      r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\student22\Desktop\Ильнур\baza.mdb;')
cursor = conn.cursor()

# print(len(a))
# for i in len(a):
#     if a[i][4].split()[-1] == 'СШ': pass
#     else: de
# print(a[0][4].split()[0])
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

Max_GraphicAddTerminal_ID = cursorObj.execute("SELECT MAX(GraphicAddTerminal_ID) FROM GraphicAddTerminal").fetchall()[0][
        0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
Max_GraphicAddTerminal_ID = 1 if str(Max_GraphicAddTerminal_ID) == 'None' else Max_GraphicAddTerminal_ID

Max_Node_ID = cursorObj.execute("SELECT MAX(Node_ID) FROM Node").fetchall()[0][
    0]  # это запрос на самый большой Node_ID в Node
# Max_GraphicText_ID = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchall()[0][
#     0]  # это запрос на самый большой GraphicText_ID в GraphicText
Max_Terminal_ID = cursorObj.execute("SELECT MAX(Terminal_ID) FROM Terminal").fetchall()[0][
    0]  # это запрос на самый большой Terminal_ID в Terminal
Max_Element_ID = cursorObj.execute("SELECT MAX(Element_ID) FROM Element").fetchall()[0][
    0]  # это запрос на самый большой Element_ID в Element
print(Max_Element_ID, Max_Terminal_ID, Max_Node_ID)


number_of_err = 0
number_yzlov = 0
vniz = 2
while int(vniz) > 1:
    vniz = input('Введите направление для трансов, вниз - 0, автоматически - 1:')

spisok_yzlov_bez_transov = []
# spisok_yzlov_bez_ishodnyh_dannyh = []

get_coordinates.get_coordinates_value(b, cursorObj)
global_value()
print('Число узлов:', len(a) + 1)
for i in range(1, len(a) + 1):
    print('ТП' + str(i))
    global_i()
    # print(a[i - 1][4])
    u = pl_elem.pl_elem()
    if u != 0:
        spisok_yzlov_bez_transov.append(a[i - 1][4])
        number_of_err += 1
    number_yzlov += 1

print('Всего узлов ' + str(number_yzlov))
print('Необработано узлов ' + str(number_of_err))


with open('узлы не обработанные скриптом.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for item in spisok_yzlov_bez_transov:
        csv_writer.writerow([item])
# with open('узлы без исходных данных.csv', 'w', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     for item in spisok_yzlov_bez_ishodnyh_dannyh:
#         csv_writer.writerow([item])


con.commit()  # подтверждаем изменения в БД
con.close()