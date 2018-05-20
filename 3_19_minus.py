#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 12:29:42 2018

@author: shiweiqiang 403574063 Econ_4_A
"""
import os
import glob
import itertools
import numpy as np
from skimage import io

#Pic擴展名
SUPPORTED_EXTENSIONS = ["bmp", "png", "jpg", "jpeg"]

def dataset_files(root):
    #returns a list of all image files in the given directory
    return list(itertools.chain.from_iterable(
            glob.glob(os.path.join( root,"*.{}".format(ext) )  )
            for ext in SUPPORTED_EXTENSIONS))

#讀取目錄的DIR
imlist = dataset_files("sub_img/")
N = len(imlist)


#取得 image 的大小  假設大小都一樣
img_shape = io.imread(imlist[0],as_grey=True).shape
print(img_shape)

#填充0
minus_img = np.zeros(img_shape, dtype = np.float)

img_1 = io.imread(imlist[0],as_grey=True)
img_2 = io.imread(imlist[1],as_grey=True)

#method_1
#minus_img = imlist[1]-imlist[0]

minus_img = img_1-img_2

#method_2
#0代表黑色  255表示最亮
#"""
max = 0.0
min = 255.0
for i in range(144):
    for j in range(119):
        #print(img_1[i][j])
        if(img_1[i][j]>max):
            max = img_1[i][j]
        if(img_1[i][j]<min):
            min = img_1[i][j]
print("max:{} min{}".format(max,min))
#"""
#"""
for i in range(144):
    for j in range(119):
        #print(img_1[i][j])
        if(minus_img[i][j] <= 0):
            minus_img[i][j] = 255-minus_img[i][j]
#"""
minus_img = np.array(minus_img , dtype = np.uint8)
io.imshow(minus_img)
io.imsave("minus.jpg", minus_img)
io.show()

"""
for im in imlist:
    img = io.imread(im)
    avg_img += avg_img/N  
    
avg_img = np.array(np.round(avg_img), dtype = np.uint8)

io.imshow(avg_img)
io.imsave("average.jpg",avg_img)
io.show()
"""