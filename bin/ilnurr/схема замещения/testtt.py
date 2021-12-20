uwu = []
def h():
    uwu.append('s')
    print(12)
    uwu.append('s')
def f():
  g(h)
  uwu.append('s')
def g(a):
  a()
  uwu.append('s')
uwu.append('s')
g(f)

print(uwu)