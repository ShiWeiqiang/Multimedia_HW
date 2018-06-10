import numpy as np
import time
from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte

b = 3

start = time.clock()

# color set to fill the different ball and background
RGB_colored = [(255, 0, 0),
               (0, 255, 0),
               (0, 0, 255),
               (0, 255, 255),
               (255, 0, 255),
               (255, 255, 0),
               (128, 128, 128),
               (255, 255, 255),
               (50, 128, 50),
               (0, 0, 0)]
RGB_colored = np.array(RGB_colored)


def find_nearest_center(pixel_RGB, pixel_Pos, centers):
    """
    return the nearest center
    :param a: each pixel [r,g,b]
    :param centers: a 9*3 R,G,B array
    :param pixel _Pos: (h,w) tuple 0-1 float
    :return:
    """
    mid_d = np.inf
    r = 0
    # add pixel info ==> (x,y,R,G,B)
    pixel_info = np.append(pixel_Pos, pixel_RGB)
    # return the most closed center
    for i in range(len(centers)):
        distance = np.linalg.norm(pixel_info - centers[i])
        if distance < mid_d:
            mid_d = distance
            r = i
    return r


# find position center
def find_pos_center(img):
    """
    把每一個中心點的RGB放在center
    :param img:
    :return:
    """
    # R,G,B 9*3
    # add background RGB => 10*3
    # add position info to center array (R,G,B,X,Y)  float 0-1
    centers = np.zeros((b ** 2, 5))
    H_max = img.shape[0]
    W_max = img.shape[1]

    h, w = (img.shape[0] // b, img.shape[1] // b)
    # get center RGB and position ==> img info
    for i in range(b):
        for j in range(b):
            img_rgb = img[i * h + h // 2, j * w + w // 2]
            pos = ((i * h + h // 2) / H_max, (j * w + w // 2) / W_max)
            img_info = np.append(pos, img_rgb)
            centers[i * b + j] = img_info
    """
    pos = np.zeros((b ** 2, 2))
    for i in range(b):
        for j in range(b):
            pos[i * b + j] = [(i * h + h // 2) / h, (j * w + w // 2) / w]
    centers = np.append(centers, pos)
    """

    # set background RGB center (0,0,0) and position (0.33,0.33)
    background_info = [0.33, 0.33, 0.0, 0.0, 0.0]
    centers = np.row_stack((background_info, centers))

    return centers


def clustering(img, center):
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.int)
    vis_img = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # find the nearest center and mark to mask array
            mask[i, j] = find_nearest_center(img[i, j], (i / img.shape[0], j / img.shape[1]), center)
            # mask i,j return R,G,B number & center [] get the R,G,B
            vis_img[i, j, :] = center[mask[i, j]][2:]
    # mask 0-9 number vis_img:image
    return mask, vis_img


# mask mean for each group
def update_center(img, mask):
    # img => original img , mask 300*300 size :number of color and position
    Centers = np.zeros((b ** 2 + 1, 5))
    for x in range(b ** 2 + 1):
        # prepare for the mean RGB and xy info
        total_arr_R, total_arr_G, total_arr_B, total_arr_h, total_arr_w = 0.0, 0.0, 0.0, 0.0, 0.0
        total_arr_num = 0.0
        # add the same mask pixel
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if x == mask[i, j]:
                    total_arr_num += 1
                    total_arr_R += img[i, j, 0]
                    total_arr_G += img[i, j, 1]
                    total_arr_B += img[i, j, 2]
                    total_arr_h += i / img.shape[0]
                    total_arr_w += j / img.shape[1]
        # get the mean of center
        if total_arr_num > 0:
            Centers[x, 2] = total_arr_R / total_arr_num
            Centers[x, 3] = total_arr_G / total_arr_num
            Centers[x, 4] = total_arr_B / total_arr_num
            Centers[x, 0] = total_arr_h / total_arr_num
            Centers[x, 1] = total_arr_w / total_arr_num

    return Centers


# fill the color by the RGB_colored array
def fill_mask_color(img):
    colored_img = img.copy()
    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            mid = np.inf
            r = 0
            for i in range(len(RGB_colored)):
                distance = np.linalg.norm(img[h][w] - RGB_colored[i] / 256)
                if distance < mid:
                    mid = distance
                    r = i
            colored_img[h][w] = (RGB_colored[r] / 256)

            # img_colored[h, w, :] = (RGB_colored[mask[h, w]]/256)
    return colored_img


# ---------------------------------------------
# first image
img = io.imread("image1.jpg")
img_H,img_W = img.shape[0],img.shape[1]
# resize size must be multiple of 3
img = resize(img, (900, 900), mode="reflect")

# a list of RGB color 9*3
# add a background RGB to Centers
Centers = find_pos_center(img)
# mask 0-8 the number of rgb   fill the color => vis
# mask size 300* 300
mask, vis = clustering(img, Centers)
vis = resize(vis, (img_H,img_W), mode="reflect")
io.imsave('init_image1.jpg', img_as_ubyte(vis))

# the more the batter?
Iters = 5
vis_images = np.zeros((Iters, img.shape[0], img.shape[1], 3))
vis_images_colored = np.zeros((Iters, img.shape[0], img.shape[1], 3))

for n in range(Iters):
    mask, vis = clustering(img, Centers)
    # copy image -> vis to vis_images[i] list
    vis_images[n] = vis
    # fill color by mask
    img_colored = fill_mask_color(vis)
    vis_images_colored[n] = img_colored
    # update center
    Centers = update_center(img, mask)
    print("finish image:", n + 1)

# save img
# concatenate all the img
results = np.concatenate(vis_images, axis=1)
output = vis_images_colored[-1]
output = resize(output, (img_H,img_W), mode="reflect")
results = resize(results, (img_H,img_W * Iters), mode="reflect")
# each 5 Iters 
results_fill_color = np.concatenate(vis_images_colored, axis=1)
results_fill_color = resize(results_fill_color, (img_H,img_W * Iters), mode="reflect")
io.imsave('result_image1.jpg', results)
io.imsave('results_image1_fill_color.jpg', results_fill_color)
io.imsave('Output1.jpg', output)


time_used = (time.clock() - start)
print("Time used:", time_used)


# ---------------------------------------------
# second image
img = io.imread("image2.jpg")
img_H,img_W = img.shape[0],img.shape[1]
# resize size must be multiple of 3
img = resize(img, (150, 150), mode="reflect")

# a list of RGB color 9*3
# add a background RGB to Centers
Centers = find_pos_center(img)
# mask 0-8 the number of rgb   fill the color => vis
# mask size 300* 300
mask, vis = clustering(img, Centers)
vis = resize(vis, (img_H,img_W), mode="reflect")
io.imsave('init_image2.jpg', img_as_ubyte(vis))

# the more the batter?
Iters = 5
vis_images = np.zeros((Iters, img.shape[0], img.shape[1], 3))
vis_images_colored = np.zeros((Iters, img.shape[0], img.shape[1], 3))

for n in range(Iters):
    mask, vis = clustering(img, Centers)
    # copy image -> vis to vis_images[i] list
    vis_images[n] = vis
    # fill color by mask
    img_colored = fill_mask_color(vis)
    vis_images_colored[n] = img_colored
    # update center
    Centers = update_center(img, mask)
    print("finish image:", n + 1)

# save img
# concatenate all the img
results = np.concatenate(vis_images, axis=1)
output = vis_images_colored[-1]
output = resize(output, (img_H,img_W), mode="reflect")
results = resize(results, (img_H,img_W * Iters), mode="reflect")
# each 5 Iters
results_fill_color = np.concatenate(vis_images_colored, axis=1)
results_fill_color = resize(results_fill_color, (img_H,img_W * Iters), mode="reflect")
io.imsave('result_image2.jpg', results)
io.imsave('results_image2_fill_color.jpg', results_fill_color)
io.imsave('Output2.jpg', output)

time_used = (time.clock() - start)
print("Time used:", time_used)
