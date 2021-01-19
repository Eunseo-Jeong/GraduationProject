import numpy as np
import os
import cv2
from pyproj import Transformer

src_x, src_y = -1,-1
des_x, des_y = -1,-1

def select_points_src(event, x, y, flags, param):
    global src_x, src_y, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        src_x, src_y = x, y
        print("frame coordinate:", src_x, src_y)
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def select_points_des(event, x, y, flags, param):
    global des_x, des_y, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        des_x, des_y = x, y
        print("map coordinate:", des_x, des_y)
        cv2.circle(map, (x, y), 5, (0, 0, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

pixel_list = []
map_list = []

frame = cv2.imread('capture.PNG',-1)
frame_copy = frame.copy()
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.moveWindow('frame', 80, 80)
cv2.setMouseCallback('frame', select_points_src)
print(frame.shape)

map = cv2.imread('map.png', -1)
map_copy = map.copy()
cv2.namedWindow('map')
cv2.moveWindow('map', 780, 80)
cv2.setMouseCallback('map', select_points_des)
print(map.shape)


while(1):
    cv2.imshow('map', map)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == ord('s'):
        break;


# cv2.circle(frame_copy, (src_x, src_y), 5, (0, 255, 0), -1)
# cv2.circle(map_copy, (des_x, des_y),5, (0, 255, 0), -1)

frame = cv2.imread('capture.PNG',-1)
frame_copy = frame.copy()
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.moveWindow('frame', 80, 80)
cv2.setMouseCallback('frame', select_points_src)
print(frame.shape)

map = cv2.imread('map.png', -1)
map_copy = map.copy()
cv2.namedWindow('map')
cv2.moveWindow('map', 780, 80)
cv2.setMouseCallback('map', select_points_des)
print(map.shape)


while(1):
    cv2.imshow('map', map)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == ord('s'):
        break;

