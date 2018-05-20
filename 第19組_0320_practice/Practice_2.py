#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:51:35 2018

@author: shiweiqiang Econ4A 403574063 Group19
"""
import os
import numpy as np
from PIL import Image
print("Practice 2")
im = np.array(Image.open("sky2.jpg"))
print(im.shape)
h,w,d =im.shape
frame_shape = (30, im.shape[0], im.shape[1], im.shape[2])
frames = np.zeros(shape=frame_shape, dtype = np.uint8)
#new_img = np.zeros((im.shape[0], im.shape[1], im.shape[2]), dtype = np.uint8)
"""
for i in range(len(frames)):
    temp = im
    offset = i*50
    #swap array
    for j in range(1489):
        if(j < offset):
            temp[j] = im[1489-offset+j]
        else:
            temp[j] = im[j-offset]

    frames[i] = temp
""" 
"""
for i in range(29):
    save = frames[i][h-50:][:]
    new_img[50:][:] = frames[i][:h-50][:]
    new_img[:50][:] = save
    frames[i+1] = new_img
"""



if not os.path.isdir("sky/"):
    os.makedirs("sky/")

frames = im
for i in range(30):
    frames = np.roll(frames,50,axis = 0)
    img = Image.fromarray(frames)
    fname = "sky/"+str(i+1)+".jpg"
    img.save(fname)


    