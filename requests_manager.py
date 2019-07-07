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


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

user_agent = random.choice(user_agent_list)
headers = {'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
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
		
    headers['User-Agent'] = random.choice(user_agent_list)
    
    resp = requests.get(url
                        , headers=headers
                        , cookies=cookies
                        , proxies = proxies)
    # 若没传入文本编码，则让requests库自己判定编码
    resp.encoding = kwargs['charset'] if 'charset' in kwargs else resp.apparent_encoding
    resp.raise_for_status() # 若返回的信息中status不是200，则报错

    html = resp.text
    resp.close()

    print("web_code:%s\nuser_agent:%s"%(resp.encoding, headers['User-Agent']))
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
                  , proxy_pool = r'C:\Users\gooddata\Desktop\proxy_pool.txt')
    print('ip地址为：{}'.format(ip))
    s = get_html('http://sz.mnr.gov.cn/kfq/201710/t20171011_1646877.html'
                 , proxy_pool = r'C:\Users\gooddata\Desktop\proxy_pool.txt')
    with codecs.open('test_requests.html', 'w', 'utf-8') as f:
        f.write(s)
    #print(requests_manager.ping_url('www.baidu.com'))

