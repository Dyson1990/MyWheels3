#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:26:18 2021

@author: wolf
"""

import time, queue, json, codecs
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support #网上看到的不知道干什么用，只知道是win10防出错
freeze_support()

with codecs.open('task_args.json', 'r', 'utf-8') as fp:
    args = json.load(fp)


# 发送任务的队列:
task_queue = queue.Queue(args['task_q_size'])
# 接收结果的队列:
res_queue = queue.Queue(args['res_q_size'])

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue) # 据说Windows不能使用lambda
QueueManager.register('get_res_queue', callable=lambda: res_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', args['master_port'])
                       , authkey=args['authkey'].encode('utf-8')
                       )
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task_q = manager.get_task_queue()
res_q = manager.get_res_queue()

while True:
    print(time.asctime(time.localtime(time.time()))
          , '\ntask queue中包含任务：', task_q.qsize()
          , '\nres queue中包含结果：', res_q.qsize()
          , '\n')
    time.sleep(2)

# 关闭:
manager.shutdown()
print('master exit.')