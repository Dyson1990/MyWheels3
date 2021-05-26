#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:37:07 2021

@author: wolf
"""

import random, time, json, codecs
from multiprocessing.managers import BaseManager

with codecs.open('task_args.json', 'r', 'utf-8') as fp:
    args = json.load(fp)

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = args['master_ip']
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, args['master_port'])
                 , authkey=args['authkey'].encode('utf-8')
                )
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()

for i in range(100):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
    time.sleep(1)

print('上传完毕')