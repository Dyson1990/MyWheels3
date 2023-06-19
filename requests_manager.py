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
from pathlib import Path
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
    from tqdm import tqdm
    # req = requests.get(url, headers=headers)
    # with open(targetfile, "wb") as code:
    #     code.write(req.content)
    #     print("====>>>Successfully saving %s" %targetfile)
    resp = requests.get(url, headers=headers, stream=True)
    
    # 获取要下载文件的总大小（单位：字节）
    total_size = int(resp.headers.get('Content-Length', 0))
    
    # 将总大小从字节转换为 MB，并保留两位小数
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    # 创建一个进度条对象，并设置描述信息以及总大小
    progress_bar = tqdm(total=total_size_mb, unit='MB', desc=url.split('/')[-1], ncols=80)
    with open(targetfile, 'wb') as fw:
        for data in resp.iter_content(chunk_size=1024):
            # 将下载到的数据写入文件中
            fw.write(data)
            # 更新进度条的当前值
            progress_bar.update(len(data) / (1024 * 1024))
    # 关闭进度条
    progress_bar.close()
        
def get_binary_image(url):
    global headers
    req = requests.get(url, headers=headers)
    try:
        binary_img = base64.b64encode(req.text)
        return binary_img
    except Exception as e0:
        logger.exception(e0)
    


if __name__ == '__main__':
    ip = get_html('https://icanhazip.com'
                  , proxies = "v2ray")
    print('ip地址为：{}'.format(ip))
    s = get_html('http://sz.mnr.gov.cn/kfq/201710/t20171011_1646877.html'
                 , proxies = "v2ray")


    #print(requests_manager.ping_url('www.baidu.com'))

