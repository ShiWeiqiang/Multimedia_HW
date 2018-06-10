import numpy as np
from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import time
b = 3

start = time.clock()
# add the x,y info

def find_nearest_center(a, centers):
    """
    return the nearest center
    :param a: each pixel [r,g,b]
    :param centers: a 9*3 R,G,B array
    :return:
    """
    mid_d = np.inf
    r = 0
    for i in range(len(centers)):
        distance = np.linalg.norm(a - centers[i])
        if distance < mid_d:
            mid_d = distance
            r = i
    return r


# find position center
# Final exam
def find_pos_center(img):
    """
    把每一個中心點的RGB放在center
    :param img:
    :return:
    """
    # R,G,B 9*3
    centers = np.zeros((b ** 2, 3))
    h, w = (img.shape[0] // b, img.shape[1] // b)
    for i in range(b):
        for j in range(b):
            centers[i * b + j] = img[i * h + h // 2, j * w + w // 2]
    # each cube centers R,G,B & return a 9*3 array of R,G,B set
    return centers


def clustering(img, center):
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.int)
    vis_img = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            mask[i, j] = find_nearest_center(img[i, j], center)
            # mask i,j return R,G,B number & center [] get the R,G,B
            vis_img[i, j, :] = center[mask[i, j]]
    # mask 0-9 number vis_img:image
    return mask, vis_img


# mask mean for each group
def update_center(img, mask):
    # img => original img , mask 300*300 size :number of color
    new_centers = np.zeros((b ** 2, 3))
    for i in range(len(new_centers)):
        new_centers[i] = img[mask == i].mean(axis=0)
    return new_centers


img = io.imread("ball.jpg")
# resize size must be multiple of 3
img = resize(img, (300, 300), mode="reflect")

# a list of RGB color 9*3
Centers = find_pos_center(img)
# mask 0-8 the number of rgb   fill the color => vis
# mask size 300* 300
mask, vis = clustering(img, Centers)
io.imsave('init.jpg', img_as_ubyte(vis))

# the more the batter?
Iters = 5
vis_images = np.zeros((Iters, img.shape[0], img.shape[1], 3))

for i in range(Iters):
    mask, vis = clustering(img, Centers)
    # update center
    Centers = update_center(img, mask)
    vis_images[i] = vis
    print("finish image:", i + 1)

# save img
# concatenate all the img
results = np.concatenate(vis_images, axis=1)
io.imsave('result.jpg', results)

elapsed = (time.clock() - start)
print("Time used:",elapsed)
# form 35 seconds down to 25-28 seconds