# import cv2 as cv
#
#
# def viewImage(image, name_of_window):
#     cv.namedWindow(name_of_window, cv.WINDOW_NORMAL)
#     cv.imshow(name_of_window, image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
#
# src = cv.imread('t.jpg')
# gr = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# canny = cv.Canny(gr, 10, 250)
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
# closed = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
# contours = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
# # viewImage(contours, 'ds')
# for cont in contours:
#         #сглаживание и определение количества углов
#         sm = cv.arcLength(cont, True)
#         apd = cv.approxPolyDP(cont, 0.02*sm, True)
#         #выделение контуров
#         if len(apd) == 9:
#             cv.drawContours(src, [apd], -1, (0,255,0), 4)
# cv.imwrite('result.jpg', src)

import numpy
import cv2 #as cv
import numpy as np
from matplotlib import pyplot as plt
import os
# def viewImage(image):
#     cv.namedWindow('Display', cv.WINDOW_KEEPRATIO)
#     cv.imshow('Display', image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# # 2. Сопоставьте несколько объектов
# img_rgb = cv.imread('result.jpg')
# img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
# ret, threshold_image = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
# template = cv.imread('node.jpg', 0)
# h, w = template.shape[:2]
#
# center = (w // 2, h // 2)
# # res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
# # res = [res]
# for i in range(1):
#     M = cv.getRotationMatrix2D(center, 90, 1.0)
#     template = cv.warpAffine(template, M, (w, h))
#     res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
#     threshold = 0.85
#     print(len(res[1]))
#     print((res[1]))
#     # print(img_gray)
#     # Возьмем координаты со степенью совпадения больше% 80
#     loc = np.where(res >= threshold)
#     # print(loc)
#     print(type(loc))
#     # print(zip(*loc[::-1]))
#     for pt in zip(*loc[::-1]):  # * Обозначает необязательные параметры
#         bottom_right = (pt[0] + w, pt[1] + h)
#         cv.rectangle(img_rgb, pt, bottom_right, (255, 255, 255), -1)
#     # print(img_rgb)
#
#     cv.imshow('img_rgb', img_rgb)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# f = open('1.txt','w')
# # count = 0
# for i in threshold_image:
#     for j in i:
#         f.write(str(j) + '\n')
#         # count += 1
#     f.write('\n')
# f.close()
# # cv.imshow('img_rgb', threshold_image)
# cv.waitKey(0)
# cv.destroyAllWindows()



def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def grayscale_17_levels (image):
    high = 255
    while(1):
        low = high - 15
        col_to_be_changed_low = np.array([low])
        col_to_be_changed_high = np.array([high])
        curr_mask = cv2.inRange(gray, col_to_be_changed_low,col_to_be_changed_high)
        gray[curr_mask > 0] = (high)
        # print(curr_mask > 0)
        high -= 15
        if(low == 0 ):
            break
        # print(len(curr_mask[0]))
image = cv2.imread('lin.jpg')
# viewImage(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayscale_17_levels(gray)
# viewImage(gray)

def get_name_of_templates():
    filenames = []
    for root, dirs, files in os.walk("."):
        filenames.append(files)
    return filenames

def moving_average(a, n=3):
    b = np.cumsum(a, dtype=float)
    b[n:] = b[n:] - b[:-n]
    return b[n-1:] / n

def get_area_of_each_gray_level(im):
    ## convert image to gray scale (must br done before contouring)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    output = []
    high = 255
    first = True
    low = 300
    # while (low > 100):


    low = high - 100
    if (first == False):
        # making values that are of a greater gray level black
        ## so it won't get detected
        to_be_black_again_low = np.array([high])
        to_be_black_again_high = np.array([255])
        curr_mask = cv2.inRange(image, to_be_black_again_low,
                                to_be_black_again_high)
        image[curr_mask > 0] = (0)

    # making values of this gray level white so we can calculate
    # it's area
    ret, threshold = cv2.threshold(image, low, 255, 0)
    contours, hirerchy = cv2.findContours(threshold,
                                          cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print(len(contours[3]))
    # print(type((contours[1][0])))
    # print('hirerchy\n', hirerchy)
    y = [j for j in (k[1] for k in (i[0] for i in contours[2]))]
    a = [i for i in range(len(y))]
    print(y)
    plt.plot(a, y)
    plt.show()
    plt.plot(numpy.diff(y) / numpy.diff(a) )
    plt.show()
    plt.plot(moving_average(numpy.diff(y) / numpy.diff(a) ))
    plt.show()
    print(moving_average(numpy.diff(y) / numpy.diff(a) ))

    if (len(contours) > 0):
        output.append([cv2.contourArea(contours[0])])
    cv2.drawContours(im, contours, -1, (0, 0, 255), 1)
    high -= 15
    first = False
        # if (low <= 0):
        #     break
    # print(contours)
    return output
a = get_area_of_each_gray_level(image)
# print(a)


cv2.imwrite('rere.jpg', image)
viewImage(image)
templates = get_name_of_templates()
for i in templates[0]:
    print(i)