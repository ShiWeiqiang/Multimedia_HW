#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:55:23 2018

@author: shiweiqiang

2018.3.12 Multimedia Class
"""

#1000-1100
import numpy as np

#row vector
row = np.array([1,2,3])
print(row)

#col vector
#reshape (( row,co l))
col = row.reshape((3,1))
print(col)

print("original:")
print(row.shape)
print("new:")
print(col.shape)

#1100-1200
for i in range(len(row)):
    print("the {}-th componet of vector row:{}"
          .format(i+1,row[i]) )

#For method
mylist = ['a','b','c']
for item in mylist:
    print(item)

#range(開始值，結束值（不算），每次增加的值)
for item in range(0, 3, 1):
    print(item)


#矩陣乘法
print(row)
print(2*row)
#矩陣組合 通用方法
print("矩陣組合 通用方法")
a1 = np.array([2,3,-2])
a2 = np.array([3,1,1])
a3 = np.array([5,-1,1])
a1 = a1.reshape((3,1))
a2 = a2.reshape((3,1))
a3 = a3.reshape((3,1))
A = np.array([a1, a2, a3])

#method2
A2 = np.array([ [2,3],[3,1],[-2,1] ])
print(A2.shape)

#1200-1300
print("矩陣transport")
M = np.arange(1,7)
print(M)
M_2x3 = M.reshape((2,3))
print(M_2x3)
M_3x2 = M_2x3.T
print(M_3x2)
M_3x2_v2=M.reshape((3,2))
print(M_3x2_v2)
#取值 N_3X2_V2[-1,-1] 冒號用法 斯坦福大學 [:2, 1:3] 先ROW再COL
#gitHub Python Numpy Tutorial：
#http://cs231n.github.io/python-numpy-tutorial/


#矩陣加減乘除  sum的用法


