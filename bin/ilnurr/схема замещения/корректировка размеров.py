import sqlite3

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