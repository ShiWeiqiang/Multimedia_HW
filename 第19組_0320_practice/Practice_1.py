#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:26:29 2018

@author: shiweiqiang Econ4A Group19
"""
print("Practice_1")
import numpy as np

a = np.array([
        [2,-4,-9],
        [3, 5,-4],
        [4, 1,-3]
        ])
b = np.array([-1, -3, 4])

print("inverse of matrix A")
inverse = np.linalg.inv(a)

print(inverse)
x = np.dot(inverse,b)
print("解聯立方程:x,y,z")
print(x)


