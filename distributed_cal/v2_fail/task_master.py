#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:26:18 2021

@author: wolf
"""
import global_setting as gs

import time
import traceback
import copy
import queue
import collections

import multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support #网上看到的不知道干什么用，只知道是win10防出错
freeze_support()

list_obj = multiprocessing.Manager().list
dict_obj = multiprocessing.Manager().dict
q_dict = dict_obj()
q_dict['default'] = {'task_q': list_obj()
                     , 'res_q': list_obj()
                    }

def monitor_request(q_dict, req_q, output_q):
    print('monitor_request', 'start')
        
    while True:
        item = req_q.get()
        print(item)
        if isinstance(item, tuple) and len(item) == 3:
            req_id, q_name, data = item
            
            if req_id not in q_dict:
                q_dict[req_id] = dict_obj()
            # print(q_dict)
            d0 = q_dict[req_id]
            if q_name not in d0:
                d0[q_name] = list_obj()
                
            # print(q_dict)
            q_dict[req_id][q_name].append(data)
            # print(q_dict)
            
        elif isinstance(item, tuple) and len(item) == 2:
            req_id, q_name = item
            
            if req_id not in q_dict or q_name not in q_dict[req_id]:
                raise Exception(req_id + 'or' + q_name + 'not exist')
            
            data = q_dict[req_id][q_name].pop()
            output_q.put(data)

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', gs.master_port)
                       , authkey=gs.authkey.encode('utf-8')
                       )
mul_q = multiprocessing.Manager().Queue()
manager.register('get_request_q', callable=lambda: mul_q)
manager.register('get_output_q', callable=lambda: queue.Queue())
# 启动Queue:
manager.start()

manager.connect()

request_q = manager.get_request_q()
output_q = manager.get_output_q()
# print(request_q)
monitor_request_p = multiprocessing.Process(target=monitor_request
                                            , args=(q_dict, request_q, output_q)
                                            )
monitor_request_p.start()

while True:
    print(time.asctime(time.localtime(time.time())))
    print('request_q qsize:', request_q.qsize())
    print('output_q qsize:', output_q.qsize())
    for req_id, d0 in q_dict.items():
        for q_name, l0 in d0.items():
            print(req_id, q_name, 'qsize:', len(l0))
    print('\n')
    time.sleep(10)
    
monitor_request_p.close()
manager.shutdown()

# if __name__ == '__main__':
#     manager.connect()
#     request_q = manager.get_request_q()
#     try:
#         while True:
#             print(time.asctime(time.localtime(time.time())))
#             print('existing queue:', q_set)
#             for q_name in q_set:
#                 func_name = 'get_' + q_name
#                 obj0 = getattr(manager, func_name, None)
#                 if obj0:
#                     q0 = obj0()
#                     print(q_name, 'qsize:', q0.qsize())
#                 else:
#                     print("error queue:", q_name)
#             print('\n')
                    
#             if not request_q.empty():
#                 new_q = request_q.get()
#                 if isinstance(new_q, str) and new_q not in q_set:
#                     q_set.add(new_q)
            
#             time.sleep(2)
#     except:
#         traceback.print_exc()
#     finally:
#         # 关闭:
#         manager.shutdown()
#         print('master exit.')

# =============================================================================
# def reboot_manager(manager=None):
#     
#     global q_set
#     backup = {}
#     if manager:
#         for q_name in q_set:
#             func_name = 'get_' + q_name
#             obj0 = getattr(manager, func_name, None)
#             if obj0:
#                 q0 = obj0()
#                 backup[q_name] = copy.deepcopy(q0)
#         
#         print('backup data:', backup)
#         manager.shutdown()
#     # 绑定端口5000, 设置验证码'abc':
#     manager = QueueManager(address=('', gs.master_port)
#                            , authkey=gs.authkey.encode('utf-8')
#                            )
#     for q_name in q_set:
#         q0 = backup.get(q_name, queue.Queue())
#         func_name = 'get_' + q_name
#         manager.register(func_name, callable=lambda: q0)
#     # print(dir(manager))
#     del backup
#     # 启动Queue:
#     manager.start()
#     return manager
# 
# if __name__ == '__main__':
#     manager = reboot_manager()
#     manager.connect()
#     request_q = manager.get_request_q()
#     try:
#         while True:
#             print(time.asctime(time.localtime(time.time())))
#             print('existing queue:', q_set)
#             for q_name in q_set:
#                 func_name = 'get_' + q_name
#                 obj0 = getattr(manager, func_name, None)
#                 if obj0:
#                     q0 = obj0()
#                     print(q_name, 'qsize:', q0.qsize())
#                 else:
#                     print("error queue:", q_name)
#             print('\n')
#                     
#             if not request_q.empty():
#                 new_q = request_q.get()
#                 if isinstance(new_q, str) and new_q not in q_set:
#                     q_set.add(new_q)
#                     reboot_manager(manager)
#             
#             time.sleep(2)
#     except:
#         traceback.print_exc()
#     finally:
#         # 关闭:
#         manager.shutdown()
#         print('master exit.')
# =============================================================================
