import numpy as np
from PIL import Image

# this file is a test file
# create Color R,G,B Range
Color_Range = []
Color_Diff = int(256/4)
for r in range(256):
    for g in range(256):
        for b in range(256):
            if(r%Color_Diff==0 and g%Color_Diff==0 and b%Color_Diff==0):
                Color_Range.append([r,g,b])

Color_Range = np.array(Color_Range)
print(Color_Range.shape)
#print(Color_Range)

image = Image.open("test.jpg")
W,H = image.size
image = np.array(image)

# TODO find the most close R,G,B in the color range
for h in range(H):
    for w in range(W):
        # if(image[h,w,:] == )
            