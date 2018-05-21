#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:44:31 2018

@author: joycehsu
"""

import numpy as np
from skimage import io
from scipy.stats import multivariate_normal


pic_bgr=io.imread("1.jpg")
h,w,d=pic_bgr.shape
pic_2D=pic_bgr.reshape(h*w,d)

ctr_x1=80
ctr_x2=135
ctr_y1=370
ctr_y2=564
ctr_h=ctr_y2-ctr_y1
ctr_w=ctr_x2-ctr_x1
bck_x1=180
bck_x2=800
bck_y1=0
bck_y2=600
bck_h=bck_y2-bck_y1
bck_w=bck_x2-bck_x1

train_back=np.zeros((bck_h*bck_w,3),np.float64)
train_center=np.zeros((ctr_h*ctr_w,3),np.float64)
for i in range(ctr_h):
    for j in range(ctr_w):
        train_center[i*ctr_w+j,0]=pic_bgr[ctr_y1+i,ctr_x1+j,0]
        train_center[i*ctr_w+j,1]=pic_bgr[ctr_y1+i,ctr_x1+j,1]
        train_center[i*ctr_w+j,2]=pic_bgr[ctr_y1+i,ctr_x1+j,2]

tmp_ctr=np.cov(train_center,rowvar=False)
cov_ctr=np.diag(np.diag(tmp_ctr))
D_mean=train_center.mean(axis=0)
rv_ctr=multivariate_normal(D_mean,cov_ctr,allow_singular=True)

for i in range(bck_h):
    for j in range(bck_w):
        train_back[i*bck_w+j,0]=pic_bgr[bck_y1+i,bck_x1+j,0]
        train_back[i*bck_w+j,1]=pic_bgr[bck_y1+i,bck_x1+j,1]
        train_back[i*bck_w+j,2]=pic_bgr[bck_y1+i,bck_x1+j,2]

tmp=np.cov(train_back,rowvar=False)
cov=np.diag(np.diag(tmp))

B_mean=train_back.mean(axis=0)
rv=multivariate_normal(B_mean,cov,allow_singular=True)

ans=pic_bgr.copy()

for i in range(h):
    for j in range(w):# D p B n
        if np.linalg.norm(ans[i,j]-D_mean)<np.linalg.norm(ans[i,j]-B_mean):
            ans[i,j,0]=255
            ans[i,j,1]=255
            ans[i,j,2]=255
        else:
            ans[i,j,0]=0
            ans[i,j,1]=0
            ans[i,j,2]=0
            
            
ctr=pic_bgr[ctr_y1:ctr_y2,ctr_x1:ctr_x2]
bck=pic_bgr[bck_y1:bck_y2,bck_x1:bck_x2]



io.imshow(pic_bgr)
io.imsave("ans.jpg",ans)
io.imsave("ctr.jpg",ctr)
io.imsave("bck.jpg",bck)
io.imshow(ans)
