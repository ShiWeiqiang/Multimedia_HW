#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:51:16 2018

@author: shiweiqiang
"""

import os
import numpy as np
from PIL import Image

im = np.array(Image.open("lena512_8bit.bmp"))
print(im.shape)
im2 = -im

frames_np = [im, im2]
frames_np2Image = [Image.fromarray(img) for img in frames_np]

frames_np2Image[0].save('eg.gif',
               save_all=True,append_images=frames_np2Image[1:],
               duration =200, loop = 0)


lena = np.array(Image.open("Lenna.jpg"))
lena2 = np.array(Image.open("Lenna.jpg"))
lenalist = [Image.fromarray(lena),
            Image.fromarray(np.ubyte(lena2+0.5))]

lenalist[0].save('eg2.gif',
               save_all=True,append_images=frames_np2Image[1:],
               duration = 200, loop = 0, optimize = True)


io.imshow(im2)
io.show()