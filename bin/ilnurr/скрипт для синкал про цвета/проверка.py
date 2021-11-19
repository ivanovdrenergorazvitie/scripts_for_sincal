import sqlite3
import pandas as pd
import openpyxl
def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

#   ---- Формирование списка groupID



#   ---- Формирование списка nodeID

red = 0
green = 0
blue = 0

groupID = 32
nodeID0 = cursorObj.execute(
    "SELECT Node_ID FROM Node WHERE Group_ID IN ({0})".format(
        str(groupID))).fetchall()
nodeID = name_changer(nodeID0)

#   ---- Формирование списка terminalID
for osn2 in range(len(nodeID)):
    terminalID0 = cursorObj.execute(
        "SELECT Terminal_ID FROM Terminal WHERE Node_ID IN ({0})".format(
            str(nodeID[osn2]))).fetchall()
    terminalID = name_changer(terminalID0)
#   ---- Формирование списка  gterminalID
    for osn3 in range(len(terminalID)):
        gterminalID = cursorObj.execute(
        "SELECT GraphicTerminal_ID FROM GraphicTerminal WHERE Terminal_ID IN ({0})".format(
            str(terminalID[osn3]))).fetchone()[0]
        try:
            gaterminalID0 = cursorObj.execute(
                "SELECT FrgndColor FROM GraphicAddTerminal WHERE GraphicTerminal_ID IN ({0})".format(
                    str(gterminalID))). fetchone()[0]
        except:
            continue

        print(terminalID, gaterminalID0)


# red = 0     #'255'
# green = 0   #'65280'
# blue = 0    #'16763904'

        if gaterminalID0 == 255:
            red += 1
        elif gaterminalID0 == 65280:
            green += 1
        elif gaterminalID0 == 16763904:
            blue += 1

        # if osn1 == 0:
        #     osn1 = 'red'
        # elif osn1 == 1:
        #     osn1 = 'green'
        # elif osn1 == 2:
        #     osn1 = 'blue'
list_of_colors = [red, green, blue]
df[groupID0[osn1][1]] = list_of_colors

df.to_excel('количество цветных узлов.xlsx')

# open('sincal_colors.txt', 'w').close()
# txt = open('sincal_colors.txt', 'a')
# txt.write(df.to_string())
# txt.close()

print(df)