# -*- coding:utf-8 -*-  
#/usr/bin/python3
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: baidu_api.py
    @time: 2018/6/29 13:44
--------------------------------
"""

import requests
import json


#import set_log  

#log_obj = set_log.Logger('baidu_api.log', set_log.logging.WARNING,
#                         set_log.logging.DEBUG)
#log_obj.cleanup('baidu_api.log', if_cleanup = True)  # 是否需要在每次运行程序前清空Log文件

class google_api(object):
    def __init__(self):
        pass

    def get_data(self, address, key='AIzaSyDakw1eATWTRmcz03v_7TpvgZSw9yflgJY'):
        # 返回一个Json格式的dict
        
        headers = {'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'max-age=0',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                   'Connection': 'keep-alive'
                   }
        headers["x-crawlera-use-https"] = "1"
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address,key)
        req = requests.get(url
                           , headers=headers
                           , verify=True)
        
        return json.loads(req.content)

if __name__ == '__main__':
    google_api = google_api()
    print(google_api.get_data('杭州'))
