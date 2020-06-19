#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: BDApi.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/18 17:34
 @Description:
"""
import base64
import os

import requests

from 识别.Logger import Logger


def getByToken(access_token, imageName):
	p2 = {'access_token': access_token, 'image': base64.b64encode(open(imageName, 'rb').read())}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	r2 = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', headers=headers, data=p2)
	return r2.json()


class BDApi(object):
	def __init__(self):
		self.params = {'grant_type': 'client_credentials',
					   'client_id': '',
					   'client_secret': ''}

	def access_token(self):
		access_token = requests.post('https://aip.baidubce.com/oauth/2.0/token', params=self.params).json()[
			'access_token']
		print('创建access_token')
		Logger.log('创建access_token:' + access_token)
		with open('data/access_token', 'w+') as f:
			f.write(access_token)
		return access_token

	def image2str(self, imageName):
		if not os.path.exists('data/access_token'):
			open('data/access_token', 'w+').close()
		with open('data/access_token', encoding='utf-8') as f:
			access_token = f.readline()
		if access_token:
			json = getByToken(access_token, imageName)
			# 若access_token已经不可用，则重新获取
			if 'error_code' in json:
				print('当前access_token不可用')
				access_token = self.access_token()
				json = getByToken(access_token, imageName)
		else:
			access_token = self.access_token()
			json = getByToken(access_token, imageName)
		print(json)
		return json


if __name__ == '__main__':
	print(BDApi().image2str('data/2.png'))
