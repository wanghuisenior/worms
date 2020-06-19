#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: 识别验证码.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/18 17:01
 @Description:
"""
import os
import time

from 识别.BDApi import BDApi
from 识别.Logger import Logger

try:
	import cv2
	import PIL
	from PIL import ImageGrab, Image
	from pymouse import PyMouse
	from pykeyboard import PyKeyboard


except:
	os.system('pip install pillow')
	os.system('pip install requests')
	os.system('pip install opencv-python')
	os.system('pip install data/pyHook-1.5.1-cp36-cp36m-win_amd64.whl')
	os.system('pip install PyUserInput')

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
		# print(point1, point2)  # (722, 32) (922, 61)
		# min_x = min(point1[0], point2[0])
		# min_y = min(point1[1], point2[1])
		# width = abs(point1[0] - point2[0])
		# height = abs(point1[1] - point2[1])
		# cut_img = img[min_y:min_y + height, min_x:min_x + width]
		# cv2.imwrite('data/result.png', cut_img)
		# 将坐标保存到文件里
		with open('data/conf.txt', 'w+') as f:
			p = point1 + point2
			f.write(str(p))


def grabLoop():
	print('配置文件已存在，根据文件内的坐标截取屏幕')
	# 已经存在了配置文件，根据文件内的坐标截取屏幕
	with open('data/conf.txt') as f:
		t = eval(f.readline())
	# 截取图片进行识别
	i = PIL.ImageGrab.grab(t)
	i.save('data/result.png')
	# 获取验证码内容
	code = None
	jsonstr = BDApi().image2str('data/result.png')
	if jsonstr['words_result_num']:
		code = jsonstr['words_result'][0]['words']
	# 点击并输入验证码
	if code and code.isdigit():
		print('识别到了验证码:', code)
		Logger.log('识别到了数字验证码:' + code)
		# 如果识别出来的是整数则点击输入框，并输入
		m.click(t[0] + 120, t[1] + 20)
		time.sleep(1)
		k.type_string(code)
		time.sleep(1)
		# 点击提交按钮
		print('点击提交按钮')
		time.sleep(1)
		m.click(t[0] + 120, t[1] + 90)
	else:
		print('未检测到数字验证码')


if __name__ == '__main__':
	m = PyMouse()
	k = PyKeyboard()
	for i in range(5, 0, -1):
		print(i, '秒后捕获屏幕')
		time.sleep(1)
	if os.path.exists('data/conf.txt'):
		# 每2分钟检测一次
		grabLoop()
		while 1:
			# range(start, end, step=1)
			for t in range(60 * 2, 0, -1):
				print(t, '秒后捕获屏幕')
				time.sleep(1)
			grabLoop()
	else:
		# 截取全屏图片,并获取截图图片的坐标
		image = PIL.ImageGrab.grab()
		image.save('data/window.png')
		img = cv2.imread('data/window.png')
		cv2.namedWindow('image')
		cv2.setMouseCallback('image', on_mouse)
		cv2.imshow('image', img)
		print('请在全屏图片上画出要识别的验证码区域，并回车')
		cv2.waitKey(0)
