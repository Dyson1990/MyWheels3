# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: requests_manager.py
    @time: 2017/10/13 9:49
--------------------------------
"""

import sys
import os
import random
import requests
import codecs
import base64
import datetime
from fake_useragent import UserAgent
import random
import multiprocessing
import sqlite3
from contextlib import closing
import traceback

# ua = UserAgent()
# headers = {'Accept': '*/*'
#             , 'Accept-Language': 'en-US,en;q=0.8'
#             , 'Cache-Control': 'max-age=0'
#             , 'User-Agent': ua.random()
#             , 'Connection': 'keep-alive'
#                 }
    

def get_html(url, **kwargs):
    # 设定headers信息
    global headers
    headers = kwargs['headers'] if 'headers' in kwargs else headers
    # 若传入了cookies的信息
    cookies = kwargs['cookies'] if 'cookies' in kwargs else None
    # 若传入了proxy_pool的路径，则读取代理池
    # 代理池提取位置https://ip.ihuan.me/ti.html
    if 'proxy_pool' in kwargs and os.path.exists(kwargs['proxy_pool']):
        with open(kwargs['proxy_pool'], 'r') as f:
            proxy_list = f.read().split('\n')
        proxies = random.choice(proxy_list)
        proxies = {'http':'http://{}'.format(proxies)
                  ,'https':'http://{}'.format(proxies)}
    else:
        proxies = None
		    
    resp = requests.get(url
                        , headers=headers
                        , cookies=cookies
                        , proxies = proxies)
    # 若没传入文本编码，则让requests库自己判定编码
    resp.encoding = kwargs['charset'] if 'charset' in kwargs else resp.apparent_encoding
    resp.raise_for_status() # 若返回的信息中status不是200，则报错

    html = resp.text
    resp.close()

    return html

def test_func(arg1):
    try:
        arg2 = 4
        print('running', arg1, arg2)
        with closing(sqlite3.connect('test.db')) as conn:
            cur = conn.cursor()
            tb_name = 'test_tb'
            rp = cur.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = '{}'".format(tb_name))
            if not rp.fetchall():
                cur.execute("CREATE TABLE {}(args1 VARCHAR(10), args2 VARCHAR(10))".format(tb_name))
            cur.execute("INSER INTO {}({}, {})".format(tb_name, arg1, arg2))
            cur.close()
    except:
        with codecs.open('test.log', 'w', 'utf-8') as fp:
            fp.write(traceback.format_exc())
        
if __name__ == '__main__':
    
    pool = multiprocessing.Pool(1)
    
    arg1 = 1
    arg2 = 2
    while arg1 < arg2:
        print(arg1, arg2)
        pool.map_async(test_func, [(arg1, arg2),])
        arg1 = random.random()
        arg2 = random.random()
    pool.close() # 关闭进程池，不再接受新的进程
    pool.join() # 主进程阻塞等待子进程的退出
    

