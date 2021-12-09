# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 12:21:15 2021

@author: aarya
"""

import cv2
import pyautogui
import numpy as np


vid = cv2.VideoCapture(0)
prev_pos = "neutral" 

def max_cnt(contours):
    cnt = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(contours[i])
        if(area > max_area):
            cnt = i
            max_area = area
    return cnt
 
while(1): 
    _, frame = vid.read()
    frame = cv2.flip(frame,1)
    frame = frame[:300,300:600]
    frame = cv2.GaussianBlur(frame,(5,5),0)
    lower_skin = np.array([162,101,215])
    upper_skin = np.array([255,255,255])

    mask = cv2.inRange(frame, lower_skin, upper_skin)
    _,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        continue
    
    max_contour = max(contours,key = cv2.contourArea)

    epsilon = 0.01*cv2.arcLength(max_contour,True)
    max_contour = cv2.approxPolyDP(max_contour,epsilon,True)
    
    M = cv2.moments(max_contour)
    try:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
    except ZeroDivisionError:
        continue

    frame = cv2.circle(frame , (x,y) , 10 , (255,0,0) , 2)
    frame = cv2.drawContours(frame, [max_contour], -1, (0,0,255), 3)

    frame = cv2.line(frame , (75,0) , (75,299) , (255,255,255) , 2)
    frame = cv2.line(frame , (225,0) , (225,299) , (255,255,255) , 2)
    frame = cv2.line(frame , (75,200) , (225,200) , (255,255,255) , 2)
    frame = cv2.line(frame , (75,250) , (225,250) , (255,255,255) , 2)

    cv2.imshow('image', frame)

    if x < 75:
        curr_pos = "left"
    elif x > 225:
        curr_pos = "right"
    elif y < 200 and x > 75 and x < 225:
        curr_pos = "up"
    elif y > 250 and x > 75 and x < 225:
        curr_pos = "down"
    else:
        curr_pos = "neutral"

    if curr_pos!=prev_pos:
        if curr_pos != "neutral":
            pyautogui.press(curr_pos)
        prev_pos = curr_pos
    if cv2.waitKey(1) == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
