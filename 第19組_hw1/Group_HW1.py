# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 01:07:14 2018

@author: Shi Weiqiang Econ4A Group_19
"""

import os
import numpy as np
from PIL import Image
from skimage.transform import resize
from skimage import img_as_ubyte, img_as_float
from skimage import io

# Load img
img1 = np.array(Image.open("img1.jpg"))
print(img1.shape)
# resize img1 to 600*450 by skimage
img1 = resize(img1, (450, 600, 3), mode='reflect')
# convert from float to uint8
img1 = img_as_ubyte(img1)

print("resize image_1 to {}".format(img1.shape))
img2 = np.array(Image.open("img2.jpg"))
print(" image_2 shape {}".format(img2.shape))

# gif prepare => 50 frame
frame_shape = (50, img2.shape[0], img2.shape[1], img2.shape[2])
# fill zero to img
frames = np.zeros(shape=frame_shape, dtype=np.uint8)
# get h, w, d from img2
h, w, d = img2.shape
# start img
frames[0] = img2
# save = np.zeros((50, img2.shape[1], img2.shape[2]), dtype = np.uint8)
# prepare for swap ROW => img pan down
new_img_row = np.zeros((img2.shape[0], img2.shape[1], img2.shape[2]), dtype=np.uint8)
# prepare for swap COL => img pan left
new_img_col = np.zeros((img2.shape[0], img2.shape[1], img2.shape[2]), dtype=np.uint8)

# test area
"""
test = frames[i][:,:w-300][:]
io.imshow(test)
"""
# create gif pic
for i in range(49):
    # down 5 pixel
    '''TA's version:
    save = frames[i][h-5:][:]
    new_img[5:][:] = frames[i][:h-5][:]
    new_img[:5][:] = save    
    frames[i+1] = new_img
    '''
    # save the second half of img => 5 ROW
    save_row = frames[i][h - 5:, :][:]
    # offset 5 pixel
    new_img_row[5:, :][:] = frames[i][:h - 5, :][:]
    # use save_row to fill the space
    new_img_row[:5, :][:] = save_row

    # save the left part of img => 3 COL
    save_col = new_img_row[:, :3][:]
    # offset 3 pixel
    new_img_col[:, :w - 3][:] = new_img_row[:, 3:][:]
    # use save_col to fill the space
    new_img_col[:, w - 3:][:] = save_col
    # next frames = create_new img
    frames[i + 1] = new_img_col

# create dir
if not os.path.isdir("gif/"):
    os.makedirs("gif/")

# save frames into dir => gif/
for i in range(len(frames)):
    img = Image.fromarray(frames[i])
    fname = "gif/" + str(i + 1) + ".jpg"
    img.save(fname)

# test area
# if color (RGB) > 1 ====> return 1
"""
print("color G:{}".format(img1[102][77][1]))
print("color G:{}".format(img2[102][77][1]))
img1 = img_as_float(img1)
img2 = img_as_float(img2)
img_test= img1+img2
print("color G:{}".format(img_test[102][77][1]))
for i in range(450):
    for j in range(600):
        for k in range(3):
            if(img_test[i][j][k] >= 1):
                img_test[i][j][k] = 1
io.imshow(img_test)
print("color G:{}".format(img_test[102][77][1]))
"""

# add img1 and img2 to img_plus
for index in range(len(frames)):
    img2 = frames[index]
    # convert img from uint8 to float
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)
    img_plus = img1 + img2
    """
    ########### Method_1 ###########
    # flatten img to 1-D matrix
    img_plus = img_plus.flatten()
    print("max:{}".format(img_plus.max(axis=0)))
    # normalization
    img_plus = (img_plus - img_plus.min(axis=0)) / (img_plus.max(axis=0) - img_plus.min(axis=0))
    # reshape img from 1-D to (450,600,3)
    img_plus = img_plus.reshape((450, 600, 3))
    """
    ########### Method_2 ###########
    # if color (RGB) > 1 ====> return 1

    for i in range(h):
        for j in range(w):
            for k in range(d):
                if(img_plus[i][j][k] >= 1):
                    img_plus[i][j][k] = 1


    # convert img from flowat to uint8
    img_plus = img_as_ubyte(img_plus)
    frames[index] = img_plus
    print("Finish frame:{}".format(index))

# all img in frames
frames_np_to_Image = [Image.fromarray(img) for img in frames]
# save after synthesis image to HW1.gif
frames_np_to_Image[0].save('HW1_output.gif',
                           save_all=True, append_images=frames_np_to_Image[1:],
                           duration=200, loop=0, optimize=True, quality=100)