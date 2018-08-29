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
import sys
import os
import numpy as np
import pandas as pd
import urllib.parse
import requests
import hashlib
import json
import time
import codecs 
import traceback

#import set_log  

#log_obj = set_log.Logger('baidu_api.log', set_log.logging.WARNING,
#                         set_log.logging.DEBUG)
#log_obj.cleanup('baidu_api.log', if_cleanup = True)  # 是否需要在每次运行程序前清空Log文件



class baidu_api(object):

    def __init__(self):
        pass

    def _make_sn(self, queryStr, sk):
        # 第一行必须有，否则报中文字符非ascii码错误


        # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak
        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

        # 在最后直接追加上yoursk
        rawStr = encodedStr + sk

        # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
        # 最终合法请求url是http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak&sn=7de5a22212ffaa9e326444c75a58f9a0

        return hashlib.md5(urllib.parse.quote_plus(rawStr).encode(encoding='UTF-8')).hexdigest()

    def get_data(self, query, region, ak='ZGz27O8UEXkC3SEIdHAn7u6aFL1CH0u0', sk='70CTq3TOe3x6XGuhW7RC7z9YVG4r5zuZ'):
        queryStr = '/place/v2/search?query=%s&region=%s&output=json&ak=%s' %(query, region, ak)
        sn = self._make_sn(queryStr, sk)

        url = "http://api.map.baidu.com%s&sn=%s" %(queryStr, sn)

        b = requests.get(url).content
        
        return b

if __name__ == '__main__':
    baidu_api = baidu_api()
    # ak = 'ZGz27O8UEXkC3SEIdHAn7u6aFL1CH0u0'
    # sk = '70CTq3TOe3x6XGuhW7RC7z9YVG4r5zuZ'
    
    # df = pd.DataFrame([])
    
    # with codecs.open('names.txt', 'r', 'utf-8') as f:
        # s0 = f.read()
        
    # l = s0.split('\r\n')
    # for s in l:
        # try:
            # query = s
            # print(query)
            # region = '上海'
        
            # queryStr = '/place/v2/search?query=%s&region=%s&output=json&ak=%s' %(query, region, ak)
            # sn = baidu_api.make_sn(queryStr, sk)
        
            # url = "http://api.map.baidu.com%s&sn=%s" %(queryStr, sn)
            # b = requests.get(url).content
        
            # d = json.loads(b)
            # if 'area' in d['results'][0]:
                # df = df.append({'query':s, 'res':d['results'][0]['area'], 'data':b}, ignore_index=True)
            # else:
                # df = df.append({'query':s, 'res':d['results'][0]['address'], 'data':b}, ignore_index=True)
        # except:
            # df = df.append({'query':s, 'res':'', 'data':b}, ignore_index=True)
            
            # with codecs.open('log.log','a','utf-8') as f:
                # f.write("%s\n%s\n" %(s, traceback.format_exc()))
        
        # df.to_csv('res.csv')
        # print(df)
        
        # time.sleep(1)





