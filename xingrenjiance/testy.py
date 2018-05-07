#Author:Huangliang   
#Time:2018/5/6

import cv2
import numpy as np
import os
import random

experence = []
neg = []
test = cv2.imread('./4.jpg')
# cv2.imshow("test",test)
# cv2.waitKey (0)
# cv2.destroyAllWindows()
experence.append(test)
test1 = cv2.imread('./5.jpg')
experence.append(test1)

print("打印experence：\n",experence)
print(type(test))
size = [128, 64]
width, height = size[1], size[0]
y = int(random.random() * (len(experence[0]) - height))
x = int(random.random() * (len(experence[0][0]) - width))
print(len(experence[0]))
print(len(experence[0][0]))
print("打印experence[0]\n",experence[0])
print("打印experence[0][0]\n",experence[0][0])
neg.append(experence[0][y:y + height, x:x + width])
print("打印neg：\n",neg)
print(type(neg))
cv2.imshow("test",test)
cv2.imshow("experence",experence[1])
#cv2.imshow("cutout",neg)
cv2.imshow('cutout',neg[0])
cv2.waitKey(0)
cv2.destroyAllWindows()