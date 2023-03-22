#!/usr/bin/env python
# coding: utf-8

# In[53]:


import requests
import lxml.etree as etree
import random
import codecs
import re
import time
import os
import socket


# In[63]:


with codecs.open(r'C:/windows/system32/drivers/etc/hosts', 'r', 'utf-8') as fp:
    hosts = fp.read()
hosts_list = re.findall(r'(\d+\.\d+\.\d+\.\d+) ([a-z\.]+)', hosts)
hosts_list = [tup[::-1] for tup in hosts_list]
# hosts_dict = {for ip, site in hosts_list}
# socket.getaddrinfo('github.global.ssl.fastly.net', None)
dict(hosts_list)


# In[45]:


# 使用ipaddress.com来获取真实IP
"""
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
            'User-Agent': user_agent,
            'Connection': 'keep-alive'
            }

def parse_detail(html):
    tree = etree.HTML(html)
    xpath = '//table[@class="panel-item table table-stripes table-v"]/tbody/tr[last()]/td/ul/li/text()'
    return tree.xpath(xpath)

# def main():
com_resp = requests.get('https://github.com.ipaddress.com/', headers=headers)
# with codecs.open('com_resp.html', 'w', 'utf-8') as fp:
#     fp.write(com_resp.text)
com_ip = parse_detail(com_resp.text)[0]
print(com_ip)

net_resp = requests.get('https://fastly.net.ipaddress.com/github.global.ssl.fastly.net', headers=headers)
net_ip = parse_detail(net_resp.text)[0]
print(net_ip)

with codecs.open(r'C:/windows/system32/drivers/etc/hosts', 'r', 'utf-8') as fp:
    hosts = fp.read()

hosts = re.sub(r'\d+\.\d+\.\d+\.\d+ github.com', com_ip+' github.com', hosts)
hosts = re.sub(r'\d+\.\d+\.\d+\.\d+ github.global.ssl.fastly.net', net_ip+' github.global.ssl.fastly.net', hosts)

with codecs.open(r'C:/windows/system32/drivers/etc/hosts', 'w', 'utf-8') as fp:
    fp.write(hosts)
    
os.system('ipconfig /flushdns')
print('update successfully!')
time.sleep(10)

"""

