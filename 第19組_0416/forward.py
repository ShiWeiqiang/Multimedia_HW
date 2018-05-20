# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:55:23 2018

@author: shiweiqiang

2018.4.16 Multimedia Class
"""

# 1000-1100
import numpy
from PIL import Image

print("Use 3 point to cal out the transformation")
'''
background    new
(22,754)  => (41,44)
(294,676) => (85,20)
(550,754) => (125,57)
'''


#lemon pic
a = numpy.array([
    [41, 44, 0, 0, 1, 0],
    [0, 0, 41, 44, 0, 1],
    [85, 20, 0, 0, 1, 0],
    [0, 0, 85, 20, 0, 1],
    [125, 57, 0, 0, 1, 0],
    [0, 0, 125, 57, 0, 1]
])
# background
b = numpy.array([22,754,294,676,550,754])
c = numpy.linalg.solve(a,b)
print(c)

pic1 = Image.open("Back.jpg")
pic2 = Image.open("lemonS.jpg")

wMax, hMax = pic1.size
w,h = pic2.size

apic1 = numpy.array(pic1)
apic2 = numpy.array(pic2)


for i in range(h):# control row
    for j in range(w):# control col
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        ans = numpy.round(numpy.matmul(src,c),0)
        if ans[1] >= hMax or ans[0] >=wMax:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        r, g, b = apic2[i,j]
        if r >= 200 and g >= 200 and b >= 200:
            continue
        apic1[int(ans[1]),int(ans[0])] = apic2[i,j]

solve_Img = Image.fromarray(apic1, mode="RGB")
solve_Img.save("save.jpg")