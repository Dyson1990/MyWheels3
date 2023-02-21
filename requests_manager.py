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
import requests
import base64
import time

from pathlib import Path
from loguru import logger
from anti_useragent import UserAgent
ua = UserAgent()

headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
            }

def ping_url(url):
    # 若ping的响应时间在一秒内，则返回True
    backinfo = os.system('ping -w 1 {}'.format(url))
    if backinfo == 1:
        return False
    elif backinfo == 0:
        return True

def get_html(url, **kwargs):
    # 设定headers信息
    global headers
    headers = kwargs['headers'] if 'headers' in kwargs else headers
    headers["user-agent"] = ua.random
    # 若传入了cookies的信息
    cookies = kwargs['cookies'] if 'cookies' in kwargs else None
    # 若传入了timeout的信息
    timeout = kwargs['timeout'] if 'timeout' in kwargs else 20
    # 若传入了proxy_pool的路径，则读取代理池
    if 'proxies' in kwargs:
        if kwargs['proxies'] == "v2ray":
            proxies = {'http': 'socks5://127.0.0.1:10808'
                       , 'https': 'socks5://127.0.0.1:10808'}
        else:
            proxies = {'http':'http://{}'.format(kwargs['proxies'])
                      ,'https':'http://{}'.format(kwargs['proxies'])}
    else:
        proxies = None
    
    while True:
        try:
            resp = requests.get(url
                                , headers=headers
                                , cookies=cookies
                                , proxies=proxies
                                , timeout=timeout)
            # 若没传入文本编码，则让requests库自己判定编码
            resp.encoding = kwargs['charset'] if 'charset' in kwargs else resp.apparent_encoding
            resp.raise_for_status() # 若返回的信息中status不是200，则报错
            break
        except Exception as e:
            logger.error(e)
            logger.error(f"出错url：{url}")
            time.sleep(10)
            
    html = resp.text
    resp.close()
    
    logger.info(f"\"get\" succeed: {url}")
    return html

def get_file(url, targetfile):
    global headers
    req = requests.get(url, headers=headers)
    with open(targetfile, "wb") as code:
        code.write(req.content)
        print("====>>>Successfully saving %s" %targetfile)
        
def get_binary_image(url):
    global headers
    req = requests.get(url, headers=headers)
    try:
        binary_img = base64.b64encode(req.text)
    except:
        raise Exception('网站response中编码不正确，或者返回的不是图片。')
    return binary_img

if __name__ == '__main__':
    ip = get_html('https://icanhazip.com'
                  , proxies = "v2ray")
    print('ip地址为：{}'.format(ip))
    s = get_html('http://sz.mnr.gov.cn/kfq/201710/t20171011_1646877.html'
                 , proxies = "v2ray")


    #print(requests_manager.ping_url('www.baidu.com'))

