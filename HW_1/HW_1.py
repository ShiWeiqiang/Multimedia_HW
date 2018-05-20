# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 22:12:56 2018

@author: Shi Weiqiang
"""

from skimage import io,util
import numpy as np
import matplotlib.pyplot as plt

#load image in
spacex = io.imread('spacex.jpg')

#read as grey 0-1(float64)
spacex_gray = io.imread('spacex.jpg',as_grey=True)
#convert form 0-1 to 0-255
spacex_gray = util.img_as_ubyte(spacex_gray)

print('\n\nOriginal Picture')
io.imshow(spacex)

#show second pic
plt.figure()
io.imshow(spacex_gray)
print('\n\nGary Picture')
io.show()

#show size
size = spacex.shape
size_grey = spacex_gray.shape
print(size)
print(size_grey)

#get size
height,width,depth = spacex.shape

io.imsave("grey.jpg",spacex_gray)

#---------invert-----------
invert = np.zeros(size_grey, dtype=np.uint8)
for i in range(height):
    for j in range(width):
        invert[i,j] = 255 - spacex_gray[i,j]

#method 2
invert2 = 255 - spacex_gray

#show picture
io.imshow(spacex_gray)
plt.figure()
io.imshow(invert)
io.show()
io.imsave("invert.jpg",invert)












