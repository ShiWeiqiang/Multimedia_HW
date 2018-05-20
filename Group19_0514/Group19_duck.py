import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import multivariate_normal
from PIL import Image

# ------------------------------------------------------------
image = Image.open("duck.jpg")
W,H = image.size
# resize img to H/2 W/2  || speedup 5X
# to remove this opinion ,replace all "/2)" to "/2)"
H = int(H/2)
W = int(W/2)
image = image.resize((W,H))
image = np.array(image)
print(image.shape)

"""
dock local: x,y
(440,100) to (570,410)
"""
# Positive Sample
# prepare the duck Img array
# 130 * 310
duck_array = np.zeros((int(310/2), int(130/2), 3), dtype=np.uint8)

for i in range(int(310/2)): # H
    for j in range(int(130/2)): # W
        duck_array[i][j] = image[i+int(100/2)][j+int(440/2)]

print("Positive Sample:",duck_array.shape)
solve_Img = Image.fromarray(duck_array, mode="RGB")
solve_Img.save("duck_crop.jpg")

'''
# parameter:
image                   the background image by numpy_array
TL_local_tuple          (x1,y1) the location of Top Left Corner
LR_local_tuple          (x2,y2) the location of Lower Right Corner
'''
def sample_crop(Bg_image_array, TL_local_tuple, LR_local_tuple):
    (x1,y1) = TL_local_tuple
    (x2,y2) = LR_local_tuple
    
    return image


print("crop")
"""
sky local: x,y
(50,20) to (200,110)
"""
# Negative Sample
# prepare the BlueSky Img array
sky_array = np.zeros((int(90/2), int(150/2), 3), dtype=np.uint8)

for i in range(int(90/2)): # H
    for j in range(int(150/2)): # W
        sky_array[i][j] = image[i+int(20/2)][j+int(50/2)]

print("Negative Sample_Sky:",sky_array.shape)
solve_Img = Image.fromarray(sky_array, mode="RGB")
solve_Img.save("sky_crop.jpg")


'''
water local: x,y
(0,400) to (200,450)
'''
# Negative Sample
# prepare the Water Img array
water_array = np.zeros((int(50/2), int(200/2), 3), dtype=np.uint8)

for i in range(int(50/2)): # H
    for j in range(int(200/2)): # W
        water_array[i][j] = image[i+int(400/2)][j+int(0/2)]

print("Negative Sample_Water:",water_array.shape)
solve_Img_water = Image.fromarray(water_array, mode="RGB")
solve_Img_water.save("water_crop.jpg")



trainP = duck_array
trainP = trainP.reshape(int(310/2)*int(130/2),3)
print("trainP.Shape:",trainP.shape)

trainN_Sky = sky_array
trainN_Sky = trainN_Sky.reshape(int(90/2)*int(150/2),3)
print("trainN_Sky.Shape:",trainN_Sky.shape)

trainN_Water = water_array
trainN_Water = trainN_Water.reshape(int(50/2)*int(200/2),3)
print("trainN_Water.Shape:",trainN_Water.shape)

tmp1 = np.cov(trainP,rowvar=False)
cov_duck = np.diag(np.diag(tmp1)) # 斜對角矩陣 只有斜線有0

tmp2 = np.cov(trainN_Sky,rowvar=False)
cov_sky = np.diag(np.diag(tmp2))

tmp3 = np.cov(trainN_Water,rowvar=False)
cov_water = np.diag(np.diag(tmp3))

image_mark_duck = np.zeros(image.shape, dtype=np.uint8)

for i in range(H):
    for j in range(W):
        r1 = multivariate_normal.pdf(image[i, j, :], trainP.mean(axis=0), cov_duck)
        r2 = multivariate_normal.pdf(image[i, j, :], trainN_Sky.mean(axis=0), cov_sky)
        r3 = multivariate_normal.pdf(image[i, j, :], trainN_Water.mean(axis=0), cov_water, allow_singular=True)

        if ((r1 > r2) and (r1 > r3)): # duck
            image_mark_duck[i, j, :] = (255, 0, 0)
        if ((r2 > r1) and (r2 > r3)): # sky
            image_mark_duck[i, j, :] = (0, 255, 0)
        if ((r3 > r1) and (r3 > r2)): # water
            image_mark_duck[i, j, :] = (255, 255, 255)

    print("Row", i+1)



img = Image.fromarray(image_mark_duck)
img.save("duck_stats.jpg")


"""
trainP = duck_array
trainN = sky_array


# 多維度
train2 = np.array([
    [10,30], [20,40], [30,50]
])

xy1 = np.array([20,45])
xy2 = np.array([45,20])

tmp = np.cov(image,rowvar=False)
cov2 = np.diag(np.diag(tmp)) # 斜對角矩陣 只有斜線有0

r1 = multivariate_normal.pdf(image, trainP.mean(axis=0), cov2) # ！axis = 0 3個人， 每個人有兩個成績,從row看
r2 = multivariate_normal.pdf(image, trainN.mean(axis=0), cov2)

print(r1,r2)

# 看每一個pixel比較像背景還是花
# 每個格子 分成16個格子 在針對每一個格子做運算 每一個格子分別當做一個人考了27個科目

"""