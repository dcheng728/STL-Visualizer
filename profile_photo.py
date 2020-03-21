import cv2
import numpy as np

img = cv2.imread('C:/Users/dchen/Downloads/profileimage.jpg')
print(img.shape)
img = cv2.resize(img,(795,1098))
cv2.imwrite('C:/Users/dchen/Downloads/profileimage2.jpg',img)
cv2.imshow('',img)
cv2.waitKey(0)