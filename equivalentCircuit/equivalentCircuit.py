import sqlite3
import math

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


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

LineID = []
TransID = []
LoadID = []
InfeederID = []
dottedTransID = []
def varID(var, flag):
    global LineID, TransID, LoadID, InfeederID, dottedTransID
    if flag == 1:
        LineID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Type IN ('Line') AND Variant_ID IN ({0})".format(str(var))).fetchall()
        LineID0 = name_changer(LineID0)
        LineID = sorted(list(set(LineID).union(set(LineID0))))

    elif flag == 2:
        TransID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Type IN ('TwoWindingTransformer') AND Variant_ID IN ({0})".format(
                str(var))).fetchall()
        TransID0 = name_changer(TransID0)
        TransID = sorted(list(set(TransID).union(set(TransID0))))

    elif flag == 3:
        LoadID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Type IN ('Load') AND Variant_ID IN ({0})".format(
                str(var))).fetchall()
        LoadID0 = name_changer(LoadID0)
        LoadID = sorted(list(set(LoadID).union(set(LoadID0))))

    elif flag == 4:
        InfeederID0 = cursorObj.execute(
            "SELECT Element_ID FROM Element WHERE Type IN ('Infeeder') AND Variant_ID IN ({0})".format(
                str(var))).fetchall()
        InfeederID0 = name_changer(InfeederID0)
        InfeederID = sorted(list(set(InfeederID).union(set(InfeederID0))))

    elif flag == 5:
        dottedTransID0 = cursorObj.execute(
            "SELECT Element_ID FROM GraphicElement WHERE SymbolDef='16847361' AND Flag_Variant='1'").fetchall()
        dottedTransID0 = name_changer(dottedTransID0)
        dottedTransID = sorted(list(set(dottedTransID).union(set(dottedTransID0))))

# Выбираем Линию
for i in variantID:
    varID(i, 1)
# Выбираем Трансформатор
for i in variantID:
    varID(i, 2)
# Выбираем Нагрузку
for i in variantID:
    varID(i, 3)
# Выбираем Источник
for i in variantID:
    varID(i, 4)
# Выбираем пунктирные трансы
for i in variantID:
    varID(i, 5)

print('Линии:', LineID, '\nТрансформаторы:', TransID, '\nНагрузка:', LoadID, '\nИсточник:', InfeederID, '\nПунктирные трансы:', dottedTransID)

for tr in TransID:
    if tr not in dottedTransID:
        cursorObj.execute("DELETE FROM GraphicElement WHERE Element_ID IN ({0})".format(str(tr)))


for i1 in range(len(TransID)):
    cursorObj.execute("UPDATE GraphicElement SET SymbolDef=({0}) WHERE Element_ID IN ({1})".format(
        '4112', str(TransID[i1]))).fetchall()
    cursorObj.execute("UPDATE GraphicElement SET SymbolType=({0}) WHERE Element_ID IN ({1})".format(
        '27', str(TransID[i1]))).fetchall()
    cursorObj.execute("UPDATE GraphicElement SET SymbolSize=({0}) WHERE Element_ID IN ({1})".format(
        '100', str(TransID[i1])))

for i2 in range(len(LineID)):
    cursorObj.execute("UPDATE GraphicElement SET SymbolDef=({0}) WHERE Element_ID IN ({1})".format(
        '4112', str(LineID[i2]))).fetchall()
    cursorObj.execute("UPDATE GraphicElement SET SymbolType=({0}) WHERE Element_ID IN ({1})".format(
        '27', str(LineID[i2]))).fetchall()
# Поменяли трансы и линии

for i3 in range(len(LoadID)):
    cursorObj.execute("DELETE FROM GraphicElement WHERE Element_ID IN ({0})".format(
        str(LoadID[i3])))
    nLoadID = cursorObj.execute(
        "SELECT Node_ID FROM Terminal WHERE Element_ID IN ({0})".format(str(LoadID[i3]))).fetchall()
    nLoadID = name_changer(nLoadID)
    nLoadID = cursorObj.execute("SELECT Node_ID, Name FROM Node WHERE Node_ID IN ({0})".format(
        str(nLoadID[0]))).fetchall()[0]
    if nLoadID[1].find(' Н-') != -1 or (nLoadID[1] + ' ').find(' Н ') != -1:
        for i4 in range(len(nLoadID)):
            cursorObj.execute("DELETE FROM GraphicNode WHERE Node_ID IN ({0})".format(str(nLoadID[0])))
# Удалили нагрузку



for el1 in range(len(LineID)):
    r = cursorObj.execute("SELECT r FROM Line WHERE Element_ID IN ({0})".format(str(LineID[el1]))).fetchall()
    r = name_changer(r)
    r = r[0]
    l = cursorObj.execute("SELECT l FROM Line WHERE Element_ID IN ({0})".format(str(LineID[el1]))).fetchall()
    l = name_changer(l)
    l = l[0]
    x = cursorObj.execute("SELECT x FROM Line WHERE Element_ID IN ({0})".format(str(LineID[el1]))).fetchall()
    x = name_changer(x)
    x = x[0]
    Formula1 = 'z=' + str(round(r * l, 5)) + '+j' + str(round(x * l, 5))
    # Formula = str(round(math.sqrt((r * l) * (r * l) + (x * l) * (x * l)), 5))
    # Formula1 = Formula1.replace(".", ",")
    if l != 0.0:
        ugolLine = round(math.atan((x * l)/(r * l)) * 57.2958, 2)
    else:
        ugolLine = 'stop'
    if ugolLine != 'stop':
        cursorObj.execute(
            "UPDATE Element SET Name=({0}), Type='SerialRLCCircuit' WHERE Element_ID IN ({1})".format(
                "'" + str(Formula1) + '\n' + str(ugolLine) + '°' + "'", str(LineID[el1])))
    else:
        cursorObj.execute(
            "UPDATE Element SET Name=({0}), Type='SerialRLCCircuit' WHERE Element_ID IN ({1})".format(
                "'" + str(Formula1) + "'", str(LineID[el1])))

    cursorObj.execute("UPDATE Element SET Flag_Input='3' WHERE Element_ID IN ({0})".format(str(LineID[el1])))

    lShortName = cursorObj.execute(
        "SELECT ShortName FROM Element WHERE Element_ID IN ({0})".format(str(LineID[el1]))).fetchone()[0]

    lShortName = 'SERLC' + lShortName[1:]
    cursorObj.execute(
        "UPDATE Element SET ShortName=({0}) WHERE Element_ID IN ({1})".format("'" + str(lShortName) + "'", str(LineID[el1])))


    # RLCVariantID = cursorObj.execute("SELECT Variant_ID FROM ELement WHERE Element_ID IN ({0})".format(LineID[el1])).fetchone()[0]
    # RLCFlagCariant = cursorObj.execute("SELECT Flag_Variant FROM Element WHERE Element_ID IN ({0})".format(LineID[el1])).fetchone()[0]
    # cursorObj.execute(
    #     "INSERT INTO SerialRLCCircuit VALUES ({0}, 2, 1, 10.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1, 1.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 1.0, 0.0, 0.0, 0.0, 0, 0, {1}, {2})".format(str(LineID[el1]), str(RLCFlagCariant), str(RLCVariantID)))
    # cursorObj.execute("UPDATE Line SET Typ_ID='0' WHERE Element_ID IN ({0})".format(str(LineID[el1])))

    cursorObj.execute("UPDATE Line SET LineTyp=''")
    # cursorObj.execute("UPDATE Line SET LineTyp=:null", {'null': None})
# Название Линии

for el2 in range(len(InfeederID)):
    Xmax = cursorObj.execute("SELECT Xmax FROM Infeeder WHERE Element_ID IN ({0})".format(str(InfeederID[el2]))).fetchall()
    Xmax = name_changer(Xmax)
    Xmax = Xmax[0]

    Xmin = cursorObj.execute("SELECT Xmin FROM Infeeder WHERE Element_ID IN ({0})".format(str(InfeederID[el2]))).fetchall()
    Xmin = name_changer(Xmin)
    Xmin = Xmin[0]
    if Xmin == 0:
        cursorObj.execute("UPDATE Element SET Name='' WHERE Element_ID IN ({0})".format(str(InfeederID[el2])))
        # cursorObj.execute("UPDATE Element SET Name=:null WHERE Element_ID IN ({0})".format(str(InfeederID[el2])), {'null': None})
        continue
    Formula2 = 'z=' + str(Xmax) + '/' + str(Xmin) + '=' + str(round(Xmax/Xmin, 5))
    cursorObj.execute(
        "UPDATE Element SET Name=({0}) WHERE Element_ID IN ({1})".format(
            "'" + str(Formula2) + "'", str(InfeederID[el2])))
#Название источника


ElementID = sorted(dottedTransID + LineID)
print('Element_ID:', ElementID)
RLCVariantID = []
for el3 in range(len(ElementID)):
    for var in variantID:
        RLCVariantID0 = cursorObj.execute(
            "SELECT Variant_ID FROM ELement WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
                str(ElementID[el3]), str(var))).fetchall()
        if RLCVariantID0 == []:
            continue
        RLCVariantID = name_changer(RLCVariantID0)
        RLCVariantID = RLCVariantID[0]

        break
    RLCFlagVariant = cursorObj.execute(
        "SELECT Flag_Variant FROM Element WHERE Element_ID IN ({0}) AND Variant_ID IN ({1})".format(
            str(ElementID[el3]), str(RLCVariantID))).fetchone()[0]
    cursorObj.execute(
        "INSERT INTO SerialRLCCircuit VALUES ({0}, 2, 1, 10.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1, 1.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 1.0, 0.0, 0.0, 0.0, 0, 0, {1}, {2})".format(str(ElementID[el3]), str(RLCFlagVariant), str(RLCVariantID)))


for el3 in range(len(TransID)):
    uk = cursorObj.execute("SELECT uk FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
        str(TransID[el3]))).fetchall()
    uk = name_changer(uk)
    print(uk)
    uk = uk[0]

    Un1 = cursorObj.execute("SELECT Un1 FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
        str(TransID[el3]))).fetchall()
    Un1 = name_changer(Un1)
    Un1 = Un1[0]

    Sn = cursorObj.execute("SELECT Sn FROM TwoWindingTransformer WHERE Element_ID IN ({0})".format(
        str(TransID[el3]))).fetchall()
    Sn = name_changer(Sn)
    Sn = Sn[0]
    if Sn == 0:
        continue
    Formula3 = 'z=' + str(round(uk * Un1 * Un1 / (Sn * 100.0), 5))
    cursorObj.execute(
        "UPDATE Element SET Name=({0}) WHERE Element_ID IN ({1})".format(
            "'" + str(Formula3) + '\n88,26°' + "'", str(TransID[el3])))

cursorObj.execute("DELETE FROM TwoWindingTransformer")
cursorObj.execute("DELETE FROM Line")

cpGTerminalID = cursorObj.execute(
    "SELECT GraphicTerminal_ID FROM GraphicAddTerminal WHERE SymType='4' AND SymState='0'").fetchall()
cpGTerminalID = name_changer(cpGTerminalID)
print('Терминалы с разомкнутыми выключателями:', cpGTerminalID)

if cpGTerminalID == []:

    cursorObj.execute("DELETE FROM GraphicAddTerminal")
    cursorObj.execute("DELETE FROM ProtOCSetting")
    cursorObj.execute("DELETE FROM ProtPickup")
    cursorObj.execute("DELETE FROM ProtMinMax")
    cursorObj.execute("DELETE FROM ProtLocation")
    cursorObj.execute("DELETE FROM Breaker")
else:
    for i4 in range(len(cpGTerminalID)):
        cursorObj.execute("DELETE FROM GraphicAddTerminal WHERE GraphicTerminal_ID NOT LIKE ({0})".format(
            cpGTerminalID[i4]))
        cursorObj.execute("DELETE FROM ProtOCSetting")
        cursorObj.execute("DELETE FROM ProtPickup")
        cursorObj.execute("DELETE FROM ProtMinMax")
        cursorObj.execute("DELETE FROM ProtLocation")
        cursorObj.execute("DELETE FROM Breaker")
# Удалили защиты и преды

con.commit()  # подтверждаем изменения в БД
con.close()
