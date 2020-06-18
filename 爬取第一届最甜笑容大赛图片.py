#!/usr/bin/python3
# -*- coding:utf-8 -*-
import json
import os

import requests

# 使用Firefox打开微博手机版， 登录用户，打开调试工具，找到网络-xhr，打开需要爬取的页面，
# 可以看到有两条get获取的文件类型，hotflow?id=*************&mid=*************,这里我们选择触发源为fetch的那条
# 点击可以获取到请求的cookie
# https://m.weibo.cn/detail/4299462631791021
# https://m.weibo.cn/comments/hotflow?id=4299462631791021&mid=4299462631791021&max_id_type=0


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
}
# cookie信息用上面截图中我们提到的cookie，复制下来粘贴到''里即可
Cookie = {
    'Cookie': 'T_WM=44413335858; XSRF-TOKEN=3d7a8e; WEIBOCN_FROM=1110006030; MLOGIN=1;'
              ' M_WEIBOCN_PARAMS=oid%3D4299462631791021%26luicode%3D20000061%26lfid%3D4299462631791021%26uicode%3D20000061%26fid%3D4299462631791021; SSOLoginState=1590627612; ALF=1593219612; SUB=_2A25zy31MDeRhGeRL61UX9SfPzTuIHXVRNAMErDV6PUNbktAKLWvlkW1NUzOVlQ4NbkcWpaERgWln7Byo8dAY-lFq; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWmFm2VIT2kDube4zGORajJ5JpX5KzhUgL.FozfehMcSK.0SoM2dJLoI7vS9HvXMJvfqJpLdg8u9Pzt; SUHB=0y0oJb-ZQ9VJHn Cache-Control: max-age=0 TE: Trailers'
}

# 存放图片主人微博名和url的字典
pic_info = {}


# 下载图片
def download_pic(pic_info: dict):
    for key, value in pic_info.items():
        print(key, value)
        image_url = value
        file_path = 'D:/a/'
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 如果没有这个path则直接创建
            file_suffix = key + os.path.splitext(image_url)[1]
            print(file_suffix)
            filename = '{}{}'.format(file_path, file_suffix)  # 拼接文件名。
            print(filename)
            with open(filename, 'wb') as f:
                f.write(requests.get(url=image_url).content)

        except IOError as e:
            print(1, e)

        except Exception as e:
            print(2, e)


# 剩余的url和图片主任微博名
def remaining(max_id, max_id_type, num):
    response = requests.get('https://m.weibo.cn/comments/hotflow?mid=4299462631791021&max_id={}&max_id_type={}'.format(
        max_id, max_id_type), headers=headers, cookies=Cookie)

    result = json.loads(response.text)
    print(result)
    ok = result['ok']
    # 没有剩余数据了，此时返回True，在main函数中就会结束循环。
    if ok == 0:
        return True
    datas = result['data']['data']
    for data in datas:
        if 'pic' in data:
            num += 1
            username = data['user']['screen_name']
            # print(username)
            url = data['pic']['url']
            # print(url)
            pic_info[str(num) + username] = url
    return False


if __name__ == '__main__':
    root_url = "https://m.weibo.cn/comments/hotflow?id=4299462631791021&mid=4299462631791021&max_id_type=0"
    # 获取第一页的数据
    response = requests.get(root_url, cookies=Cookie, headers=headers)
    result = json.loads(response.text)
    # 此处result数据类型为字典，可以直接使用。
    ok = result['ok']
    max = result['data']['max']
    max_id = result['data']['max_id']
    max_id_type = result['data']['max_id_type']
    datas = result['data']['data']  # 第一页数据
    print("ok", ok, "max", max, "max_id", max_id, "max_id_type", max_id_type)
    num = 0
    if ok == 1:
        for data in datas:
            username = data['user']['screen_name']
            print(username)
            if 'pic' in data:
                num += 1
                url = data['pic']['url']
                print(url)
                pic_info[str(num) + username] = url
        # 获取剩下所有的数据，max：在图中为24，但其实真实数据是三页，那为什么要用max做循环次数呢？因为如果每条评论下都没有子评论，
        # 那max就是最大循环次数了，我们在剩余数据的函数里做了判断，当ok=0时，直接跳出循环了。所以不用担心多次循环问题
        for i in range(max):
            print("==============================================", i)
            b = remaining(max_id, max_id_type, num)
            if (b):
                break
        print(pic_info)  # 最终得到所有的图片数据
        # # 下载图片
        download_pic(pic_info)
