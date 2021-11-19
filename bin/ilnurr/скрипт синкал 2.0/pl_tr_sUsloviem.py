node = []
tr_s = []
trans = []
i = 0
b = 0
cursorObj = 'simple text'
import pyodbc
import pl_tr
import get_coordinatesОригинал
import sqlite3
import csv
import pandas as pd

def pl_tr_sUsloviem(a):
    #   ---- Проверка на наличие узла с одним трансформатором
    term_id_for_pkt = []
    try:
        tr_index = node.index(a[i - 1][4])
        #   ---- Для узла с одним трансформатором
        tr_for_db = cursor.execute('select * from StdTwoWindingTransformer where TwotTyp in ({0})'.format(
            str("'" + str(trans[tr_index]).split('-')[0] + '-' + str(
                tr_s[tr_index]) + '/' +
                trans[tr_index].split('-')[1] + "'"))).fetchone()
        #   ---- Условие корректного названия
        if tr_s[node.index(a[i - 1][4])].find('x') == -1 and tr_s[node.index(a[i - 1][4])].find(
                '+') == -1 and isinstance(tr_for_db, pyodbc.Row) and a[i - 1][4].find('П') == -1:

            get_coordinatesОригинал.get_coordinates(2, cursorObj, b, i)
            pl_tr.pl_tr()

        else:
            spisok_yzlov_bez_transov.append(a[i - 1][4])
    except:
        #   ---- Проверка на наличие узла с двумя трансформаторами
        try:
            a[i - 1][4] = a[i - 1][4] + ' Т1'
            spisok_yzlov_s_dvumya_transormatorami.append(node[node.index(a[i - 1][4])])
            tr_index = node.index(a[i - 1][4])


            #   ---- Для Т1
            if node.index(a[i - 1][4].find('T1') > 0:
                tr_for_db = cursor.execute('select * from StdTwoWindingTransformer where TwotTyp in ({0})'.format(
                    str("'" + str(trans[tr_index]).split('-')[0] + '-' + str(
                        tr_s[tr_index]) + '/' +
                        trans[tr_index].split('-')[1] + "'"))).fetchone()
                #   ---- Условие корректного названия
                if tr_s[node.index(a[i - 1][4])].find('x') == -1 and tr_s[node.index(a[i - 1][4])].find(
                        '+') == -1 and isinstance(tr_for_db, pyodbc.Row) and a[i - 1][4].find('П') == -1:

                    get_coordinatesОригинал.get_coordinates(1, cursorObj, b, i)
                    pl_tr.pl_tr()

                    a[i - 1][4].replace('Т1', 'Т2')
                else:
                    spisok_yzlov_bez_transov.append(a[i - 1][4])
            #   ---- Для Т2
            if node.index(a[i - 1][4].find('T2')) > 0:
                tr_for_db = cursor.execute('select * from StdTwoWindingTransformer where TwotTyp in ({0})'.format(
                    str("'" + str(trans[tr_index]).split('-')[0] + '-' + str(
                        tr_s[tr_index]) + '/' +
                        trans[tr_index].split('-')[1] + "'"))).fetchone()
                #   ---- Условие корректного названия
                if tr_s[node.index(a[i - 1][4])].find('x') == -1 and tr_s[node.index(a[i - 1][4])].find(
                        '+') == -1 and isinstance(tr_for_db, pyodbc.Row) and a[i - 1][4].find('П') == -1:

                    get_coordinatesОригинал.get_coordinates(3, cursorObj, b, i)
                    pl_tr.pl_tr()

                else:
                    spisok_yzlov_bez_transov.append(a[i - 1][4])
        except:
            #   ---- Узел без трансформатора
            number_of_err += 1
            spisok_yzlov_bez_transov.append(a[i - 1][4])
    pl_tr.pl_tr()
