import numpy as np
from PIL import Image

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
print(image_array.shape)


def image_cube(image_array, cube_size):
    """
    image_array: image by numpy array, dtype = numpy.uint8
    cube_size: (h,w) tuple
    :return:
    """
    image_h = image_array.shape[0]
    image_w = image_array.shape[1]
    (cube_h, cube_w) = cube_size
    image_output = image_array.copy()
    cube_h_ruler = []
    cube_w_ruler = []
    cube_ruler_sqr = []
    for h in range(image_h+1):  # +1 for the last number
        if h % cube_h == 0:
            cube_h_ruler.append(h)

    for w in range(image_w+1):  # +1 for the last number
        if w % cube_w == 0:
            cube_w_ruler.append(w)
    print(cube_h_ruler, cube_w_ruler)

    for h in cube_h_ruler:
        for w in cube_w_ruler:
            cube_ruler_sqr.append([h, w])
    cube_ruler_sqr = np.array(cube_ruler_sqr)
    print(cube_ruler_sqr.shape)
    cube_ruler_sqr = cube_ruler_sqr.reshape(int(image_h / cube_h) + 1, int(image_w / cube_w) + 1, 2)
    print(cube_ruler_sqr[10, :])
    # TODO 找到每一個cube的mean 設定該位置的值
    # for num_cube in range((int(image_h / cube_h) + 1)*(int(image_w / cube_w) + 1)):



image_cube(image_array, (60, 80))
