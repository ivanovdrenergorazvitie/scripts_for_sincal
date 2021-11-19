import sqlite3

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

"""
ПРИ НЕОБХОДИМОСТИ НУЖНО ВЕРНУТЬ ПОЛЬЗОВАТЕЛЬСКИЙ ВВОД ВАРИАНТА СХЕМЫ
"""
# userVariantID = int(input('Ввведите вариант схемы (' + str(fullvariantID)+ '): '))
userVariantID = 3


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
print('Парядок вариантов: ' + str(variantID) + ';')

AreaID0 = cursorObj.execute("SELECT GraphicArea_ID FROM GraphicAreaTile").fetchall()
AreaID0 = name_changer(AreaID0)
AreaID = AreaID0[1:]
ParentAreaID = AreaID0[:1]
print('Список видов: ' + str(AreaID) + '; Вид исходника: ' + str(ParentAreaID))

for i1 in range(len(AreaID)):

    GTerminalID = cursorObj.execute(
        "SELECT GraphicTerminal_ID FROM GraphicAddTerminal WHERE GraphicArea_ID IN ({0})".format(
            str(AreaID[i1]))).fetchall()
    GTerminalID = name_changer(GTerminalID)

    for i2 in range(len(GTerminalID)):
        # if GTerminalID[i2] == 13664:
        #     input('point')
        ff7 = 0
        # Этот флаг нужен, чтобы пропускать проблемные преды, но, возможно, проблема решилась после того, как я добавил
        # поиск по вариантам на p_nam
        TerminalID = cursorObj.execute(
            "SELECT Terminal_ID FROM GraphicTerminal WHERE GraphicTerminal_ID IN ({0}) AND GraphicArea_ID IN ({1})".format(
                str(GTerminalID[i2]), str(AreaID[i1]))).fetchone()[0]


        for var1 in variantID:
            ProtLocID = cursorObj.execute(
                "SELECT ProtLoc_ID FROM ProtLocation WHERE Terminal_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(TerminalID), str(var1))).fetchone()
            if ProtLocID is not None:
                ProtLocID = ProtLocID[0]
                break
            if ProtLocID is None and var1 == 1:
                ff7 = 1
        if ff7 == 1:
            continue

        ff7 = 0
        for var2 in variantID:
            p_nam = cursorObj.execute(
                "SELECT p_nam FROM ProtOCSetting WHERE ProtLoc_ID IN ({0}) AND Variant_ID IN ({1})".format(
                    str(ProtLocID), str(var2))).fetchone()
            if p_nam is not None:
                p_nam = p_nam[0]
                break
            if p_nam is None and var2 == 1:
                ff7 = 1

        if ff7 == 1:
            continue

        if p_nam[:3] == 'ПКТ':
            PNominal = ((p_nam.split('('))[-1]).split(')')[0]
            try:
                PNominal = PNominal.split(' ')[0]
            except:
                print('Без Ампеража', PNominal)
            if PNominal == '5':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='1262987' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('5', PNominal)
            elif PNominal == '8':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='7059389' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('8', PNominal)
            elif PNominal == '10':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='2330219' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('10', PNominal)
            elif PNominal == '16':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='8721863' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('16', PNominal)
            elif PNominal == '20':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='7504122' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('20', PNominal)
            elif PNominal == '31':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='10156544' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('31', PNominal)
            elif PNominal == '40':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='11186976' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('40', PNominal)
            elif PNominal == '50':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='8388736' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('50', PNominal)
            elif PNominal == '80':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='15128749' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('80', PNominal)
            elif PNominal == '100':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='2263842' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('100', PNominal)
            elif PNominal == '160':
                cursorObj.execute("UPDATE GraphicAddTerminal SET FrgndColor='13495295' "
                                  "WHERE GraphicTerminal_ID IN ({0}) AND GraphicType_ID='1' AND GraphicArea_ID IN ({1})".format(
                                        str(GTerminalID[i2]), AreaID[i1]))
                print('160', PNominal)

con.commit()
con.close()