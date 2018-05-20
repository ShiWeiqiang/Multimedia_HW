# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:07:14 2018

@author: Shi Weiqiang Econ4A 403574063 Group_19
"""

import numpy
from PIL import Image

head = Image.open("Head.jpg")
W, H = head.size
print(W,H)

glass = Image.open("eyeglasses.jpg")
w_g, h_g = glass.size
print(w_g,h_g)

'''
background    new
(200,130)  => (0,0)
(200,185) => (0,654)
(375,185) => (2000,654)
'''


#lemon pic
a = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 654, 0, 0, 1, 0],
    [0, 0, 0, 654, 0, 1],
    [2000, 654, 0, 0, 1, 0],
    [0, 0, 2000, 654, 0, 1]
])
# background
b = numpy.array([200,130,200,185,375,185])
c = numpy.linalg.solve(a,b)
print(c)

pic1 = head
pic2 = glass

wMax, hMax = pic1.size
w,h = pic2.size

apic1 = numpy.array(pic1)
apic2 = numpy.array(pic2)


for i in range(h):# control row
    for j in range(w):# control col
        src = numpy.array([
            [j,i,0,0,1,0],[0,0,j,i,0,1]
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


# ----------part1
pic3 = Image.open("mustache.jpg")
w,h = pic3.size
print(w,h)
apic2 = numpy.array(pic2)


'''
background    new
(200,200)  => (0,0)
(200,240) => (0,665)
(370,240) => (2006,665)
'''


#lemon pic
a = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 665, 0, 0, 1, 0],
    [0, 0, 0, 665, 0, 1],
    [2006, 665, 0, 0, 1, 0],
    [0, 0, 2006, 665, 0, 1]
])
# background
b = numpy.array([200,200,200,240,370,240])
c = numpy.linalg.solve(a,b)
print(c)

#apic1 = numpy.array(pic1)
apic3 = numpy.array(pic3)

for i in range(h):# control row
    for j in range(w):# control col
        src = numpy.array([
            [j,i,0,0,1,0],[0,0,j,i,0,1]
        ])
        ans = numpy.round(numpy.matmul(src,c),0)
        if ans[1] >= hMax or ans[0] >=wMax:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        r, g, b = apic3[i,j]
        if r >= 200 and g >= 200 and b >= 200:
            continue
        apic1[int(ans[1]),int(ans[0])] = apic3[i,j]



solve_Img = Image.fromarray(apic1, mode="RGB")
solve_Img.save("save.jpg")