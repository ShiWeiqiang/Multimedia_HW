#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:24:48 2018

@author: shiweiqiang
"""


"""
1.auto load image
2.numbers of pics
3.height & Width
4.8_bit -> float
5.avg by buf RGB

"""
import os
import glob
import itertools
import numpy as np
from skimage import io

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
img_shape = io.imread(imlist[0]).shape
print(img_shape)

avg_img = np.zeros(img_shape,dtype = np.float)

for im in imlist:
    img = io.imread(im)
    avg_img += img / N
    
avg_img = np.array(np.round(avg_img), dtype = np.uint8)

io.imshow(avg_img)
io.imsave("average.jpg",avg_img)
io.show()
















