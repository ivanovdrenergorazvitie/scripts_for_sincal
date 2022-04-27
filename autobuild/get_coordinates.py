vniz = 0
trans_x = 0.0
trans_y = 0.0
node_x = 0.0
node_y = 0.0
load_x = 0.0
load_y = 0.0
import pl_tr
import pl_load

def get_coordinates(k, cursorObj, b, i, j):
    global node_x, node_y, trans_x, trans_y, load_x, load_y
    terminalOfSomeintermediateCoordinates = cursorObj.execute(
        "SELECT Element_ID FROM Terminal WHERE Node_ID IN ({0})".format(str(b[i - 1][0][0]))).fetchone()
    # print(terminalOfSomeintermediateCoordinates)
    oldNodeStart_x = b[i - 1][0][11]
    oldNodeStart_y = b[i - 1][0][12]
    oldNodeEnd_x = b[i - 1][0][13]
    oldNodeEnd_y = b[i - 1][0][14]
    try:
        positionBack_x = cursorObj.execute("SELECT SymCenterX FROM GraphicElement WHERE Element_ID IN ({0})".format(
            str(terminalOfSomeintermediateCoordinates[0]))).fetchone()
        positionBack_y = cursorObj.execute("SELECT SymCenterY FROM GraphicElement WHERE Element_ID IN ({0})".format(
            str(terminalOfSomeintermediateCoordinates[0]))).fetchone()
        # print(positionBack_x)

        if vniz == '1':
            if oldNodeStart_y == oldNodeEnd_y and positionBack_y[0] > oldNodeStart_y:
                trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                trans_y = round(oldNodeEnd_y - 0.0075, 4)
                node_x = trans_x
                node_y = round(oldNodeEnd_y - 0.011, 4)
                load_x = trans_x
                load_y = round(oldNodeEnd_y - 0.013, 4)
            elif oldNodeStart_y == oldNodeEnd_y and positionBack_y[0] < oldNodeStart_y:
                trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
                trans_y = round(oldNodeEnd_y + 0.0075, 4)
                node_x = trans_x
                node_y = round(oldNodeEnd_y + 0.011, 4)
                load_x = trans_x
                load_y = round(oldNodeEnd_y + 0.013, 4)
            else:
                if positionBack_x[0] < oldNodeStart_x:
                    trans_x = round(oldNodeEnd_x + 0.0075, 4)
                    trans_y = round(oldNodeStart_x + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                    node_x = round(oldNodeEnd_x + 0.011, 4)
                    node_y = trans_y
                    load_x = round(oldNodeEnd_x + 0.013, 4)
                    load_y = trans_y
                else:
                    trans_x = round(oldNodeEnd_x - 0.0075, 4)
                    trans_y = round(oldNodeStart_x + (oldNodeEnd_y - oldNodeStart_y) * k / j, 4)
                    node_x = round(oldNodeEnd_x - 0.011, 4)
                    node_y = trans_y
                    load_x = round(oldNodeEnd_x - 0.013, 4)
                    load_y = trans_y
        else:
            trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
            trans_y = round(oldNodeEnd_y - 0.0075, 4)
            node_x = trans_x
            node_y = round(oldNodeEnd_y - 0.011, 4)
            load_x = trans_x
            load_y = round(oldNodeEnd_y - 0.013, 4)

    except:
        trans_x = round(oldNodeStart_x + (oldNodeEnd_x - oldNodeStart_x) * k / j, 4)
        trans_y = round(oldNodeEnd_y - 0.0075, 4)
        node_x = trans_x
        node_y = round(oldNodeEnd_y - 0.011, 4)
        load_x = trans_x
        load_y = round(oldNodeEnd_y - 0.013, 4)

    pl_tr.node_x = node_x
    pl_tr.node_y = node_y
    pl_tr.trans_x = trans_x
    pl_tr.trans_y = trans_y
    pl_load.node_x = node_x
    pl_load.node_y = node_y
    pl_load.load_x = load_x
    pl_load.load_y = load_y