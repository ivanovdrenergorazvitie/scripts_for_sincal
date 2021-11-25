"""
СКРИПТ ДЛЯ КОРРЕКТИРОВКИ СХЕМЫ ЗАМЕЩЕНИЯ.
Используется после создания схемы замещения.
"""
import sqlite3
import ec

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a

def varID(var, flag):
    global elementID
    if flag == 1:
        elementID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Variant_ID IN ({0})".format(str(var))).fetchall()
        elementID0 = name_changer(elementID0)
        elementID = sorted(list(set(elementID).union(set(elementID0))))

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

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

ksize = float(input('Коэффициент увеличения схемы (В процентах): '))/100

elementID = []
for i in variantID:
    varID(i, 1)

nodeID = cursorObj.execute(
    "SELECT Node_ID FROM GraphicNode WHERE NodeStartX!=NodeEndX OR NodeStartY!=NodeEndY").fetchall()
nodeID = name_changer(nodeID)
print(nodeID)

# ec.nodes_texts.cursorObj = cursorObj
# ec.nodes_texts.variantID = variantID
ec.nodes_texts(nodeID, cursorObj, variantID)     # Расстановка узлов
# ec.centrovka(elementID, cursorObj, variantID)          # Центровка символов элемента
# ec.size(ksize, cursorObj, variantID)                # Увеличение схемы

input('SAVE')
con.commit()
con.close()

