#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 10:20:25 2018

@author: shiweiqiang
"""

#1000-1100
#明天小考內容與今天相關  矩陣運算
import numpy as np

#矩陣乘法
A = np.array([
        [1,4],
        [-3,2]
])
B = np.array([-2, 0.5])

#B*A等價與B作為係數乘以A的矩陣每一個ROWs
print("點乘")
print(B*A)
print("dot")
print(np.dot(B,A))
print(np.dot(A,B))
#dot(A,B)會自動轉換

#解聯立方程
"""
解聯立方程，需要有determined\=0
即A的inverse存在 X = A^-1*B
3x1+x2=9
X1+2X2=8
使用基礎弱運算，消去法
如果Singular Matrix 無解 
"""
a = np.array([
        [3,1],
        [1,2]
        ])
b = np.array([9,8])
x = np.linalg.solve(a,b)
print("解聯立方程")
print(x)

a = np.array([
        [3,4],
        [2,16]
        ])
print("inverse of matrix")
inverse = np.linalg.inv(a)
print(inverse)

#1100-1200
"""
必考！！！------------------------
3X1+x2 = 9
如何解？ >  A^T * A = 9* A^T
"""


#1200-1300
"""
影像處理 avg
矩陣相減處理
找出平面內min max 
 g-min
-------  = C/255
max-min
 
g = C/255 *(max - min) + min
"""
