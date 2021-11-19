# import sqlite3
# import test3
#
# path_db = 'database.db'
#
# con = sqlite3.connect(path_db)
# cursorObj = con.cursor()
# a = cursorObj.execute(
#     "SELECT * FROM Node WHERE Name NOT LIKE '%ПС%' AND Name NOT LIKE '%N%'AND Name NOT LIKE 'РП%' AND Name NOT LIKE '0%' AND Name NOT LIKE '1%' AND Name NOT LIKE '2%' AND Name NOT LIKE '3%' AND Name NOT LIKE '4%' AND Name NOT LIKE '5%' AND Name NOT LIKE '6%' AND Name NOT LIKE '7%' AND Name NOT LIKE '8%' AND Name NOT LIKE '9%'").fetchall()
# test3.cursorObj = cursorObj
# test3.test3()

# a = [3, 4, 4, 10]
# d = []
# for i in range(len(a)):
#     print(i, 'i')
#     b = a[i]
#     c = a.count(b)
#     print(c, 'c')
#     if c == 1:
#         d += [b]
# print(d)

# line = [3, 10]
# line1 = [[1, 3, 4, 4],[1, 4, 4, 4],[1, 4, 4, 4],[1, 10, 4, 4]]
# lineList = []
# mi = 0
# for m in line:
#     if m == line1[mi][1]:
#         lineList += [line1[mi]]
#         mi += 1
#     else:
#         m1 = mi
#         while m != line1[m1][1]:
#             m1 += 1
#         lineList += [line1[m1]]
# print(lineList)


# for i in range(10):
#     i = 5
#     break
# print(i)

k = 0.1230220010002
print(round(k, 9))
