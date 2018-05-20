import numpy as np
from scipy.stats import multivariate_normal


# pdf probability distribution function
# use scipy.stats
#

trainP = np.array([30,40,50])
trainN = np.array([10,20,30])
x = 30
print(np.cov(trainP))
yP =multivariate_normal.pdf(x, mean=trainP.mean(), cov=np.cov(trainP))
yN =multivariate_normal.pdf(x, mean=trainN.mean(), cov=np.cov(trainN))

print(yP,yN)


# 多維度
train2 = np.array([
    [10,30], [20,40], [30,50]
])

xy1 = np.array([20,45])
xy2 = np.array([45,20])

tmp = np.cov(train2,rowvar=False)
cov2 = np.diag(np.diag(tmp)) # 斜對角矩陣 只有斜線有0

r1 = multivariate_normal.pdf(xy1, train2.mean(axis=0), cov2) # ！axis = 0 3個人， 每個人有兩個成績,從row看
r2 = multivariate_normal.pdf(xy2, train2.mean(axis=0), cov2)

print(r1,r2)

# 看每一個pixel比較像背景還是花
# 每個格子 分成16個格子 在針對每一個格子做運算 每一個格子分別當做一個人考了27個科目