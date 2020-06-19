#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: 使用pillow截取屏幕.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/18 14:52
 @Description:
"""
import os

try:
	import cv2
	from PIL import ImageGrab, Image
except:
	os.system('pip install pillow')
	os.system('pip install opencv-python==3.4.3.18')
global img
global point1, point2


def on_mouse(event, x, y, flags, param):
	global img, point1, point2
	img2 = img.copy()
	if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
		point1 = (x, y)
		# cv2.circle(img2, point1, 10, (0, 255, 0), 2)
		cv2.imshow('image', img2)
	elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
		cv2.rectangle(img2, point1, (x, y), (255, 0, 0), 2)
		cv2.imshow('image', img2)
	elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
		point2 = (x, y)
		cv2.rectangle(img2, point1, point2, (0, 0, 255), 2)
		cv2.imshow('image', img2)
		print(point1, point2)  # (722, 32) (922, 61)
		min_x = min(point1[0], point2[0])
		min_y = min(point1[1], point2[1])
		width = abs(point1[0] - point2[0])
		height = abs(point1[1] - point2[1])
		cut_img = img[min_y:min_y + height, min_x:min_x + width]
		cv2.imwrite('crop.png', cut_img)


if __name__ == '__main__':
	img = cv2.imread('grab.png')
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', on_mouse)
	cv2.imshow('image', img)
	cv2.waitKey(0)
