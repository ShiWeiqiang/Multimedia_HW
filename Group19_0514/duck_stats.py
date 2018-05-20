from scipy.stats import multivariate_normal
import numpy as np
from PIL import Image

image = Image.open("duck.jpg")


"""

'''
dock local: x,y
(440,100) to (570,410)
'''
# Positive Sample
# prepare the duck Img array
# 130 * 310
duck_array = np.zeros((310, 130, 3), dtype=np.uint8)

for i in range(310): # H
    for j in range(130): # W
        duck_array[i][j] = image[i+100][j+440]

print(duck_array.shape)
solve_Img = Image.fromarray(duck_array, mode="RGB")
solve_Img.save("duck_crop.jpg")


'''
sky local: x,y
(50,20) to (200,110)
'''
# Negative Sample
# prepare the BlueSky Img array
sky_array = np.zeros((90, 150, 3), dtype=np.uint8)

for i in range(90): # H
    for j in range(150): # W
        sky_array[i][j] = image[i+20][j+50]

print(sky_array.shape)
solve_Img = Image.fromarray(sky_array, mode="RGB")
solve_Img.save("sky_crop.jpg")

trainP = duck_array
trainP = trainP.reshape(310*130,3)
print(trainP.shape)
"""


duckP = Image.open("duck_crop.jpg")
duckN = Image.open("sky_crop.jpg")

duckArray = np.array(image, dtype=np.uint8)
duckPArray = np.array(duckP, dtype=np.uint8)
duckNArray = np.array(duckN, dtype=np.uint8)
ProbMap = np.zeros(duckArray.shape, dtype=np.uint8)

print(duckArray.shape)

trainP = duckPArray.reshape(310*130,3)
trainN = duckNArray.reshape(90*150,3)


tmpP = np.cov(trainP, rowvar=False)
covP = np.diag(np.diag(tmpP))

tmpN = np.cov(trainN, rowvar=False)
covN = np.diag(np.diag(tmpN))


duckArray.flatten()

"""
for i in range(duckArray.shape[0]):
    for j in range(duckArray.shape[1]):
        n1 = multivariate_normal.pdf(duckArray[i, j, :], trainP.mean(axis=0), covP)
        n2 = multivariate_normal.pdf(duckArray[i, j, :], trainN.mean(axis=0), covN)
        if(n1>n2):
            ProbMap[i, j, 0] = 255
            ProbMap[i, j, 1] = 0
            ProbMap[i, j, 2] = 0
    print("Row",i)

"""
img = Image.fromarray(ProbMap)
img.save("duck_stats.jpg")