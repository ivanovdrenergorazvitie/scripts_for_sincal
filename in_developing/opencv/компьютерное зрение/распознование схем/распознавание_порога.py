import cv2
import matplotlib.pyplot as plt
import numpy
import matplotlib
import random

#------------------------DIREVATIVE(ПРОИЗВОДНАЯ)---------------------------------------
import numpy as np

x = [150 + random.randint(-2,2) for i in range(10)]
x += [i + random.randint(-2,2) for i in range(150, -50, -20)]
x += [-50 + random.randint(-2,2) for i in range(10)]
x += [i + random.randint(-2,2) for i in range(-50, 150, 20)]
print(x)
y = [i for i in range(40)]
print(y)
plt.plot(y, x)
plt.show()
plt.plot(numpy.diff(x) / numpy.diff(y) )
plt.show()
#------------------------DIREVATIVE(ПРОИЗВОДНАЯ)---------------------------------------



#------------------------MOVAVG(СКОЛЬЗЯЩАЯ СРЕДНЯЯ)---------------------------------------
def moving_average(a, n=3):
    b = np.cumsum(a, dtype=float)
    b[n:] = b[n:] - b[:-n]
    return b[n-1:] / n
#------------------------MOVAVG(СКОЛЬЗЯЩАЯ СРЕДНЯЯ)---------------------------------------
