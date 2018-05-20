#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:59:54 2018

@author: shiweiqiang
"""


import os
import glob
import itertools
import numpy as np
from skimage import io
from PIL import Image

SUPPORTED_EXTENSIONS = ["bmp", "png", "jpg", "jpeg"]

def dataset_files(root):
    #returns a list of all image files in the given directory
    return list(itertools.chain.from_iterable(
            glob.glob(os.path.join( root,"*.{}".format(ext) )  )
            for ext in SUPPORTED_EXTENSIONS))

#讀取目錄的DIR
imlist = dataset_files("sky/")
N = len(imlist)
print(N)
    
#取得 image 的大小  假設大小都一樣
img_shape = io.imread(imlist[0]).shape
print(img_shape)


frames_np = io.imread(imlist[0])
frames_np2Image = [Image.fromarray(img) for img in frames_np]

frames_np2Image[0].save('eg.gif',
               save_all=True,append_images=frames_np2Image[1:],
               duration =200, loop = 0)
##
"""
frames_np2Image = [Image.fromarray(img) for img in imlist]

frames_np2Image[0].save('eg.gif',
               save_all=True,append_images=frames_np2Image[1:],
               duration =200, loop = 0)
"""


