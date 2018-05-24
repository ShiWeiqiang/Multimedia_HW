#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shiweiqiang Econ4A
"""
import os
import glob
import itertools
import numpy as np
from scipy.stats import multivariate_normal
from PIL import Image
from skimage import io
from matplotlib import pyplot as plt

# Load image
SUPPORTED_EXTENSIONS = ["bmp", "png", "jpg", "jpeg"]
def dataset_files(root):
    #returns a list of all image files in the given directory
    return list(itertools.chain.from_iterable(
            glob.glob(os.path.join( root,"*.{}".format(ext) )  )
            for ext in SUPPORTED_EXTENSIONS))

#讀取目錄的DIR
Imglist = dataset_files("originals/")
N = len(Imglist)
print("Image N",N)


# to array
for i in range(N):
    Imglist[i] = Image.open(Imglist[i])
    Imglist[i] = np.array(Imglist[i])
    print("Original Image shape ",i+1,":",Imglist[i].shape)

'''
image = Image.open("duck.jpg")
W,H = image.size
# resize img to H/2 W/2  || speedup 5X
# to remove this opinion ,replace all "/2)" to "/2)"
H = int(H/2)
W = int(W/2)
image = image.resize((W,H))
image = np.array(image)
print(image.shape)
'''

# Resize img to speedup
H = int((Imglist[0].shape[0]))
W = int((Imglist[0].shape[1]))
"""
Imglist = dataset_files("originals/")
for i in range(N):
    Imglist[i] = Image.open(Imglist[i])
    Imglist[i] = Imglist[i].resize((W,H))
    Imglist[i] = np.array(Imglist[i])
    print("Resize Image shape ",i+1,":",Imglist[i].shape)
"""

# Crop img
def sample_crop(Bg_image_array, UL_local_tuple, LR_local_tuple):
    """
    # parameter:
    image                   the background image by numpy_array
    UL_local_tuple          (x1,y1) the location of Upper Left Corner
    LR_local_tuple          (x2,y2) the location of Lower Right Corner
    """
    (x1, y1) = UL_local_tuple
    (x2, y2) = LR_local_tuple
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    image_crop_H = y2 - y1
    image_crop_W = x2 - x1
    sample_array = np.zeros((image_crop_H, image_crop_W, Bg_image_array.shape[2]), dtype=np.uint8)
    for i in range(image_crop_H):  # H
        for j in range(image_crop_W):  # W
            sample_array[i][j] = Bg_image_array[i + y1][j + x1]
    return sample_array



minion_sample_head = sample_crop(Imglist[0], (70,367), (138,448))
print("Positive Sample:", minion_sample_head.shape)
solve_Img = Image.fromarray(minion_sample_head, mode="RGB")
solve_Img.save("minion_sample_head.jpg")

minion_sample_body = sample_crop(Imglist[0], (70, 470), (128, 530))
print("Positive Sample:", minion_sample_body.shape)
solve_Img = Image.fromarray(minion_sample_body, mode="RGB")
solve_Img.save("minion_sample_body.jpg")

trainP_head = minion_sample_head.reshape(minion_sample_head.shape[0]*minion_sample_head.shape[1],3)
print("trainP_head.Shape:",trainP_head.shape)
trainP_body = minion_sample_body.reshape(minion_sample_body.shape[0]*minion_sample_body.shape[1],3)
print("trainP_body.Shape:",trainP_body.shape)

# create RGB range
trainP_head_mean = trainP_head.mean(axis=0)
trainP_head_std = np.std(trainP_head,axis=0)
print("trainP_head_mean:",trainP_head_mean)
print("trainP_head_std:",trainP_head_std)

trainP_body_mean = trainP_body.mean(axis=0)
trainP_body_std = np.std(trainP_body,axis=0)
print("trainP_body_mean:",trainP_body_mean)
print("trainP_body_std:",trainP_body_std)



def mask_inrange(image ,lower, upper):
    # create 3 channels masks
    m = True
    for c in range(3):
        tmp_m = (image[:, :, c] >= lower[c]) & (image[:, :, c] <= upper[c])
        if c == 0:
            m = tmp_m
        else:
            m = tmp_m & m
    return m

# lower,upper = mean+- 1 std
Parameter_K = 1.2
RGBrange_head = [
    # lower     upper
    (trainP_head_mean - Parameter_K * trainP_head_std, trainP_head_mean + Parameter_K * trainP_head_std)#head
]
RGBrange_body = [
    (trainP_body_mean - Parameter_K*trainP_body_std, trainP_body_mean + Parameter_K*trainP_body_std)#body
]

"""
bg_sample = Sample_Crop(Imglist[0], (470 / 2, 460 / 2), (570 / 2, 540 / 2))
print("Negative Sample:", bg_sample.shape)
solve_Img_Bg = Image.fromarray(bg_sample, mode="RGB")
solve_Img_Bg.save("bg_sample.jpg")
"""



# copy the list
Imglist_output = Imglist[:]

#Imglist_output[0]

for n in range(N):
    ans = np.zeros(Imglist[0].shape, dtype=np.uint8)
    # ans = Imglist[n].copy()
    for (lower, upper) in RGBrange_head:
        # create the mask
        mask = mask_inrange(Imglist[n], lower, upper)
        # output = image.copy()
        # background color
        ans[mask] = (255, 255, 255)
    for (lower, upper) in RGBrange_body:
        # create the mask
        mask = mask_inrange(Imglist[n], lower, upper)
        # output = image.copy()
        # background color
        ans[mask] = (255, 255, 255)

    ''' 
    ans = np.zeros(Imglist[n].shape, dtype=np.uint8)
    for i in range(H):
        for j in range(W):
    '''
    
    
    Imglist_output[n] = ans.copy()
    print("Finish No:",n+1)
    # Imglist_output[n] = image_mark_minion
    # img = Image.fromarray(image_mark_minion)
    # img.save("duck_stats.jpg")



# Save image
# create dir
if not os.path.isdir("Output/"):
    os.makedirs("Output/")
# save Image
for i in range(len(Imglist)):
    img = Image.fromarray(Imglist_output[i])
    fname = "Output/" + "stat_" + str(i + 1) + ".jpg"
    img.save(fname)