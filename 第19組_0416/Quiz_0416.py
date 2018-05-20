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
    [22, 754, 0, 0, 1, 0],
    [0, 0, 22, 754, 0, 1],
    [294, 676, 0, 0, 1, 0],
    [0, 0, 294, 676, 0, 1],
    [550, 754, 0, 0, 1, 0],
    [0, 0, 550, 754, 0, 1]
])
# background
b = numpy.array([41,44,85,20,125,57])
c = numpy.linalg.solve(a,b)
print(c)

pic1 = Image.open("Back.jpg")
pic2 = Image.open("lemonS.jpg")

wMax, hMax = pic1.size
w,h = pic2.size

apic1 = numpy.array(pic1)
apic2 = numpy.array(pic2)


for i in range(hMax):# control row
    for j in range(wMax):# control col
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        ans = numpy.round(numpy.matmul(src,c),0)
        #
        if ans[1] >= h or ans[0] >= w:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        r, g, b = apic2[int(ans[1]),int(ans[0])]
        if r >= 200 and g >= 200 and b >= 200:
            continue

        apic1[i,j] = apic2[int(ans[1]),int(ans[0])]

solve_Img = Image.fromarray(apic1, mode="RGB")
solve_Img.save("save.jpg")