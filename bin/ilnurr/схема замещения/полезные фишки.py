import os
import shutil
ff = input('Флаг: ')
if ff == '1':
    f = 1
    oldName = input('Название файла, которое нужно переименовать: ')
    Format = input('Формат файла через точку: ')
    while f == 1:
        newName = input('Введите новое имя файла (Enter, чтобы сохранить): ')
        if newName == '':
            f = 0
            break
        file_oldname = os.path.join("c:\\Users\student22\Desktop\Ильнур\схема замещения", oldName + Format)
        file_newname_newfile = os.path.join("c:\\Users\student22\Desktop\Ильнур\схема замещения", newName + Format)
        oldName = newName
        os.rename(file_oldname, file_newname_newfile)
if ff == '2':
    oldbd = input("Введите название (database - ''.db): ")
    shutil.copy(r'database — ' + oldbd + '.db', r'database.db')
