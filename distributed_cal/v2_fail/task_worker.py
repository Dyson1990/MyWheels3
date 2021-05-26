#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:45:59 2021

@author: wolf
"""
import global_setting as gs

import time, sys, queue
from multiprocessing.managers import BaseManager

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = gs.master_ip
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, gs.master_port)
                 , authkey=gs.authkey.encode('utf-8')
                )
# 从网络连接:
m.connect()
# 获取Queue的对象:
m.register('get_request_q')
m.register('get_output_q')
request_q = m.get_request_q()
output_q = m.get_output_q()

while True:
    req_id = 'id'
    task_q = 'q'
    request_q.put((req_id, task_q))
    print(req_id, task_q)
    data = output_q.get()
    print(data)
    data = data * 3
    request_q.put((req_id, 'res_q', data))
    time.sleep(2)
# ID23-task_q-1345
# 处理结束:
print('worker exit.')