import time
import numpy as np
from skimage import io

start = time.clock()
# 加粗白線的方式 mask上設定如果周圍有兩到四個個白點，就設定中間白點
# 濾橫波

def Filter_img (L):
    kernel = (np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]]))
    height, width = L.shape
    filtered = np.zeros_like(L)
    for y in range(height):
        for x in range(width):
            weighted_pixel_sum = 0
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    pixel = 0
                    pixel_y = y + ky
                    pixel_x = x + kx
                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = L[pixel_y, pixel_x]
                    weight = kernel[ky + 1, kx + 1]
                    weighted_pixel_sum += pixel * weight
            filtered[y, x] = abs(weighted_pixel_sum)

    Range = filtered.max() - filtered.min()
    filtered = (filtered - filtered.min()) / Range
    return filtered


L = io.imread("bOX.bmp",as_grey=True)
filtered = Filter_img(L)
io.imsave('filtered1.jpg', filtered)

L = io.imread("bOX2.bmp", as_grey=True)
filtered = Filter_img(L)
io.imsave('filtered2.jpg', filtered)

time_used = (time.clock() - start)
print("Time used:",time_used)