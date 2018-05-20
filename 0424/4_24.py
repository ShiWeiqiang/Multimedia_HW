import os
import numpy as np
from skimage import io
from math import *
from matplotlib import pyplot as plt

def mask_inrange(image ,lower, upper):
    # create 3 channels masks
    for c in range(3):
        tmp_m = (image[:, :, c] >= lower[c]) & (image[:, :, c] < upper[c])
        if c == 0:
            m = tmp_m
        else:
            m = tmp_m & m
    return np.logical_not(m)

color = ('red', 'green', 'blue')
Bins = 5
# imp
image = io.imread("Head.jpg")
for i, col in enumerate(color):
    histr, num = np.histogram(image[:, :, i], Bins)
    plt.bar(num[:-1], histr, width = 10, color=col)
    plt.show()


"""
RGBrange = [
    ([0, 50, 0], [255, 200, 255]),
    ([50, 0, 0], [200, 255, 255]),
    ([0, 0, 50], [255, 255, 200]),
]
"""
RGBrange = [
    ([0, 50, 0], [255, 200, 255]),
    ([50, 0, 0], [200, 255, 255]),
    ([0, 0, 50], [255, 255, 200]),
]

index = 0
if not os.path.exists("masked_images/"):
    os.mkdir("masked_images/")

# ====Mid Exam ====
img_shape = image.shape
outputs = np.empty(shape=(len(RGBrange), img_shape[0], img_shape[1], img_shape[2]))
for(lower,upper) in RGBrange:
    # create the mask
    mask = mask_inrange(image, lower, upper)
    output = image.copy()
    output[mask] = 0
    file_name = "masked_images" + str(index+1)+".jpg"
    io.imsave(file_name, output)
    index += 1
