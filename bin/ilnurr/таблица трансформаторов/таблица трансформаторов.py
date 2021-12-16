import sqlite3
import pyodbc
import pandas as pd
import xlsxwriter

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\Users\student22\Desktop\scripts_for_sincal\bin\ilnurr\таблица трансформаторов\baza.mdb;')
cursor = conn.cursor()

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('Ввведите вариант схемы ' + str(variantID0) + ': '))
variantID = []
variantID1 = userVariantID

if userVariantID != 1:
    while variantID1 != 0:
        variantID += [variantID1]
        print(variantID)
        parentVariantID = cursorObj.execute(
            "SELECT ParentVariant_ID FROM Variant WHERE Variant_ID IN ({0})".format(
                str(variantID1))).fetchall()
        parentVariantID = name_changer(parentVariantID)
        parentVariantID = parentVariantID[0]
        variantID1 = parentVariantID
else:
    variantID = [1]

typID = cursorObj.execute(f"SELECT Typ_ID FROM TwoWindingTransformer").fetchall()
typID = name_changer(typID)
typID = sorted(list(set(typID)))
print(typID)
tr_for_db = []
for i in range(len(typID)):
    if i == 0 or i == 32:
        continue
    tr_for_db += [cursor.execute(
        f"select Element_ID, TwotTyp from StdTwoWindingTransformer where Element_ID in ({typID[i]})").fetchone()]
    for k in range(len(tr_for_db)):
        tr_for_db[k][1] = tr_for_db[k][1].replace(' ', '')
print('Число трансов:', len(tr_for_db), '\n', tr_for_db)

transID = []
transIDz = []
for var in variantID:
    transID0 = cursorObj.execute(
        f"SELECT Element_ID, Typ_ID, Un1, Sn, uk FROM TwoWindingTransformer WHERE Variant_ID IN ({var})").fetchall()
    transID = sorted(list(set(transID).union(set(transID0))))
print(transID, '\n Количество до:', len(transID))
for i in range(len(transID)):
    nametrans = cursorObj.execute(f"SELECT Name FROM Element WHERE Element_ID IN ({transID[i][0]})").fetchone()
    transID[i] += nametrans
i = 0
while i < len(transID):
    transtrans = cursorObj.execute(f"SELECT Element_ID FROM Element WHERE Name IN ('{transID[i][5]}')").fetchall()
    for k in range(len(transtrans)):
        if transtrans[k][0] > transID[i][0]:
            del transID[i]
        else:
            i += 1

print('Чистый список: ', transID, '\n Количество после:', len(transID))

error_el = []
for i in range(len(transID)):
    voltlevelID = cursorObj.execute(
        f"SELECT Element_ID, VoltLevel_ID FROM Element WHERE Element_ID IN ({transID[i][0]})").fetchone()
    if voltlevelID[1] == 1 and transID[i][2] == 10.0:
        continue
    elif voltlevelID[1] == 2 and transID[i][2] == 6.0:
        continue
    else:
        error_el += [transID[i][0], transID[i][1]]
print('Список ошибок:', error_el)
names = [['ТП', 'Тип', 'Un', 'Sn', 'z']]
for i in range(len(transID)):
    transID[i] = list(transID[i])
    #transID[i][1] = next(tr_for_db[x][1] for x in range(len(tr_for_db)) if list(tr_for_db)[x][0] == transID[i][1])
    for x in range(len(tr_for_db)):
        tr_for_db = list(tr_for_db)
        if tr_for_db[x][0] == transID[i][1]:
            transID[i][0] = transID[i][5].split(' ')[0]
            transID[i][1] = tr_for_db[x][1]
            transID[i][4] = str(round(((transID[i][4] * transID[i][2] ** 2)/(transID[i][3] * 100)) / 33, 4)) + ' + j' + str(round((transID[i][4] * transID[i][2] ** 2)/(transID[i][3] * 100), 4))
            del transID[i][5]
names += transID
print(names)
with xlsxwriter.Workbook('таблица трансформаторов.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(names):
        worksheet.write_row(row_num, 0, data)
print(transID)
