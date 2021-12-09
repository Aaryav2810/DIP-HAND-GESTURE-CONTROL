# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 00:41:21 2021

@author: aarya
"""

import cv2
import numpy as np

def nothing(x):
    pass

img = np.zeros((300,512,3), np.uint8)

cv2.namedWindow('image')
cv2.createTrackbar('R_low','image',0,255,nothing)
cv2.createTrackbar('G_low','image',0,255,nothing)
cv2.createTrackbar('B_low','image',0,255,nothing)

cv2.createTrackbar('R_high','image',0,255,nothing)
cv2.createTrackbar('G_high','image',0,255,nothing)
cv2.createTrackbar('B_high','image',0,255,nothing)

vid = cv2.VideoCapture(0)

while(1): 
    _, frame = vid.read()
    
    frame = cv2.flip(frame,1)
    
    frame = frame[:250,100:]
    frame = cv2.GaussianBlur(frame,(5,5),0)
    
    #(232, 190, 172)
    r_low = cv2.getTrackbarPos('B_low','image')
    g_low = cv2.getTrackbarPos('G_low','image')
    b_low = cv2.getTrackbarPos('R_low','image')
    r_high = cv2.getTrackbarPos('B_high','image')
    g_high = cv2.getTrackbarPos('G_high','image')
    b_high = cv2.getTrackbarPos('R_high','image')
    
    lower_skin = np.array([b_low,g_low,r_low])
    upper_skin = np.array([b_high,g_high,r_high])

    mask = cv2.inRange(frame, lower_skin, upper_skin)
    # res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('image', frame)
    cv2.imshow('segmentation',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(r_low,g_low,b_low)
        print(r_high,g_high,b_high)
        break
  
vid.release()
cv2.destroyAllWindows()
