#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: Logger.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/19 10:36
 @Description:
"""
import datetime


class Logger(object):
	def __init__(self):
		"""Do nothing, by default."""

	@staticmethod
	def log(msg):
		time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with open('data/log.txt', 'a+', encoding='utf-8') as f:
			f.write(time + ' = ' + msg + '\n')


if __name__ == '__main__':
	Logger.log('test msg')
