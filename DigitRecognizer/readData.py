'''
@file    : readData.py
@time    : Mar 17,2016 16:24
@author  : duanxxnj@163.com
'''

import cv2

import numpy as np
import pandas as pd

img = pd.read_csv('test.csv')

p1 = img.values[10]
pix = []

for i in range(28):
    pix.append([])
    for j in range(28):
        pix[i].append(p1[i*28 + j])

nppix = np.array(pix)

cv2.imshow("image", np.array(pix))
cv2.waitKey()