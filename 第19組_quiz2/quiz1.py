# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 10:07:14 2018

@author: Shi Weiqiang Econ4A Group_19
"""

import numpy
from PIL import Image

# Load img and set W, H
head = Image.open("Head.jpg")
W, H = head.size
print(W,H)
# Img to numpy array
apic_origin = numpy.array(head)
# prepare the affine Img array
apic_affine = numpy.zeros((apic_origin.shape[0], apic_origin.shape[1], apic_origin.shape[2]), dtype=numpy.uint8)


# copy the Head Img to apic_Head
apic_Head = numpy.zeros((1100, 750, 3), dtype=numpy.uint8)
for i in range(1100):# h
    for j in range(750):# w
        apic_Head[i][j] = apic_origin[i+650][j+830]

# prepare the affine Img for Head
apic_affine_head = numpy.zeros((W, H, 3), dtype=numpy.uint8)
'''
Small Img =>  Big Img
apic_Head =>  apic_affine_head
(Col,Row) to the matrix
Affine      Original
(0, 0) =>    (0,0)
(X1,Y1)  => (X1',Y1')
(0, W)  => (0, 1100)
(X2,Y2)  => (X2',Y2')
(W, 0) => (750,0)
(X3,Y3)  => (X3',Y3')
Target      Input
'''

# because of Small Img to Big Img，a_1 Use Affine's point
a_1 = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, H, 0, 0, 1, 0],
    [0, 0, 0, H, 0, 1],
    [W, 0, 0, 0, 1, 0],
    [0, 0, W, 0, 0, 1]
])

# because of Small Img to Big Img，b_1 Use Original's point
b_1 = numpy.array([0, 0, 0, 1100 , 750, 0])
c_1 = numpy.linalg.solve(a_1,b_1)
print(c_1)



for i in range(H):# control row H
    for j in range(W):# control col W
        # find the new (x,y) for pixels
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        ans = numpy.round(numpy.matmul(src,c_1),0)
        # the Local of the pixel in the img
        if ans[1] >= 1100 or ans[0] >= 750:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        # transfor the Img from Part2 to apic_affine_Part2
        apic_affine[i,j] = apic_Head[int(ans[1]),int(ans[0])]


print("Finish part 1")
solve_Img = Image.fromarray(apic_affine, mode="RGB")
solve_Img.save("Output.jpg")

