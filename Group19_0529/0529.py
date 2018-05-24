import numpy as np
from PIL import Image
import sys

# this file is a test file


"""
# create Color R,G,B Range
Color_Range = []
Color_Diff = int(256 / 4)
for r in range(256):
    for g in range(256):
        for b in range(256):
            if r % Color_Diff == 0 and g % Color_Diff == 0 and b % Color_Diff == 0:
                Color_Range.append([r, g, b])

Color_Range = np.array(Color_Range)
print(Color_Range.shape)
# print(Color_Range)
"""

image = Image.open("test.jpg")
W, H = image.size
image_array = np.array(image)
print("image shape:", image_array.shape)


def sample_crop(Bg_image_array, UL_local_tuple, LR_local_tuple):
    """
    # parameter:
    image                   the background image by numpy_array
    UL_local_tuple          (x1,y1) the location of Upper Left Corner
    LR_local_tuple          (x2,y2) the location of Lower Right Corner
    """
    (x1, y1) = UL_local_tuple
    (x2, y2) = LR_local_tuple
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    image_crop_H = y2 - y1
    image_crop_W = x2 - x1

    sample_array = np.zeros((image_crop_H, image_crop_W, Bg_image_array.shape[2]), dtype=np.uint8)
    for i in range(image_crop_H):  # H
        for j in range(image_crop_W):  # W
            sample_array[i][j] = Bg_image_array[i + y1][j + x1]
    return sample_array


def image_cube(image_array, cube_size):
    """
    image_array: image by numpy array, dtype = numpy.uint8
    cube_size: (h,w) tuple, and the size must a suitable value:
        image_size % tuple size == 0
    :return:
    """
    image_h = image_array.shape[0]
    image_w = image_array.shape[1]
    (cube_h, cube_w) = cube_size

    # check the size value
    if image_h % cube_h != 0 or image_w % cube_w != 0:
        print("Error!the cube_size is not suitable the image size!")
        print("      image_size % tuple size == 0")
        sys.exit()  # exit the process

    image_output = np.zeros(image_array.shape, dtype=np.uint8)
    cube_h_ruler = []
    cube_w_ruler = []
    cube_ruler_sqr = []
    for h in range(image_h + 1):  # +1 for the last number
        if h % cube_h == 0:
            cube_h_ruler.append(h)

    for w in range(image_w + 1):  # +1 for the last number
        if w % cube_w == 0:
            cube_w_ruler.append(w)

    print("set Cube size (cube_h,cube_w):",(cube_h,cube_w))
    print("Cube_h_ruler:", cube_h_ruler)
    print("cube_w_ruler:", cube_w_ruler)
    """
    for h in cube_h_ruler:
        for w in cube_w_ruler:
            cube_ruler_sqr.append([h, w])
    cube_ruler_sqr = np.array(cube_ruler_sqr)
    print("cube_ruler_sqr:",cube_ruler_sqr.shape)
    cube_ruler_sqr = cube_ruler_sqr.reshape(int(image_h / cube_h) + 1, int(image_w / cube_w) + 1, 2)
    print(cube_ruler_sqr[:, :])
    """

    cube_array = np.array([])
    # TODO 找到每一個cube的mean 設定該位置的值
    # for num_cube in range((int(image_h / cube_h) + 1)*(int(image_w / cube_w) + 1)):
    for mark_h in cube_h_ruler:  # h
        for mark_w in cube_w_ruler:  # w
            if mark_h == image_h or mark_w == image_w:
                continue
            else:
                # print((mark_h, mark_w), "\t", end="")
                # copy cube_size element to cube array
                # print("location: UL(x1, y1):", (mark_w, mark_h), "DR(x2,y2):", (mark_w + cube_w, mark_h + cube_h))

                cube_array = sample_crop(image_array, (mark_w, mark_h), (mark_w + cube_w, mark_h + cube_h))
                cube_array = cube_array.reshape(cube_array.shape[0] * cube_array.shape[1], cube_array.shape[2])
                cube_array_mean = cube_array.mean(axis=0)
                '''
                for h in range(cube_h):
                    for w in range(cube_w):
                        cube_array[h,w] = cube_array_mean
                '''
                # print(cube_array_mean)
                # use the mean of color to fill the cube size
                for h in range(cube_h):
                    for w in range(cube_w):
                        image_output[h+mark_h, w+mark_w] = cube_array_mean
                """"""
    #print(image_output.shape)
    #image_output[0,0] = cube_array_mean
    #print(image_output)
    return image_output


# (h,w) cube_size
img_output = image_cube(image_array, (12, 16))
img = Image.fromarray(img_output)
img.save("img_output.jpg")