i = 0
cursorObj = 0

def test3():
    print(i)
    print('test3')
    a = cursorObj.execute(
        "SELECT * FROM Node WHERE Name NOT LIKE '%ПС%' AND Name NOT LIKE '%N%'AND Name NOT LIKE 'РП%' AND Name NOT LIKE '0%' AND Name NOT LIKE '1%' AND Name NOT LIKE '2%' AND Name NOT LIKE '3%' AND Name NOT LIKE '4%' AND Name NOT LIKE '5%' AND Name NOT LIKE '6%' AND Name NOT LIKE '7%' AND Name NOT LIKE '8%' AND Name NOT LIKE '9%'").fetchall()
    print(a)
