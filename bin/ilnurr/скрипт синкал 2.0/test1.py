i = 1
import test2
test2.i = i
for i in range(1, 10):
    print(i)
    print('test1')
    a = test2.test2()
    i += a