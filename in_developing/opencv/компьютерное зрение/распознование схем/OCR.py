import numpy
import cv2 #as cv
import numpy as np
from matplotlib import pyplot as plt
import os

def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_name_of_templates(path):
    filenames = []
    for root, dirs, files in os.walk(path):
        filenames.append(files)
    return filenames

def moving_average(a, n=3):
    b = np.cumsum(a, dtype=float)
    b[n:] = b[n:] - b[:-n]
    return b[n-1:] / n

print(get_name_of_templates("templates"))







