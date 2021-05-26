#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:37:07 2021

@author: wolf
"""
import global_setting as gs

import random
import time

from multiprocessing.managers import BaseManager

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass



# QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = gs.master_ip
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, gs.master_port)
                 , authkey=gs.authkey.encode('utf-8')
                )
# 从网络连接:
m.connect()

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
m.register('get_request_q')
# 获取Queue的对象:
request_q = m.get_request_q()

while True:
    str0 = input('do it:')
    tup0 = tuple(str0.split('-'))
    request_q.put(tup0)
    print('Put task', tup0)
# ID23-task_q-1345


# for i in range(100):
#     n = input('do it:')
#     print('Put task %d...' % int(n))
#     task.put(n)
#     time.sleep(1)

print('上传完毕')