import PySimpleGUI as sg
import pandas as pd
import sqlite3
import re

def Maximum(path_database):  # получим имена всех шин, а также найдем максимальный Node_ID
    con = sqlite3.connect(path_database)

    cursorObj = con.cursor()
    Max_Node_ID = cursorObj.execute("SELECT MAX(Node_ID) FROM Node").fetchall()[0][
        0]  # это запрос на самый большой Node_ID в Node
    Max_GraphicText_ID = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchall()[0][
        0]  # это запрос на самый большой GraphicText_ID в GraphicText
    Max_Terminal_ID = cursorObj.execute("SELECT MAX(Terminal_ID) FROM Terminal").fetchall()[0][
        0]  # это запрос на самый большой Terminal_ID в Terminal
    Max_Element_ID = cursorObj.execute("SELECT MAX(Element_ID) FROM Element").fetchall()[0][
        0]  # это запрос на самый большой Element_ID в Element

    ProtLoc_ID = cursorObj.execute("SELECT MAX(ProtLoc_ID) FROM ProtLocation").fetchall()[0][0]
    GraphicAddTerminal_ID = \
    cursorObj.execute("SELECT MAX(GraphicAddTerminal_ID) FROM GraphicAddTerminal").fetchall()[0][0]
    ProtPickup_ID = cursorObj.execute("SELECT MAX(ProtPickup_ID) FROM ProtPickup").fetchall()[0][0]
    try:
        ProtSet_ID = cursorObj.execute("SELECT MAX(ProtSet_ID) FROM ProtOCSetting").fetchall()[0][0] + 10
    except:
        ProtSet_ID = 0

    con.close()
    return Max_Element_ID, Max_Node_ID, Max_Terminal_ID, Max_GraphicText_ID, ProtLoc_ID, GraphicAddTerminal_ID, ProtPickup_ID, ProtSet_ID


def place_trans(TP_Sn, Flag_Lf, path_database, Line_Node_ID, Name, ShortName, PosX, PosY, Max_Element_ID, Max_Node_ID,
                Max_Terminal_ID, Max_GraphicText_ID, ProtLock_ID, GraphicAddTerminal_ID, ProtPickup_ID, ProtSet_ID, V):
    con = sqlite3.connect(path_database)
    cursorObj = con.cursor()
    cursorObj.execute(
        "INSERT INTO Element VALUES ({0}, 2, 1, 1, 1, {1}, {2}, 'TwoWindingTransformer', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, 'None', 0.0, 'None', 0.0, 0.0, 0, 0, 0, 0, '', 'None', 1.0, 1.0)".format(
            str(Max_Element_ID + 1), "'" + Convertor.name_convertor(Name, 0) + "'", "'" + ShortName + "'"))
    # cursorObj.execute("INSERT INTO Element VALUES (Element_ID,'2', '1','1', '1','nameTR','ShortNameTR','TwoWindingTransformer','3','1','1','0','0','0.0','0.0','0.0','0.0','NULL','0.0','NULL','0.0','0.0','0','0','0','0','','NULL','1.0','1.0')")#,%Max_Element_ID)
    cursorObj.execute(
        "INSERT INTO Node VALUES ({0}, 1, 1, 1, {1}, {2}, 10.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, '', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 'None', 0.0, 'None', 0.0, 0, 0, 0, 0, 0.0, 0.0, 0, 7, 0, 2, 0.0, 0.0, 'None', 0.0, 0)".format(
            str(Max_Node_ID + 1), "'" + Convertor.name_convertor(Name, 1) + "'", "'" + ShortName + "'"))
    # cursorObj.execute("INSERT INTO Node VALUES (Node_ID,'1','1','2','nameNode','ShortNameNode','10.0','1','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0','1','','1','0','0','0','0','0','0','0','0','0.0','0','0','1','0.0','0.0','0','0','0','0','0.0','0.0','0.0','0.0','NULL','0.0','NULL','0.0','0','0','0','0','0.0','0.0','0','7','0','2','0.0','0.0','NULL','0.0','0')")
    # print(Convertor.name_convertor(Name,0))
    # print("'"+str(ID.get_ID().get(Convertor.name_convertor(Name,0)))+"'")
    cursorObj.execute(
        "INSERT INTO TwoWindingTransformer VALUES ({0}, {1}, 1, 10.0, 10.0, 0.0001, 0.0, 8.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 100.0, 0.9, 6, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0, 103.0, 98.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 3, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0, 16.0, 0.0, 0, 0, 2, 0.0, 0.0, 0.0, 0, 0.0, 0.1, 0.05, 0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 8, 0, 0, 1, 0, 0)".format(
            str(Max_Element_ID + 1), "'" + str(ID.get_ID().get(Convertor.name_convertor(Name, 0))) + "'"))
    # (Element_ID, 0, 0, 10.0, 10.0, 0.0001, 0.0, 8.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 100.0, 0.9, 6, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0, 103.0, 98.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 3, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0, 16.0, 0.0, 0, 0, 2, 0.0, 0.0, 0.0, 0, 0.0, 0.1, 0.05, 0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 8, 0, 0, 1, 0, 0)
    cursorObj.execute("INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 1, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
        str(Max_Terminal_ID + 1), str(Max_Element_ID + 1), str(Line_Node_ID)))
    cursorObj.execute("INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 2, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
        str(Max_Terminal_ID + 2), str(Max_Element_ID + 1), str(Max_Node_ID + 1)))
    # Terminal_ID,Element_ID,Node_ID,'1',Start or end(1 or 2),'1','0.0','0.0','7','1','0','0','1','0')")
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 1)))
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 0, 0, 0, 1, 1, 0.0, -0.00095, -0.00065, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 2)))
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 3, 0, 0, 1, 1, 0.0, -2.75e-05, 0.0075, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 3)))
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 3, 0, 0, 1, 1, 0.0, -2.75e-05, 0.0075, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 4)))
    cursorObj.execute(
        "INSERT INTO GraphicElement VALUES ({0}, 1, 1, {1}, 0,{2}, 16777730, 0, -1, 0, 1, 100, {3},{4}, 20, 0, 0, 1, 1, 1, 0)".format(
            str(Max_Element_ID + 1), str(Max_GraphicText_ID + 1), str(Max_Element_ID + 1), str(PosX[1]), str(PosY[1])))
    # (Graphic_Element_ID, 1, 1,Graphic_text_ID, 0, Element_ID, 16777730, 0, -1, 0, 1, 100, CenterX, CenterY, 20, 0, 0, 1, 1, 1, 0)
    cursorObj.execute(
        "INSERT INTO GraphicNode VALUES ({0}, 1, 1, {1}, 0, {2}, 0, -1, 0, 2, 4, {3}, {4}, {5}, {6}, 0, 0, 1, 1, 1)".format(
            str(Max_Node_ID + 1), str(Max_GraphicText_ID + 2), str(Max_Node_ID + 1), str(PosX[2]), str(PosY[2]),
            str(PosX[2]), str(PosY[2])))
    # (GraphicNode_ID, 1, 1,GraphicText_ID, 0, Node_ID, 0, -1, 0, 2, 4, startX, StartY, EndX, EndY, 0, 0, 1, 1, 1)
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3},{4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_Terminal_ID + 1), str(Max_Element_ID + 1), str(Max_GraphicText_ID + 3), str(Max_Terminal_ID + 1),
            str(PosX[0]), str(PosY[0])))
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3},{4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_Terminal_ID + 2), str(Max_Element_ID + 1), str(Max_GraphicText_ID + 4), str(Max_Terminal_ID + 2),
            str(PosX[2]), str(PosY[2])))
    # Точка присоединения к линии(Graphic_TErminal_ID,GraphicElement_ID,GraphicTExt_ID,Terminal_ID, PosX, PosY, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)

    con.commit()
    con.close()

    path_table_prot = 'D:/aleksey/PythonProjects/Insert Elements/TypeTr.db'
    Sn = ID.get_Sn(Convertor.name_convertor(Name, 0).strip())
    Snprot = Insert_PKT.get_Table_value(Sn, V, path_table_prot)
    Insert_PKT.insert(path_database, ProtSet_ID + 1, ProtLock_ID + 1, Snprot, V)

    con = sqlite3.connect(path_database)
    cursorObj = con.cursor()
    # отрисовка нагрузки
    cursorObj.execute(
        "INSERT INTO Element VALUES ({0}, 1, 1, 1, 1,{1}, {2}, 'Load', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, 'None', 0.0, 'None', 0.0, 0.0, 0, 0, 0, 0, '', 'None', 1.0, 1.0)".format(
            str(Max_Element_ID + 2), "'" + Convertor.name_convertor(Name, 1) + "'", "'" + ShortName + "'"))
    # cursorObj.execute("INSERT INTO Element VALUES (Element_ID,'2', '1','1', '1','nameTR','ShortNameTR','TwoWindingTransformer','3','1','1','0','0','0.0','0.0','0.0','0.0','NULL','0.0','NULL','0.0','0.0','0','0','0','0','','NULL','1.0','1.0')")#,%Max_Element_ID)
    try:
        cursorObj.execute(
            "INSERT INTO Load VALUES ({0}, 0, 1, 2, {1}, 0.0, 0.0, {2}, {3}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1, 0, 0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1.0, 0.0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 1, 0.0, 0.75, 0, 0, 0, 1, 1, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0.0, 0.0, 0.0, 0.0)".format(
                str(Max_Element_ID + 2), str(Flag_Lf), str(Sn), str(Sn)))
    except:
        cursorObj.execute(
            "INSERT INTO Load VALUES ({0}, 0, 1, 2, {1}, 0.0, 0.0, {2}, {3}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1, 0, 0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1.0, 0.0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 1, 0.0, 0.75, 0, 0, 0, 1, 1, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0.0, 0.0, 0.0, 0.0)".format(
                str(Max_Element_ID + 2), str(Flag_Lf), 0, 0))

    cursorObj.execute("INSERT INTO Terminal VALUES 	({0}, {1}, {2}, 1, 1, 1, 0.0, 0.0, 7, 1, 0, 0, 1, 0)".format(
        str(Max_Terminal_ID + 3), str(Max_Element_ID + 2), str(Max_Node_ID + 1)))
    # cursorObj.execute("INSERT INTO Terminal VALUES (Terminal_ID,Element_ID,Node_ID,'1',Start or end(1 or 2),'1','0.0','0.0','7','1','0','0','1','0')")
    cursorObj.execute(
        "INSERT INTO GraphicElement VALUES ({0}, 1, 1, {1}, 0, {2}, 1, 0, -1, 0, 1, 100, {3}, {4}, 13, 0, 0, 1, 1, 1, 0)".format(
            str(Max_Element_ID + 2), str(Max_GraphicText_ID + 5), str(Max_Element_ID + 2), str(PosX[3]), str(PosY[3])))
    # (Graphic_Element_ID, 1, 1,Graphic_text_ID, 0, Element_ID, 16777730, 0, -1, 0, 1, 100, CenterX, CenterY, 20, 0, 0, 1, 1, 1, 0)
    cursorObj.execute(
        "INSERT INTO GraphicTerminal VALUES ({0}, {1}, {2}, {3}, {4}, {5}, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)".format(
            str(Max_Terminal_ID + 3), str(Max_Element_ID + 2), str(Max_GraphicText_ID + 6), str(Max_Terminal_ID + 3),
            str(PosX[2]), str(PosY[2])))
    # Точка присоединения к линии(Graphic_TErminal_ID,GraphicElement_ID,GraphicTExt_ID,Terminal_ID, PosX, PosY, 0, 0, 1, 0, 4, 20.0, 80, -1, 0, 0, 0, 4, 0.4, 0, -1, 0, 0, 292, 0, 1, 1, 1, 0)
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 6, 0, 0, 1, 1, 0.0,0.0, -0.0075,  1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 5)))
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 0, 0, 0, 1, 1, 0.0, -2.75e-05, 0.0075, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 6)))

    # Настройка защиты(предохранителя)

    # GraphicAddTerminal
    cursorObj.execute(
        "INSERT INTO GraphicAddTerminal VALUES ({0}, {1}, 1, 1, {2}, 0, -1, 0, 1, 80, 1, 4, 0, {3}, {4}, 292, 2048, 2, 86, 1, 0, {5}, 1, 1)".format(
            str(GraphicAddTerminal_ID + 1), str(Max_Terminal_ID + 1), str(Max_GraphicText_ID + 7), str(0.0), str(-0.0),
            str(20.0)))
    # (GraphicAddTerminal_ID, GraphicTerminal_ID, 1, 1, GraphicText_ID, 0, -1, 0, 1, 80, 1, 4, 0, PosX, PosY, 292, 2048, 2, 86, 1, 0, SymNodePos(Расстояние до узла), 1, 1)
    # ProtPickup
    cursorObj.execute(
        "INSERT INTO ProtPickup VALUES ({0}, {1}, 2, 0, 0, 0.0, 0, 0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 1, 1, 0.0, 90.0, 0.0, 90.0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)".format(
            str(ProtPickup_ID + 1), str(ProtLock_ID + 1)))
    # (ProtPickup_ID, ProtLock_ID, 2, 0, 0, 0.0, 0, 0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 0, 1.0, 1.0, 1.5, 1.2, 0.7, 1.0, 30.0, 0.0, 1, 1, 0.0, 90.0, 0.0, 90.0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # ProtOCSetting

    # cursorObj.execute("INSERT INTO ProtOCSetting VALUES ({0}, {1}, 2287, 2287,'HH-SE (80 A)','HH-SE (80 A)', 0.0, 1.8, 0.0, 0.0, 0.0, 80.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0.0, 0.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 4, 0, 0.0, 4)".format(str(ProtSet_ID+1),str(ProtLock_ID+1)))
    # #(ProtSet_ID, ProtLock_ID, ProtCharP_ID(2287), ProtCharE_ID(2287), p_nam('HH-SE (80 A)'),e_nam('HH-SE (80 A)'), 0.0, 1.8, 0.0, 0.0, 0.0, 80.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0.0, 0.0, 0, 135.0, 315.0, -45.0, 135.0, 1, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 1, 0.0, 4, 1, 0.0, 1, 0, 0.0, 1, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 4, 0, 0.0, 4)
    # ProtMinMax
    cursorObj.execute(
        "INSERT INTO ProtMinMax VALUES ({0}, {1}, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)".format(
            str(ProtSet_ID + 1), str(ProtLock_ID + 1)))
    # (ProtSet_ID, ProtLock_ID, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
    # ProtLocation
    cursorObj.execute(
        "INSERT INTO ProtLocation VALUES ({0}, 825, 0, {1}, 0, 1, {2}, 1, 0, 0, 0, 0, 0, 0, 0.0, 1, 1, 2, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 135.0, -45.0, 315.0, 135.0, 1, 135.0, -45.0, 315.0, 135.0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0, '', 0.0, 0, 0, 0, 0, 0, 'None', 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0)".format(
            str(ProtLock_ID + 1), str(Max_Terminal_ID + 1), "'" + Convertor.name_convertor(Name, 2) + "'"))
    # (ProtLock_ID, ProtDev_ID(825), 0, Terminal_ID(Трансформатора), Node_ID(0), 1, Name, 1, 0, 0, 0, 0, 0, 0, 0.0, 1, 1, 2, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 135.0, -45.0, 315.0, 135.0, 1, 135.0, -45.0, 315.0, 135.0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0, '', 0.0, 0, 0, 0, 0, 0, None, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0)
    cursorObj.execute(
        "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 9, 0, 0, 0, 1, 0, 0.0, 0.03, -0.015, 1, 0, 0, 1, 1)".format(
            str(Max_GraphicText_ID + 7)))

    con.commit()
    con.close()


def Get_Bus_data(path_database, Line_Node_ID):
    con = sqlite3.connect(path_database)
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT NodeStartX, NodeStartY, NodeEndX FROM GraphicNode WHERE Node_ID='{0}'".format(str(Line_Node_ID)))
    rows = cursorObj.fetchall()
    PosX = (rows[0][0] + rows[0][2]) / 2
    PosY = rows[0][1]
    con.close()
    return PosX, PosY


def Get_Direction(Line_Node_ID, path_database):
    con = sqlite3.connect(path_database)
    cursorObj = con.cursor()
    cursorObj.execute("SELECT Terminal_ID FROM Terminal WHERE Node_ID='{0}'".format(str(Line_Node_ID)))
    Terminal_ID = cursorObj.fetchall()
    if len(Terminal_ID) > 1:
        cursorObj.execute(
            "SELECT PosX,PosY FROM GraphicBucklePoint WHERE GraphicTerminal_ID={0} or GraphicTerminal_ID={1}".format(
                str(Terminal_ID[0][0]), str(Terminal_ID[1][0])))
        position = cursorObj.fetchall()
    else:
        cursorObj.execute(
            "SELECT PosX,PosY FROM GraphicBucklePoint WHERE GraphicTerminal_ID={0}".format(str(Terminal_ID[0][0])))
        position = cursorObj.fetchall()

    if position == []:
        cursorObj.execute("SELECT Element_ID FROM Terminal WHERE Node_ID='{0}'".format(str(Line_Node_ID)))
        Element_ID = cursorObj.fetchall()
        cursorObj.execute(
            "SELECT SymCenterX,SymCenterY FROM GraphicElement WHERE Element_ID='{0}'".format(str(Element_ID[0][0])))
        position = cursorObj.fetchall()
    con.close()
    return position


def place_elements(path_database, TP_Sn, Flag_Lf, V):
    con = sqlite3.connect(path_database)
    cursorObj = con.cursor()
    Node_ID_Name = []
    cursorObj.execute("SELECT  Name, Node_ID  FROM Node")
    rows = cursorObj.fetchall()
    for row in rows:
        Node_ID_Name.append((row[1], row[0]))

    for Node_ID in Node_ID_Name:
        PosX, PosY = [], []
        position = Get_Direction(Node_ID[0], path_database)
        cursorObj.execute(
            "SELECT NodeStartX, NodeStartY, NodeEndX,NodeEndY FROM GraphicNode WHERE Node_ID='{0}'".format(
                str(Node_ID[0])))
        rows = cursorObj.fetchall()
        PosX.append((rows[0][0] + rows[0][2]) / 2)
        PosY.append((rows[0][1] + rows[0][3]) / 2)
        if (rows[0][0] - rows[0][2]) == 0:  # Направление элемента
            if position[0][0] > PosX[0]:
                PosX.append(PosX[0] - 0.01534)  # для трансформатора
                PosY.append(PosY[0])
                PosX.append(PosX[0] - 0.02436)  # для узла
                PosY.append(PosY[0])
                PosX.append(PosX[0] - 0.02753)  # для нагрузки
                PosY.append(PosY[0])
            else:
                PosX.append(PosX[0] + 0.01534)  # для трансформатора
                PosY.append(PosY[0])
                PosX.append(PosX[0] + 0.02436)  # для узла
                PosY.append(PosY[0])
                PosX.append(PosX[0] + 0.02753)  # для нагрузки
                PosY.append(PosY[0])
        else:
            if position[0][1] > PosY[0]:
                PosX.append(PosX[0])  # для трансформатора
                PosY.append(PosY[0] - 0.01534)
                PosX.append(PosX[0])  # для узла
                PosY.append(PosY[0] - 0.02436)
                PosX.append(PosX[0])  # для нагрузки
                PosY.append(PosY[0] - 0.02753)
            else:
                PosX.append(PosX[0])  # для трансформатора
                PosY.append(PosY[0] + 0.01534)
                PosX.append(PosX[0])  # для узла
                PosY.append(PosY[0] + 0.02436)
                PosX.append(PosX[0])  # для нагрузки
                PosY.append(PosY[0] + 0.02753)
        # Position=Get_Bus_data(path_database,Node_ID[0])
        # PosX=Position[0]
        # PosY=Position[1]
        if rows[0][0] == rows[0][2] and rows[0][1] == rows[0][3]:
            pass
        else:
            Maximums = Maximum(path_database)
            if Maximums[0] == None:
                Max_Element_ID = 0
            else:
                Max_Element_ID = Maximums[0]
            if Maximums[1] == None:
                Max_Node_ID = 0
            else:
                Max_Node_ID = Maximums[1]
            if Maximums[2] == None:
                Max_Terminal_ID = 0
            else:
                Max_Terminal_ID = Maximums[2]
            if Maximums[3] == None:
                Max_GraphicText_ID = 0
            else:
                Max_GraphicText_ID = Maximums[3]
            if Maximums[4] == None:
                ProtLoc_ID = 0
            else:
                ProtLoc_ID = Maximums[4]
            if Maximums[5] == None:
                GraphicAddTerminal_ID = 0
            else:
                GraphicAddTerminal_ID = Maximums[5]
            if Maximums[6] == None:
                ProtPickup_ID = 0
            else:
                ProtPickup_ID = Maximums[6]
            if Maximums[7] == None:
                ProtSet_ID = 0
            else:
                ProtSet_ID = Maximums[7]

            place_trans(TP_Sn, Flag_Lf, path_database, Node_ID[0], Node_ID[1], Node_ID[1], PosX, PosY, Max_Element_ID,
                        Max_Node_ID, Max_Terminal_ID, Max_GraphicText_ID, ProtLoc_ID, GraphicAddTerminal_ID,
                        ProtPickup_ID, ProtSet_ID, V)
    con.close()


def get_Sn(csv_path):
    TP_Sn = {}
    # csv_path = "LoadPower.csv"
    tables = pd.read_csv(csv_path, sep=';', encoding="utf_8")

    for i in range(len(list(tables['ТП']))):
        TP_Sn[str(list(tables['ТП'])[i])] = float(list(tables['Sнагр'])[i].replace(",", '.'))
    return (TP_Sn)


'''
TP_Sn=get_Sn('D:/aleksey/PythonProjects/Insert Elements/LoadPower.csv')
path_type_db='TypeTr.db'
path_data='Data.csv'
ID=T_type(path_data,path_type_db)
place_elements('R:/2. Моделирование - группа/3 СОТРУДНИКИ/Алексей/проекты/Пермь/Половина_files/database.db',TP_Sn,4,6)

'''


def GUI():
    initial_load = ['P,Q и (v),%', 'P,Q и (V),kV', 'P,Q и (v)-delta,%', 'P, cosφ и v,%', 'P, cosφ и V,kV',
                    'S, cosφ и v,%', 'S, cosφ и V,kV']
    layout = [
        [sg.Text('File LoadPower.csv', size=(18, 1)), sg.InputText(), sg.FileBrowse()],
        [sg.Text('File database.db', size=(18, 1)), sg.InputText(), sg.FileBrowse()],
        [sg.Combo(initial_load)],
        [sg.Output(size=(88, 20))],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('File Compare', layout)
    while True:  # The Event Loop
        event, values = window.read()
        # print(values)
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Submit':
            file1 = file2 = None
            if values[0] and values[1]:
                print(values[0])
                print(values[1])
                file1 = re.findall('.+:\/.+\.+.', values[0])
                file2 = re.findall('.+:\/.+\.+.', values[1])
                isitago = 1
                if not file1 or not file2:
                    print('Error: Files path not valid.')
                    isitago = 0
                    print(type(values[2]))
                if values[2] == 'P,Q и (v),%':
                    Flag_Lf = 1
                elif values[2] == 'P,Q и (V),kV':
                    Flag_Lf = 2
                elif values[2] == 'P,Q и (v)-delta,%':
                    Flag_Lf = 15
                elif values[2] == 'P, cosφ и v,%':
                    Flag_Lf = 11
                elif values[2] == 'P, cosφ и V,kV':
                    Flag_Lf = 12
                elif values[2] == 'S, cosφ и v,%':
                    Flag_Lf = 3
                elif values[2] == 'S, cosφ и V,kV':
                    Flag_Lf = 4
                else:
                    print('Error: Выберите тип исходной нагрузки.')
                    isitago = 0
                if isitago == 1:
                    TP_Sn = get_Sn(values[0])
                    place_elements(values[1], TP_Sn, Flag_Lf, 10)
                    print('Info: Успех!')
            else:
                print('Please choose all files.')
                TP_Sn = get_Sn('D:/aleksey/PythonProjects/Insert Elements/LoadPower.csv')
                place_elements('R:/2. Моделирование - группа/3 СОТРУДНИКИ/Алексей/проекты/TrLoad_files/database.db',
                               TP_Sn, 4, 10)
    window.close()


# path_database='R:/2. Моделирование - группа/3 СОТРУДНИКИ/Алексей/проекты/Пермь/Половина_files/database.db'
# print(Get_Direction(129,path_database))
# D:/aleksey/PythonProjects/Insert Elements/LoadPower.csv
# R:/2. Моделирование - группа/3 СОТРУДНИКИ/Алексей/проекты/TrLoad_files/database.db

TP_Sn = get_Sn('D:/aleksey/PythonProjects/Insert Elements/LoadPower.csv')
path_type_db = 'TypeTr.db'
path_data = 'Data.csv'
ID = T_type(path_data, path_type_db)
place_elements('R:/2. Моделирование - группа/3 СОТРУДНИКИ/Алексей/123_files/database.db', TP_Sn, 4, 6)
