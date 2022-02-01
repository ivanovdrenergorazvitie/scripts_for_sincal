x = [1, 2, 3]
print(id(x))
print(id([1, 2, 3]))
y = x
print(type(id(x)))



































# n = int(input('Введите число n: '))
# a = []
# for i in range(n):
#     a += [[]]
#     for j in range(n):
#         a[i] += ['x']
#     print(a[i])
# l = 0
# startR = 0
# endR = 0
# nn = 0
# povorot = 0
# while povorot < 2 * n:
#     for i in range(n - endR - startR):
#         l += 1
#         a[0][i + startR] = l
#     # for i in range(n):
#     #     for j in range(n):
#     #         b = a[n - 1 - j][i]
#     #         a[i][j] = a[n - 1 - j][i]
#     #         c = a[n - 1 - j][i - 1 - j]
#     #         a[n - 1 - j][i] = a[n - 1 - j][i - 1 - j]
#     rotated = tuple(zip(a[::-1]))
#     povorot += 1
#     if povorot % 4 == 1:
#         startR += 1
#     if povorot % 4 == 3:
#         startR += 1
# print(a)
