# import xlsxwriter
import sqlite3

# wb = xlsxwriter.Workbook('ав.xlsm')

path_db = 'database.db'
con = sqlite3.connect(path_db)
cursorObj = con.cursor()

nodeID = cursorObj.execute(f"SELECT Node, U FROM QueryResultLFNode WHERE Variant_ID='3'").fetchall()
for i in nodeID:
    print(str(i)[1:-1])