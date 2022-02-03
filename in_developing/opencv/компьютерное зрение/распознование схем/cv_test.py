
import numpy
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    # cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 2. Сопоставьте несколько объектов
img_rgb = cv2.imread('result.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
ret, threshold_image = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
template = cv2.imread('node.jpg', 0)

h, w = template.shape[:2]
center = (w // 2, h // 2)
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# res = [res]
for i in range(1):
    M = cv2.getRotationMatrix2D(center, i*90, 1.0)
    template = cv2.warpAffine(template, M, (w, h))
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    # print(len(res[1]))
    # print((res[1]))
    # print(img_gray)
    # Возьмем координаты со степенью совпадения больше% 80
    loc = np.where(res >= threshold)
    # print(loc)
    asj = []
    # print(zip(*loc[::-1]))
    for pt in zip(*loc[::-1]):  # * Обозначает необязательные параметры
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img_rgb, pt, bottom_right, (0, 0, 255), 1)
        # print(pt)
        asj.append(pt)

    # cv2.imshow('img_rgb', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
f = open('1.txt','w')
count = 0

print(asj, len(asj))
for i in threshold_image:
    for j in i:
        f.write(str(j) + '\n')
        # count += 1
    f.write('\n')
f.close()
# cv2.imshow('img_rgb', threshold_image)
cv2.waitKey(0)



cv2.destroyAllWindows()
# def grayscale_17_levels (image):
#     high = 255
#     while(1):
#         low = high - 15
#         col_to_be_changed_low = np.array([low])
#         col_to_be_changed_high = np.array([high])
#         curr_mask = cv2.inRange(gray, col_to_be_changed_low,col_to_be_changed_high)
#         gray[curr_mask > 0] = (high)
#         # print(curr_mask > 0)
#         high -= 15
#         if(low == 0 ):
#             break
#         # print(len(curr_mask[0]))
# image = cv2.imread('line.jpg')
# # viewImage(image)
# gray = cv2.cv2tColor(image, cv2.COLOR_BGR2GRAY)
# grayscale_17_levels(gray)
# # viewImage(gray)
#
# def get_name_of_templates():
#     filenames = []
#     for root, dirs, files in os.walk("."):
#         filenames.append(files)
#     return filenames
#
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
    # print(len(contours[3]))
    # print(type((contours[1][0])))
    # print('hirerchy\n', hirerchy)
    lenContours = []
    for i in contours:
        lenContours.append(len(i))
    y = [j for j in (k[0] for k in (i[0] for i in contours[lenContours.index(max(lenContours))]))]
    # a = [j for j in (k[0] for k in (i[0] for i in contours[1]))]
    a = [i for i in range(len(y))]
    print(y)
    plt.plot(a, y)
    plt.show()
    plt.plot(numpy.diff(y) / numpy.diff(a) )
    plt.show()
    plt.plot(moving_average(numpy.diff(y) / numpy.diff(a) ))
    plt.show()
    # print(moving_average(numpy.diff(y) / numpy.diff(a) ))

    if (len(contours) > 0):
        output.append([cv2.contourArea(contours[0])])
    cv2.drawContours(im, contours, -1, (0, 0, 255), 1)
    high -= 15
    first = False
        # if (low <= 0):
        #     break
    # print(contours)
    return a, y
a, y = get_area_of_each_gray_level(img_rgb)
print(a, y)
#
#
# cv2.imwrite('rere.jpg', image)
# viewImage(image)
# templates = get_name_of_templates()
# for i in templates[0]:
#     print(i)