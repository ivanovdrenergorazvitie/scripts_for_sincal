
import sqlite3
from time import time
import numpy
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
startTime = time()
path_db = 'database.db'
path_to_templates = 'templates\\'
# con = sqlite3.connect(path_db)
# cursorObj = con.cursor()

# Max_GraphicText_ID = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchall()[0][
#     0]  # это запрос на самый большой GraphicText_ID в GraphicText
# Max_GraphicElement_ID = cursorObj.execute("SELECT MAX(GraphicElement_ID) FROM GraphicElement").fetchall()[0][
#     0]  # это запрос на самый большой GraphicText_ID в GraphicText
# Max_GraphicNode_ID = cursorObj.execute("SELECT MAX(GraphicNode_ID) FROM GraphicNode").fetchall()[0][
#     0]  # это запрос на самый большой GraphicText_ID в GraphicText
# Max_GraphicTerminal_ID = cursorObj.execute("SELECT MAX(GraphicTerminal_ID) FROM GraphicTerminal").fetchall()[0][
#     0]  # это запрос на самый большой GraphicText_ID в GraphicText
#
# VoltLevel_ID = cursorObj.execute("SELECT VoltLevel_ID FROM VoltageLevel WHERE Name LIKE '0,4 кВ'").fetchall()
#
# Max_VoltageTran_ID = cursorObj.execute("SELECT MAX(VoltageTran_ID) FROM VoltageTransformer").fetchall()[0][
#     0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
# Max_VoltageTran_ID = 1 if str(Max_VoltageTran_ID) == 'None' else Max_VoltageTran_ID
#
# Max_ProtPickup_ID = cursorObj.execute("SELECT MAX(ProtPickup_ID) FROM ProtPickup").fetchall()[0][
#     0]  # это запрос на самый большой ProtPickup_ID в ProtPickup
# Max_ProtPickup_ID = 1 if str(Max_ProtPickup_ID) == 'None' else Max_ProtPickup_ID
#
# Max_ProtSet_ID = cursorObj.execute("SELECT MAX(ProtSet_ID) FROM ProtOCSetting").fetchall()[0][
#     0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
# Max_ProtSet_ID = 1 if str(Max_ProtSet_ID) == 'None' else Max_ProtSet_ID
#
# Max_ProtLoc_ID = cursorObj.execute("SELECT MAX(ProtLoc_ID) FROM ProtLocation").fetchall()[0][
#     0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
# Max_ProtLoc_ID = 1 if str(Max_ProtLoc_ID) == 'None' else Max_ProtLoc_ID
#
# Max_GraphicAddTerminal_ID = cursorObj.execute("SELECT MAX(GraphicAddTerminal_ID) FROM GraphicAddTerminal").fetchall()[0][
#         0]  # это запрос на самый большой VoltageTran_ID в VoltageTransformer
# Max_GraphicAddTerminal_ID = 1 if str(Max_GraphicAddTerminal_ID) == 'None' else Max_GraphicAddTerminal_ID
#
# Max_Node_ID = cursorObj.execute("SELECT MAX(Node_ID) FROM Node").fetchall()[0][
#     0]  # это запрос на самый большой Node_ID в Node
# # Max_GraphicText_ID = cursorObj.execute("SELECT MAX(GraphicText_ID) FROM GraphicText").fetchall()[0][
# #     0]  # это запрос на самый большой GraphicText_ID в GraphicText
# Max_Terminal_ID = cursorObj.execute("SELECT MAX(Terminal_ID) FROM Terminal").fetchall()[0][
#     0]  # это запрос на самый большой Terminal_ID в Terminal
# Max_Element_ID = cursorObj.execute("SELECT MAX(Element_ID) FROM Element").fetchall()[0][
#     0]  # это запрос на самый большой Element_ID в Element

# def max_id(k):
#     global Max_Element_ID, Max_GraphicElement_ID, Max_Node_ID, Max_GraphicNode_ID, Max_Terminal_ID, Max_GraphicTerminal_ID, Max_GraphicText_ID, Max_ProtSet_ID, Max_ProtLoc_ID, Max_ProtPickup_ID, Max_GraphicAddTerminal_ID
#     Max_Element_ID += 2 * (k - 1)
#     Max_Node_ID += k - 1
#     Max_Terminal_ID += 3 * (k - 1)
#     Max_GraphicNode_ID += k - 1
#     Max_GraphicTerminal_ID += 3 * (k - 1)
#     Max_GraphicText_ID += 8 * (k - 1)
#     Max_GraphicElement_ID += 2 * (k - 1)
#     Max_ProtSet_ID += k - 1
#     Max_ProtLoc_ID += k - 1
#     Max_ProtPickup_ID += k - 1
#     Max_GraphicAddTerminal_ID += k - 1

# def place_trans(x, y):
#     cursorObj.execute(
#         "INSERT INTO TwoWindingTransformer VALUES ({0}, 0, 1, {1}, 0.4, 0.0001, 0.0, 8.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 100.0, 0.9, 59, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0, 103.0, 98.0, 1, 1.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 3, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0, 16.0, 0.0, 0, 0, 2, 0.0, 0.0, 0.0, 0, 0.0, 0.1, 0.05, 0, 0.0, 0, 0.0, 0.0, 0.0, 0, 0, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 8, 0, 0, 1, 0, 0)".format(
#             str(Max_Element_ID + 2 * i), str(a[i - 1][6])))
#     cursorObj.execute(
#         "INSERT INTO Element VALUES ({0}, {1}, 1, 1, 1, {2}, :null, 'TwoWindingTransformer', 3, 1, 1, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0.0, 0, 0, 0, 0, '', :null, 1.0, 1.0)".format(
#             str(Max_Element_ID + 2 * i), str(a[i - 1][3]),
#             "'" + str(a[i - 1][4].split()[0] + ' Т') + "'"),
#         {'null': None})
#     cursorObj.execute(
#         "INSERT INTO Node VALUES ({0}, 1, 1, {1}, {2}, :null, 0.4, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 1, '', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, :null, 0.0, :null, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0, 7, 0, 2, 0.0, 0.0, :null, 0.0, 0)".format(
#             str(Max_Node_ID + i), str(VoltLevel_ID[0][0]),
#             "'" + str(a[i - 1][4].split()[0] + ' Н') + "'"),
#         {'null': None})
#     cursorObj.execute(
#         "INSERT INTO GraphicText VALUES ({0}, 1, 'Arial', 16, 2, 6, 0, 0, 1, 1, 0.0, -0.006811, 0.0, 1, 0, 0, 1, 1)".format(
#             str(Max_GraphicText_ID + 8 * i - 5)))
#     #   ---- Текст трансформатора
#     #   ---- Изображение трансформатора
#     cursorObj.execute(
#         "INSERT INTO GraphicElement VALUES ({0}, 1, 1, {1}, 0,{2}, 16781825, 0, -1, 0, 1, 30, {3},{4}, 20, 0, 0, 1, 1, 1, 0)".format(
#             str(Max_GraphicElement_ID + 2 * i), str(Max_GraphicText_ID + 8 * i - 3),
#             str(Max_Element_ID + 2 * i),
#             str(trans_x), str(trans_y)))
#     #   ---- Изображение узла нагрузки
#     cursorObj.execute(
#         "INSERT INTO GraphicNode VALUES ({0}, 1, 1, {1}, 0, {2}, 0, -1, 0, 1, 0, {3}, {4}, {5}, {6}, 0, 0, 1, 1, 1)".format(
#             str(Max_GraphicNode_ID + i), str(Max_GraphicText_ID + 8 * i - 5), str(Max_Node_ID + i),
#             str(node_x), str(node_y),
#             str(node_x), str(node_y)))
#     pass

params_for_elem = {'dio': [1],
                   'resist': [1, 1],
                   'transist': [0,0, 0.7],
                   'node': [0,0,0.85]}

def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_namepath_to_templates(path):
    for root, dirs, files in os.walk(path):
        return files

def moving_average(a, n=3):
    b = np.cumsum(a, dtype=float)
    b[n:] = b[n:] - b[:-n]
    return b[n-1:] / n

def get_contours(im):
    ## convert image to gray scale (must br done before contouring)
    # image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    image = im
    high = 255


    low = high - 100
    to_be_black_again_low = np.array([high])
    to_be_black_again_high = np.array([255])
    curr_mask = cv2.inRange(image, to_be_black_again_low,
                            to_be_black_again_high)
    image[curr_mask > 0] = (255)

    # making values of this gray level white so we can calculate
    # it's area
    ret, threshold = cv2.threshold(image, low, 255, 0)
    for i in threshold:pass
    contours, hirerchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    return contours

def get_element(image, template, rotation=0, template_symmetry=0, threshold=0.8):
    if rotation not in [0, 1] or template_symmetry not in [0, 1]:
        print()
        print("\nPlease use in 'get_element' for 'rotation' and 'template_symmetry' values '0' and '1'.")
        exit(-1)
    result = []
    for i in range(0, int((1 + 359 * rotation) / (1 + template_symmetry)), 90):
        # center = (w // 2, h // 2)
        # M = cv2.getRotationMatrix2D(center, i, 1.0)
        # print(i)
        # template = cv2.warpAffine(template, M, (w, h))
        # h, w = template.shape[:2]
        if i == 90:
            template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
        h, w = template.shape[:2]
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # Возьмем координаты со степенью совпадения больше% 80
        loc = np.where(res >= threshold)
        # print('trans', loc)
        for pt in zip(*loc[::-1]):  # * Обозначает необязательные параметры
            bottom_right = (pt[0] + w, pt[1] + h)
            # print(pt)
            flag = 0
            for i in result:
                if pt[0] in range(i[0] - w, i[0] + w) and pt[1] in range(i[1] - h, i[1] + h):
                    flag = 1
                    break
            if flag == 0:
                cv2.rectangle(image, pt, bottom_right, (255, 255, 255), -1)
                result.append(pt)
    # print(h, w)
    return result, h, w

def get_terminal(elements, contours):
    a = dict()
    b = 0
    for i in elements:
        a[i] = []
        if elements.index(i) < 3:
            continue
        for l in contours:
            for k in l:
                if str(i[0]).isdigit() and (k[0][0]) in [j for j in range(i[0]-1, i[0]+1 + elements[2])] \
                        and (k[0][1]) in [j for j in range(i[1]-1, i[1]+1 + elements[1])]:
                    b += 1
                    # print(type(contours))
                    a[i] += [contours.index(l)]

                    break
    print(b)
    return a



elements = []
img = cv2.imread('test_XL.png', cv2.IMREAD_REDUCED_GRAYSCALE_2)
print('загрузка изображения', time() - startTime)
# template = cv2.imread(r'C:\Users\user\Desktop\scripts_for_sincal\in_developing\opencv\компьютерное зрение\распознование схем\templates\dio.png', cv2.IMREAD_GRAYSCALE)
for i in get_namepath_to_templates(path_to_templates):
    template = cv2.imread(path_to_templates + i, cv2.IMREAD_GRAYSCALE)
    # viewImage(template)
    contours_el, h, w = get_element(img, template, *params_for_elem[i.split('.')[0]])
    elements += [[i.split('.')[0], h, w] + contours_el]

print('elements', time() - startTime)
contours = get_contours(img)
print('contours', time() - startTime)
cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
print('drawcontours', time() - startTime)
contours = [i.tolist() for i in contours]
print(len(elements[1]))
print(sum([len(i) for i in contours]))
print(len(elements[1])*sum([len(i) for i in contours]))

elements_contours = dict()
# for i in elements:
#     # print(i[0], '-', len(i) - 1)
#     a = get_terminal(i, contours)
#     # print((list(a.items())[0][0]))
#     elements_contours[list(a.items())[0][0]] = a
print('get_term', time() - startTime)
cv2.imwrite("result.png", img)
print('imwrite', time() - startTime)
# print(elements_contours)

# con.commit()  # подтверждаем изменения в БД
# con.close()
# =======
