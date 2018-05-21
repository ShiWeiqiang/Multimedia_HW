import os
import numpy as np
from skimage import io
from math import *
from matplotlib import pyplot as plt

# out of range is True
# in range
def mask_inrange(image ,lower, upper):
    # create 3 channels masks
    for c in range(3):
        tmp_m = (image[:, :, c] >= lower[c]) & (image[:, :, c] <= upper[c])
        if c == 0:
            m = tmp_m
        else:
            m = tmp_m & m
    return m

color = ('red', 'green', 'blue')
Bins = 5
# imp
image = io.imread("duck.jpg")

'''
# create the graph
for i, col in enumerate(color):
    histr, num = np.histogram(image[:, :, i], Bins)
    plt.bar(num[:-1], histr, width = 10, color=col)
    # plt.show()
'''

# 3 cell [R,G,B] lower, [R,G,B] upper
# define the mask -->  color Range
RGBrange = [
    ([50, 120, 185], [95,170,220]),
    ([180, 150, 0], [255, 226, 100])
]

RGBrange_sky = [
    ([50, 120, 185], [95,170,220])
]
RGBrange_duck= [
    ([180, 150, 0], [255, 226, 100]) #
]

ReColor = [
    [0,0,255],
    [255,0,0],
    [0,255,0]
]

img_shape = image.shape
outputs = np.empty(shape=(len(RGBrange), img_shape[0], img_shape[1], img_shape[2]))
output = image.copy()

for(lower,upper) in RGBrange:
    # create the mask
    mask = mask_inrange(image, lower, upper)
    mask = np.logical_not(mask)
    # output = image.copy()
    # background color
    output[mask] = ReColor[2]

for(lower,upper) in RGBrange_sky:
    # create the mask
    mask = mask_inrange(image, lower, upper)
    # output = image.copy()
    # background color
    output[mask] = ReColor[0]

for(lower,upper) in RGBrange_duck:
    # create the mask
    mask = mask_inrange(image, lower, upper)
    # output = image.copy()
    # background color
    output[mask] = ReColor[1]


io.imsave("ReColor_duck.jpg", output)
