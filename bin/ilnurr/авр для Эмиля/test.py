import sqlite3
path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()
def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a
el = cursorObj.execute("SELECT Name FROM Node WHERE VoltLevel_ID='2'").fetchall()
el = name_changer(el)
print(el)
x = 0
while x < len(el):

    ff = el[x].split('-')
    fs = ''
    print(el[x])
    for y in range(len(ff) - 1):
        fs += ff[y]
        fs += '-'
    if ff[-2][-1] == 'Н' or ff[-2][-1] == 'H':

        if ff[-1] == '1':
            fs += '2'
            el.remove(fs)
            el.remove(el[x])
            print(fs)
            x -= 1
            continue
        elif ff[-1] == '2':
            fs += '1'
            el.remove(fs)
            el.remove(el[x])
            print(fs)
            x -= 1
            continue
    x += 1


print(el)
print(len(el))