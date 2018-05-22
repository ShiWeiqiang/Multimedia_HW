from skimage import io
import numpy as np
img = io.imread('c-snoopy.bmp',as_grey=True)

a,b = img.shape
print(a,b)

img_t = np.zeros((a,b), dtype=np.uint8)
for i in range(a):
    img_t[i,:] = img[i,:]

io.imshow(img.T)

"""output 等價
img_t = np.zeros((b,a), dtype=np.uint8)
for i in range(a):
    img_t[:,i] = img[i,:]
io.imshow(img_t)
"""

io.show()