#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: test.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/19 9:18
 @Description:
"""
import time

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import PIL
from PIL import ImageGrab, Image

m = PyMouse()
k = PyKeyboard()
time.sleep(5)
print('click')
#
#(562, 404, 630, 443)
# 测试截取定制位置查看截取的图片是否能被识别
with open('data/conf.txt') as f:
	t = eval(f.readline())
print(t)
i = PIL.ImageGrab.grab(t)
i.save('data/test.png')
# 确认输入框框位置
# m.click(t[0] + 120, t[1] + 20)
# 确认提交按钮位置
m.click(t[0] + 120, t[1] + 90)
