#ВРЕМЯ
import sqlite3
import pandas as pd

def name_changer(b):
    a = []
    for i in range(len(b)):
        a.append(b[i][0])
    return a


path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()




for t1 in range(len(allProtLastNodeID)):
    if allProtLastNodeID[t1][1][1] == 0:
        continue
    tTerminal = allProtLastNodeID[t1][2]
    nextNodeID = []
    listOfLastNode = []
    lastNodeID = []
    checkedTerminalID = []
    forgottenTerminalID = []
    nextTerminalID = []
    usl1 = True  # False, когда закончатся forgottenTerminalID
    while usl1 == True:
        usl2 = True  # False, когда последняя шина
        while usl2 == True:

    # составляем списки маршрутов к последним реклоузерам, начиная с главной защиты
# на последний реклоузер ставим 0,01
# приплюсовываем к последнему реклоузеру 0,05 с

