Max_Element_ID = 0
Max_GraphicElement_ID = 0
Max_Node_ID = 0
Max_GraphicNode_ID = 0
Max_Terminal_ID = 0
Max_GraphicTerminal_ID = 0
Max_GraphicText_ID = 0
Max_ProtSet_ID = 0
Max_ProtLoc_ID = 0
Max_ProtPickup_ID = 0
Max_GraphicAddTerminal_ID = 0
node = []
number_of_err = 0
spisok_yzlov_bez_transov = []
a = []
i = 0
b = 0
k = 0
line = 0
lT1 = 0
lineList = 0
cursorObj = 'simple text'
import global_max_id
import get_coordinates
import pl_tr
import pl_pkt
import pl_load
import sqlite3
def max_id(k):
    global Max_Element_ID, Max_GraphicElement_ID, Max_Node_ID, Max_GraphicNode_ID, Max_Terminal_ID, Max_GraphicTerminal_ID, Max_GraphicText_ID, Max_ProtSet_ID, Max_ProtLoc_ID, Max_ProtPickup_ID, Max_GraphicAddTerminal_ID
    Max_Element_ID += 2 * (k - 1)
    Max_Node_ID += k - 1
    Max_Terminal_ID += 3 * (k - 1)
    Max_GraphicNode_ID += k - 1
    Max_GraphicTerminal_ID += 3 * (k - 1)
    Max_GraphicText_ID += 8 * (k - 1)
    Max_GraphicElement_ID += 2 * (k - 1)
    Max_ProtSet_ID += k - 1
    Max_ProtLoc_ID += k - 1
    Max_ProtPickup_ID += k - 1
    Max_GraphicAddTerminal_ID += k - 1

def global_max_id():

    pl_tr.Max_Element_ID = Max_Element_ID
    pl_tr.Max_Node_ID = Max_Node_ID
    pl_tr.Max_Terminal_ID = Max_Terminal_ID
    pl_tr.Max_GraphicTerminal_ID = Max_GraphicTerminal_ID
    pl_tr.Max_GraphicText_ID = Max_GraphicText_ID
    pl_tr.Max_GraphicNode_ID = Max_GraphicNode_ID
    pl_tr.Max_GraphicElement_ID = Max_GraphicElement_ID

    pl_pkt.Max_ProtSet_ID = Max_ProtSet_ID
    pl_pkt.Max_ProtLoc_ID = Max_ProtLoc_ID
    pl_pkt.Max_ProtPickup_ID = Max_ProtPickup_ID
    pl_pkt.Max_GraphicAddTerminal_ID = Max_GraphicAddTerminal_ID
    pl_pkt.Max_Terminal_ID = Max_Terminal_ID
    pl_pkt.Max_GraphicText_ID = Max_GraphicText_ID

    pl_load.Max_Element_ID = Max_Element_ID
    pl_load.Max_Terminal_ID = Max_Terminal_ID
    pl_load.Max_Node_ID = Max_Node_ID
    pl_load.Max_GraphicText_ID = Max_GraphicText_ID
    pl_load.Max_GraphicElement_ID = Max_GraphicElement_ID
    pl_load.Max_GraphicTerminal_ID = Max_GraphicTerminal_ID
def pl_elem():
    j = 1
    try:
        tr_index = node.index(a[i - 1][4])
        pl_pkt.tr_index = tr_index
        pl_load.tr_index = tr_index
    except:
        try:
            tr_index = node.index(a[i - 1][4] + ' Т1')
            pl_pkt.tr_index = tr_index
            pl_load.tr_index = tr_index
            try:
                for j in range(1, 100):
                    if any((a[i - 1][4] + ' Т' + str(j)) in s for s in node):
                        continue
            except:
                print(a[i - 1][4] + ' Т' + str(j) + ' не найдено')
                print()
        except:
            return (a[i - 1][4])
    for k in range(1, j):
        print('Т' + str(k))
        max_id(k)
        global_max_id()
        get_coordinates.get_coordinates(k, cursorObj, b, i, j, line, lT1, lineList)
        pl_tr.pl_tr(k, j)
        pl_load.pl_load(k, j)
        pl_pkt.pl_pkt()
    return 0