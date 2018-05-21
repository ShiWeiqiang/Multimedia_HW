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
H = int((Imglist[0].shape[0]) / 2)
W = int((Imglist[0].shape[1]) / 2)
Imglist = dataset_files("originals/")
for i in range(N):
    Imglist[i] = Image.open(Imglist[i])
    Imglist[i] = Imglist[i].resize((W,H))
    Imglist[i] = np.array(Imglist[i])
    print("Resize Image shape ",i+1,":",Imglist[i].shape)


# Crop img
def Sample_Crop(Bg_image_array, TL_local_tuple, LR_local_tuple):
    (x1,y1) = TL_local_tuple
    (x2,y2) = LR_local_tuple
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    image_crop_H = y2 - y1
    image_crop_W = x2 - x1
    sample_array = np.zeros((image_crop_H, image_crop_W, Bg_image_array.shape[2]), dtype=np.uint8)
    for i in range(image_crop_H): # H
        for j in range(image_crop_W): # W
            sample_array[i][j] = Bg_image_array[i+y1][j+x1]
    return sample_array





# Method 1
minion_sample_head = Sample_Crop(Imglist[0], (70/2,367/2), (138/2,448/2))
print("Positive Sample:",minion_sample_head.shape)
solve_Img = Image.fromarray(minion_sample_head, mode="RGB")
solve_Img.save("minion_sample_head.jpg")

minion_sample_body = Sample_Crop(Imglist[0], (70/2,470/2), (128/2,530/2))
print("Positive Sample:",minion_sample_body.shape)
solve_Img = Image.fromarray(minion_sample_body, mode="RGB")
solve_Img.save("minion_sample_body.jpg")

bg_sample = Sample_Crop(Imglist[0], (470/2,460/2), (570/2,540/2))
print("Negative Sample:",bg_sample.shape)
solve_Img_Bg = Image.fromarray(bg_sample, mode="RGB")
solve_Img_Bg.save("bg_sample.jpg")

# train
trainP_head = minion_sample_head
trainP_head = trainP_head.reshape((minion_sample_head.shape[0]*minion_sample_head.shape[1]),3)
print("trainP_head.Shape:",trainP_head.shape)

trainP_body = minion_sample_body
trainP_body = trainP_body.reshape((minion_sample_body.shape[0]*minion_sample_body.shape[1]),3)
print("trainP_head.Shape:",trainP_body.shape)

trainN_Bg = bg_sample
trainN_Bg = trainN_Bg.reshape((bg_sample.shape[0]*bg_sample.shape[1]),3)
print("trainN.Shape:",trainN_Bg.shape)

tmp1 = np.cov(trainP_head,rowvar=False)
cov_head = np.diag(np.diag(tmp1)) # 斜對角矩陣 只有斜線有0

tmp2 = np.cov(trainP_body,rowvar=False)
cov_body = np.diag(np.diag(tmp2))

tmp3 = np.cov(trainN_Bg,rowvar=False)
cov_bg = np.diag(np.diag(tmp3))

image_mark_minion = np.zeros(Imglist[0].shape, dtype=np.uint8)
Imglist_output = Imglist

for n in range(N):
    for i in range(H): # H
        for j in range(W): # W
            r1 = multivariate_normal.pdf(Imglist[n][i, j, :], trainP_head.mean(axis=0), cov_head)
            r2 = multivariate_normal.pdf(Imglist[n][i, j, :], trainP_body.mean(axis=0), cov_body)
            r3 = multivariate_normal.pdf(Imglist[n][i, j, :], trainN_Bg.mean(axis=0), cov_bg, allow_singular=True)

            if ((r1 > r3) or (r2 > r3)): # minions
                image_mark_minion[i, j, :] = (255, 255, 255)
            else: # bg
                image_mark_minion[i, j, :] = (0, 0, 0)
        print("Image No.",n+1,"Row", i+1)

    print("Finish No:" ,n+1)
    Imglist_output[n] = image_mark_minion
    # img = Image.fromarray(image_mark_minion)
    # img.save("duck_stats.jpg")


# create dir
if not os.path.isdir("Output/"):
    os.makedirs("Output/")
# save Image
for i in range(len(Imglist)):
    img = Image.fromarray(Imglist_output[i])
    fname = "Output/" + str(i + 1) + ".jpg"
    img.save(fname)