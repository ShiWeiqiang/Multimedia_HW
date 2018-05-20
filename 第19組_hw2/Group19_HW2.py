# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:07:14 2018

@author: Shi Weiqiang Econ4A 403574063 Group_19
"""

import numpy
from PIL import Image

# Load img and set W, H
head = Image.open("Head.jpg")
W, H = head.size

# Img to numpy array
apic_origin = numpy.array(head)
# prepare the affine Img array
apic_affine = numpy.zeros((apic_origin.shape[0], apic_origin.shape[1], apic_origin.shape[2]), dtype=numpy.uint8)

"""
# the ratio of 3 part: ignore W -> only affine the H
# prepare for Other Img
0-499               part 1
-------((500*H/1348),W)
500-999             part 2
-------((1000*H/1348),W)
1000-1347(1348-1)   part 3
"""


# First part of Pic
# copy the Part 1 Img to apic_Part1
apic_Part1 = numpy.zeros((int(500*H/1348), W, 3), dtype=numpy.uint8)
for i in range(int(500*H/1348)):
    for j in range(W):
        apic_Part1[i][j] = apic_origin[i][j]
'''
Big Img   =>   Small Img
(Col,Row) to the matrix
Affine    Original
(0,0)  => (0,0)
(X1,Y1)  => (X1',Y1')
(W,0) => (W,0)
(X2,Y2)  => (X2',Y2')
(W,int(200*H/1348)) => (W,int(500*H/1348))
(X3,Y3)  => (X3',Y3')
Target      Input
'''

# Three Point of Original Pic
a_1 = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [W, 0, 0, 0, 1, 0],
    [0, 0, W, 0, 0, 1],
    [W, int(500*H/1348), 0, 0, 1, 0],
    [0, 0, W, int(500*H/1348), 0, 1]
])
# Three Point of affine Pic
b_1 = numpy.array([0, 0, W, 0, W, int(200*H/1348)])
c_1 = numpy.linalg.solve(a_1,b_1)
print(c_1)

for i in range(int(500*H/1348)):# control row
    for j in range(W):# control col
        # find the new (x,y) for pixels
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        # the Local of the pixel in the img
        ans = numpy.round(numpy.matmul(src,c_1),0)
        if ans[1] >= int(500*H/1348) or ans[0] >= W:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        # transfor the Img from Part1 to apic_affine
        apic_affine[int(ans[1]),int(ans[0])] = apic_Part1[i,j]

print("Finish part 1")




# Second part of Pic
# copy the Part 2 Img to apic_Part1
apic_Part2 = numpy.zeros((int(500*H/1348), W, 3), dtype=numpy.uint8)
for i in range(int(500*H/1348)):
    for j in range(W):
        apic_Part2[i][j] = apic_origin[i+int(500*H/1348)][j]
# prepare the affine img for Part2
apic_affine_Part2 = numpy.zeros((int(1000*H/1348), W, 3), dtype=numpy.uint8)
'''
Small Img =>  Big Img
(Col,Row) to the matrix
Affine                      Original
(0, 0)      =>                (0,0)
(X1,Y1)  => (X1',Y1')
(0, int(1000*H/1348))  => (0, int(500*H/1348))
(X2,Y2)  => (X2',Y2')
(W, int(1000*H/1348)) => (W, int(500*H/1348))
(X3,Y3)  => (X3',Y3')
Target      Input
'''

# because of Small Img to Big Img，a_2 Use Affine's point
a_2 = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, int(1000*H/1348), 0, 0, 1, 0],
    [0, 0, 0, int(1000*H/1348), 0, 1],
    [W, int(1000*H/1348), 0, 0, 1, 0],
    [0, 0, W, int(1000*H/1348), 0, 1]
])

# because of Small Img to Big Img，b_2 Use Original's point
b_2 = numpy.array([0, 0, 0, int(500*H/1348), W, int(500*H/1348)])
c_2 = numpy.linalg.solve(a_2,b_2)
print(c_2)



for i in range(int(1000*H/1348)):# control row
    for j in range(W):# control col
        # find the new (x,y) for pixels
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        ans = numpy.round(numpy.matmul(src,c_2),0)
        # the Local of the pixel in the img
        if ans[1] >= int(500*H/1348) or ans[0] >= W:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        # transfor the Img from Part2 to apic_affine_Part2
        apic_affine_Part2[i,j] = apic_Part2[int(ans[1]),int(ans[0])]

# copy the apic_affine_Part2 img to apic_affine
for i in range(int(1000*H/1348)):
    for j in range(W):
        apic_affine[i+int(200*H/1348)+1][j] = apic_affine_Part2[i][j]

print("Finish part 2")


# Third part of Pic
# copy the Part 3 Img to apic_Part3
apic_Part3 = numpy.zeros((int(348*H/1348), W, 3), dtype=numpy.uint8)
for i in range(int(348*H/1348)):
    for j in range(W):
        apic_Part3[i][j] = apic_origin[i+int(1000*H/1348)][j]
'''
Big Img   =>   Small Img
(Col,Row)
Affine    Original
(0,0)  => (0,0)
(X1,Y1)  => (X1',Y1')
(W,0) => (W,0)
(X2,Y2)  => (X2',Y2')
(W,int(148*H/1348)) => (W,int(348*H/1348))
(X3,Y3)  => (X3',Y3')
Target      Input
'''

# Three Point of Original Pic
a_3 = numpy.array([
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [W, 0, 0, 0, 1, 0],
    [0, 0, W, 0, 0, 1],
    [W, int(348*H/1348), 0, 0, 1, 0],
    [0, 0, W, int(348*H/1348), 0, 1]
])
# Three Point of affine Pic
b_3 = numpy.array([0, 0, W, 0, W, int(148*H/1348)])
c_3 = numpy.linalg.solve(a_3,b_3)
print(c_3)

for i in range(int(348*H/1348)):# control row
    for j in range(W):# control col
        # find the new (x,y) for pixels
        src = numpy.array([
            [j,i,0,0,1,0],
            [0,0,j,i,0,1]
        ])
        # the Local of the pixel in the img
        ans = numpy.round(numpy.matmul(src,c_3),0)
        if ans[1] >= int(148*H/1348) or ans[0] >= W:
            continue # over range
        if ans[1] < 0 or ans[0] < 0:
            continue # over range
        # transfor the Img from Part3 to apic_affine
        # and offset down int(1199*H/1348) pixels
        apic_affine[int(ans[1])+int(1199*H/1348),int(ans[0])] = apic_Part3[i,j]

print("Finish part 3")

solve_Img = Image.fromarray(apic_affine, mode="RGB")
solve_Img.save("Output.jpg")
