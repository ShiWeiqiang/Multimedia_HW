# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 10:07:14 2018

@author: Shi Weiqiang Econ4A 403574063 Group_19
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

"""
Separate the Head Img to nice part
UpperLeft UpperMid UpperRight
Left      Head     Right
DownLeft  DownMid  DownRight

"""

"""
create a function to affine the img:
    if the img enlarge the centre obj and keep the same size
    1.Load the img form array
    2.set the radio of the new img affined:
        1.the 4 new point of img
"""

# set the img and UpperLeft DownRight point
# also the point for new img
def enlarge_centre_img(origin_img,origin_UL,origin_DR,affine_UL,affine_DR):
    print("===start function [enlarge]====")
    W = origin_img.shape[1]
    H = origin_img.shape[0]
    print("the shape of img W:",W,"H:",H)
    # prepare the img to save
    affine_img = numpy.zeros((origin_img.shape[0], origin_img.shape[1], origin_img.shape[2]), dtype=numpy.uint8)



    #  --------------------- Part I ---------------------
    """
    resize the ROW to and enlarge the center row
    """
    # First part of img
    # copy the Part 1 Img to apic_Part1
    apic_Part1_row = numpy.zeros((origin_UL[0], W, 3), dtype=numpy.uint8)
    for i in range(origin_UL[0]):
        for j in range(W):
            apic_Part1_row[i][j] = origin_img[i][j]
    '''
    Big Img   =>   Small Img
    (Col,Row) to the matrix
    Affine    Original
    (0,0)  => (0,0)
    (X1,Y1)  => (X1',Y1')
    (W,0) => (W,0)
    (X2,Y2)  => (X2',Y2')
    (W,affine_UL) => (W,origin_UL[0])
    (X3,Y3)  => (X3',Y3')
    Target      Input
    '''

    # Three Point of Original Pic
    a_1_row = numpy.array([
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [W, 0, 0, 0, 1, 0],
        [0, 0, W, 0, 0, 1],
        [W, origin_UL[0], 0, 0, 1, 0],
        [0, 0, W, origin_UL[0], 0, 1]
    ])
    # Three Point of affine Pic
    b_1_row = numpy.array([0, 0, W, 0, W, affine_UL[0]])
    c_1_row = numpy.linalg.solve(a_1_row, b_1_row)
    print(c_1_row)
    for i in range(origin_UL[0]):  # control row
        for j in range(W):  # control col
            # find the new (x,y) for pixels
            src = numpy.array([
                [j, i, 0, 0, 1, 0],
                [0, 0, j, i, 0, 1]
            ])
            # the Local of the pixel in the img
            ans = numpy.round(numpy.matmul(src, c_1_row), 0)
            if ans[1] >= origin_UL[0] or ans[0] >= W:
                continue  # over range
            if ans[1] < 0 or ans[0] < 0:
                continue  # over range
            # transfor the Img from Part1 to apic_affine
            affine_img[int(ans[1]), int(ans[0])] = apic_Part1_row[i, j]
    print("Finish resize row up")


    # Second part of Pic
    # copy the Part 2 Img to apic_Part2
    # origin_DR[0]-origin_UL[0] is the diff of H
    apic_Part2 = numpy.zeros((origin_DR[0]-origin_UL[0], W, 3), dtype=numpy.uint8)
    for i in range(origin_DR[0]-origin_UL[0]):
        for j in range(W):
            apic_Part2[i][j] = apic_origin[i + origin_UL[0]][j]
    # prepare the affine img for Part2
    apic_affine_Part2 = numpy.zeros((affine_DR[0]-affine_UL[0], W, 3), dtype=numpy.uint8)
    '''
    Small Img =>  Big Img
    (Col,Row) to the matrix
    Affine                      Original
    (0, 0)      =>                (0,0)
    (X1,Y1)  => (X1',Y1')
    (0, int(affine_DR[0]-affine_UL[0]))  => (0, origin_DR[0]-origin_UL[0])
    (X2,Y2)  => (X2',Y2')
    (W, int(affine_DR[0]-affine_UL[0])) => (W, origin_DR[0]-origin_UL[0])
    (X3,Y3)  => (X3',Y3')
    Target      Input
    '''

    # because of Small Img to Big Img，a_2 Use Affine's point
    a_2_row = numpy.array([
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, int(affine_DR[0]-affine_UL[0]), 0, 0, 1, 0],
        [0, 0, 0, int(affine_DR[0]-affine_UL[0]), 0, 1],
        [W, int(affine_DR[0]-affine_UL[0]), 0, 0, 1, 0],
        [0, 0, W, int(affine_DR[0]-affine_UL[0]), 0, 1]
    ])

    # because of Small Img to Big Img，b_2 Use Original's point
    b_2_row = numpy.array([0, 0, 0, int(origin_DR[0]-origin_UL[0]), W, int(origin_DR[0]-origin_UL[0])])
    c_2_row = numpy.linalg.solve(a_2_row, b_2_row)
    print(c_2_row)

    for i in range(int(affine_DR[0]-affine_UL[0])):  # control row
        for j in range(W):  # control col
            # find the new (x,y) for pixels
            src = numpy.array([
                [j, i, 0, 0, 1, 0],
                [0, 0, j, i, 0, 1]
            ])
            ans = numpy.round(numpy.matmul(src, c_2_row), 0)
            # the Local of the pixel in the img
            if ans[1] >= int(origin_DR[0]-origin_UL[0]) or ans[0] >= W:
                continue  # over range
            if ans[1] < 0 or ans[0] < 0:
                continue  # over range
            # transfor the Img from Part2 to apic_affine_Part2
            apic_affine_Part2[i, j] = apic_Part2[int(ans[1]), int(ans[0])]

    # copy the apic_affine_Part2 img to apic_affine
    for i in range(int(affine_DR[0]-affine_UL[0])):
        for j in range(W):
            affine_img[i + affine_UL[0] + 1][j] = apic_affine_Part2[i][j]

    print("Finish resize row mid")

    # Third part of Pic
    # copy the Part 3 Img to apic_Part3
    apic_Part3 = numpy.zeros((int(H-origin_DR[0]), W, 3), dtype=numpy.uint8)
    for i in range(int(H-origin_DR[0])):
        for j in range(W):
            apic_Part3[i][j] = apic_origin[i + origin_DR[0]][j]
    '''
    Big Img   =>   Small Img
    (Col,Row)
    Affine    Original
    (0,0)  => (0,0)
    (X1,Y1)  => (X1',Y1')
    (W,0) => (W,0)
    (X2,Y2)  => (X2',Y2')
    (W,int(affine_DR[0])) => (W,int(H-origin_DR[0]))
    (X3,Y3)  => (X3',Y3')
    Target      Input
    '''

    # Three Point of Original Pic
    a_3 = numpy.array([
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [W, 0, 0, 0, 1, 0],
        [0, 0, W, 0, 0, 1],
        [W, H-origin_DR[0], 0, 0, 1, 0],
        [0, 0, W, H-origin_DR[0], 0, 1]
    ])
    # Three Point of affine Pic
    b_3 = numpy.array([0, 0, W, 0, W, int(H-affine_DR[0])])
    c_3 = numpy.linalg.solve(a_3, b_3)
    print(c_3)

    for i in range(H-origin_DR[0]):  # control row
        for j in range(W):  # control col
            # find the new (x,y) for pixels
            src = numpy.array([
                [j, i, 0, 0, 1, 0],
                [0, 0, j, i, 0, 1]
            ])
            # the Local of the pixel in the img
            ans = numpy.round(numpy.matmul(src, c_3), 0)
            if ans[1] >= int(H-affine_DR[0]) or ans[0] >= W:
                continue  # over range
            if ans[1] < 0 or ans[0] < 0:
                continue  # over range
            # transfor the Img from Part3 to apic_affine
            # and offset down int(1199*H/1348) pixels
            affine_img[int(ans[1]) + affine_DR[0], int(ans[0])] = apic_Part3[i, j]

    print("Finish part 3")
    """
    # for the img which to enlarge, the four corner resize to smaller part
    # so create the function to do that
    def resize_corner():
        print("Finish ") 
    """
    return affine_img
    # finish function
# ==========================================


# call the function by created
apic_affine = enlarge_centre_img(apic_origin,(650,830),(1750,1580),(200,200),(2461,2236))

# transpose the array to enlarge the Col side
apic_affine = enlarge_centre_img(apic_affine.T,(830,650),(1580,1750),(200,200),(2236,2461))
#then transpose three 3 to return the position

solve_Img = Image.fromarray(apic_affine, mode="RGB")
solve_Img.save("Output_2.jpg")

