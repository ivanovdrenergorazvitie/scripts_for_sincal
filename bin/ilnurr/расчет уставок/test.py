import sqlite3


#   ---- Перевод кортежей в строки или списки
def name_changer(b):
    a = []
    for i in range(len(b)):
        if len(b[i]) == 1:  # *
            a.append(b[i][0])
        else:  # *
            a.append(list(b[i]))  # *
    return a


"""
Обращение к базе данных SQLite
"""

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()
"""
Выбор варианта
"""
print('\n\n----+-Список вариантов-+----')
var_to_print = list(cursorObj.execute("SELECT Variant_ID, Name FROM Variant").fetchall())
for v in var_to_print:
    print(v[0], '----------------', v[1])

fullvariantID = cursorObj.execute(
    "SELECT Variant_ID FROM Variant").fetchall()
variantID0 = name_changer(fullvariantID)

userVariantID = int(input('\nВведите вариант схемы ' + str(variantID0) + ': '))
variantID = []
variantID1 = userVariantID

if userVariantID != 1:
    while variantID1 != 0:
        variantID += [variantID1]
        parentVariantID = cursorObj.execute(
            "SELECT ParentVariant_ID FROM Variant WHERE Variant_ID IN ({0})".format(
                str(variantID1))).fetchall()
        parentVariantID = name_changer(parentVariantID)
        parentVariantID = parentVariantID[0]
        variantID1 = parentVariantID
else:
    variantID = [1]
print('Последовательность вариантов:', variantID)

netwGroup = name_changer(cursorObj.execute("SELECT Group_ID FROM NetworkGroup").fetchall())
nameGroup = name_changer(cursorObj.execute("SELECT Name, Group_ID FROM NetworkGroup").fetchall())
netwZone = name_changer(cursorObj.execute("SELECT Zone_ID FROM NetworkZone").fetchall())
nameZone = name_changer(cursorObj.execute("SELECT Name, Zone_ID FROM NetworkZone").fetchall())
print('\n\n----+--------Список подстанций--------+----')
for nz in netwZone:
    infElementID = []
    for v in variantID:
        infElementID = cursorObj.execute(
            f"SELECT Element_ID, Variant_ID FROM Element WHERE Variant_ID IN ({v}) "
            f"AND Zone_ID IN ({nz}) AND Type='Infeeder' AND Flag_Variant='1'").fetchall()
        if infElementID == []:
            continue
        else:
            infElementID = name_changer(infElementID)
            break
    print(nz, '--+-' if len(str(nz)) == 1 else '-+-', next(x[0] for x in nameZone if x[1] == nz),
          '-' * (30 - len(next(x[0] for x in nameZone if x[1] == nz))) + '+-', infElementID)

print('\n\n----+-------Список фидеров-------+----')
privyazka = dict()
for ng in netwGroup:
    for v in variantID:
        grInZone = cursorObj.execute(f"SELECT Zone_ID, Name FROM Element WHERE Group_ID IN ({ng}) "
                                     f"AND Variant_ID IN ({v}) AND Flag_Variant='1' AND Group_ID!='1'").fetchone()
        if grInZone is None:
            continue
        else:
            grinz_ID = grInZone[0]
            grinzName = grInZone[1]
            break
    if grInZone != 0 and grInZone != None:
        print(ng, '--+-' if len(str(ng)) == 1 else '-+-', next(x[0] for x in nameGroup if x[1] == ng),
              '-' * (20 - len(next(x[0] for x in nameGroup if x[1] == ng))), grinz_ID,
              '--+-' if len(str(grinz_ID)) == 1 else '-+-', grinzName)
        if grinz_ID in privyazka.keys():
            privyazka[grinz_ID] += [ng]
        else:
            privyazka[grinz_ID] = [ng]

# print(next(
#     list(privyazka.items())[x][0] for x in range(len(list(privyazka.items()))) if 6 in list(privyazka.items())[x][1]))
PSbusbars_Zone = []
PSbusbars_ID = []
PSbusbars = []
for v in variantID:
    PSbusbars_ID = list(set(PSbusbars_ID).union(set(name_changer(cursorObj.execute(f"SELECT Node_ID FROM Node"
                                                                                    f" WHERE Variant_ID IN ({v}) AND "
                                                                                    f"Name LIKE 'ПС%'").fetchall()))))


fiederbaza = dict()
for i in PSbusbars_ID:
    for v in variantID:
        startLine = cursorObj.execute(f"SELECT Element_ID FROM Terminal "
                                      f"WHERE Node_ID IN ({i}) AND Variant_ID IN ({v})").fetchall()
        if startLine == []:
            continue
        else:
            startLine = name_changer(startLine)
            break
    for k in startLine:
        for v in variantID:
            groupID = cursorObj.execute(f"SELECT Group_ID FROM Element "
                                        f"WHERE Element_ID IN ({k}) AND Variant_ID IN ({v})").fetchone()
            if groupID is None:
                continue
            else:
                groupID = groupID[0]
                fiederbaza[groupID] = k
                break
print(fiederbaza)