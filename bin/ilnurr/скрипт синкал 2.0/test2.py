import test3
i = 0
def test2():
    print(i)
    print('test2')
    test3.i = i
    test3.test3()
    k()
    return i
def k():
    global i
    i += 1


