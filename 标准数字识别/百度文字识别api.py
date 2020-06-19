#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: 百度文字识别api.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/18 16:29
 @Description:
"""
import base64

import requests

# 1获取Access Token
# https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Va5yQRHlA4Fq5eR3LT0vuXV4&client_secret=0rDSjzQ20XUj5itV6WRtznPQSzr5pVw2&
p1 = {'grant_type': 'client_credentials',
	  'client_id': 'jkuE1NhoDjZiaXq63QjKu5Aq',
	  'client_secret': 'vbEDS9EPKH2YAEHXlGuvYKiNyTSylhj6'}

r1 = requests.post('https://aip.baidubce.com/oauth/2.0/token', params=p1)
print(r1.json())
token = r1.json()['access_token']
print(token)
# 2 进行接口调用
#    https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=【获取的access-token】
# r2 = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=' + token)
p2 = {}
p2['access_token'] = token
image = open('2.png', 'rb').read()
p2['image'] = base64.b64encode(image)
headers = {
	'Content-Type': 'application/x-www-form-urlencoded'
}
r2 = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', headers=headers, data=p2)
print(r2.json())
