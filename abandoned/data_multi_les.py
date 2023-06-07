# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 09:05:25 2020

@author: gooddata






les means:
    load
    execute
    save






"""

import pandas as pd
import numpy as np
import re
import time
import multiprocessing
import os
import datetime
import psutil
import random
import json
import codecs

pd.set_option('mode.chained_assignment','raise')

def pre_load(args):
    """
    将数据源中的数据读入data_q

    Parameters
    ----------
    args : TYPE
        多进程参数.

    Returns
    -------
    None.

    """
    data_q = args['data_q']
    file_path = args['file_path']
    cols = args['cols']
    row_count = args['row_count']
    
# =============================================================================
#     gen = pd.read_csv(file_path
#                       , chunksize=1
#                       , dtype=np.str
#                       # , nrows=100
#                       )
#     for chunk in gen:
#         for col0 in cols:
#             data_q.put(chunk.loc[:, col0].iloc[0])
#             row_count.value = row_count.value + 1
# =============================================================================
    
    # 以下是测试数据
    tmp_arr = np.random.random([100000,10])
    for row0 in range(tmp_arr.shape[0]):
        data_q.put(tmp_arr.iloc[row0, 0])
        row_count.value = row_count.value + 1
    

    args['trigger'].value = False

def save_data(args):
    """
    将res_q中的数据输出至文件
    Parameters
    ----------
    args : TYPE
        多进程参数.

    Returns
    -------
    None.

    """
    res_path = args['res_path']
    res_q = args['res_q']
    save_size = args['save_size']
    res_q_wait = args['res_q_wait']
    
    output = []
    start_time = time.time()
    while True:   # not res_q.empty() or trigger.value:
        row = res_q.get()
        # print(os.getpid(), 'save_data进程取得数据：', row)
        output.append(row)
        
        if len(output) > save_size/4 or (res_q.empty() and len(output) > 0):
            (pd.DataFrame(output, columns=['字符串', '匹配关系', '结果', '最佳匹配', '最佳匹配县码'])
               .to_csv(res_path
                       , mode='a'
                       , encoding='utf_8_sig'
                       , header=not os.path.exists(res_path)
                       )
            )
            
            print('-' * 30 + '\n'
                  , datetime.datetime.now()
                  , os.getpid()
                  , 'save_data进程存入{}条数据耗时{}'.format(len(output), time.time()-start_time)
                  , '\n' + '-' * 30
                  )
            
            output.clear()
            if not res_q.full():
                time.sleep(res_q_wait)
            start_time = time.time()
            
        time.sleep(0.03)
            

def proc_data(args):
    """
    从data_q读入数据，处理完毕后输出至res_q

    Parameters
    ----------
    args : TYPE
        多进程参数.

    Returns
    -------
    None.

    """
    data_q = args['data_q']
    trigger = args['trigger']
    proc_list = args['proc_list']
    pid = os.getpid()
    proc_list.append(pid)
    
    
    while not data_q.empty() or trigger.value:
        chunk = data_q.get()
        # print(os.getpid(), 'proc_data进程取得数据：', str0)
# =============================================================================
#         res = exec_re(chunk, re_df)
#         res_q.put(res)
# =============================================================================
        
        # 以下是测试
        res_q.put([chunk.sum()])
        
        if data_q.empty():
            time.sleep(3)

        
    proc_list.remove(pid)
        
def monitor(args):
    data_q = args['data_q']
    res_q = args['res_q']
    proc_list = args['proc_list']
    row_count = args['row_count']
    start_time = time.time()
    while True:
        time_used = time.time() - start_time
        if time_used > 3600:
            time_plus = time_used * random.random() * 0.005
        else:
            time_plus = 0
        time.sleep(10 + time_plus)
        print()
        print(datetime.datetime.now())
        print('正在处理数据的进程有：', proc_list)
        print('已经加载数据量：', row_count.value)
        print('此时待处理数据队列中有（个）', data_q.qsize())
        print('此时处理完的数据队列中有（条）', res_q.qsize())
        print('此时内存占用：', psutil.virtual_memory().percent)
        print('此时CPU占用：', psutil.cpu_percent(percpu=True))
        print()
        
    
if __name__ == '__main__':
    """
    正则表达式的计算输入“计算密集型”操作，所以优先关注“CPU占用率”
    """
    json_args = {
        "file_path":"C:\\Users\\gooddata\\Desktop\\地址变更样例数据.csv",
        "target_cols":[
            "ALTBE",
            "ALTAF"
        ],
        "res_path":"C:\\Users\\gooddata\\Desktop\\res.csv",
        "re_file_path":".\\行政区划正则表达式20200726.xlsx",
        "proc_count":5,
        "save_size":1000,
        "res_q_wait":20
    }
    
    file_path = os.path.abspath(json_args['file_path']) # 数据源文件路径
    target_cols = json_args['target_cols'] # 数据源文件中需要处理的字段名
    res_path = os.path.abspath(json_args['res_path']) # 结果输出路径
    re_file_path = os.path.abspath(json_args['re_file_path'])
        
######################### 必要参数 #############################################
    proc_count = json_args['proc_count'] # 用来处理数据的进程数，CPU占用率过高（每个都接近100%）则需要减少
    save_size = json_args['save_size'] # 内存中最大保存结果记录条数，内存占用率过高则需要减少；“处理完的数据队列”容易达到上限，需要增加
    res_q_wait = json_args['res_q_wait'] # 结果记录条数不够多时的等待时间，“处理完的数据队列”容易满的时候，需要减少；若经常为0则需要增加
    
    data_q = multiprocessing.Manager().Queue(proc_count)
    res_q = multiprocessing.Manager().Queue(save_size)
    proc_list = multiprocessing.Manager().list()
    row_count = multiprocessing.Manager().Value(int, 0)
    
    trigger = multiprocessing.Manager().Value(bool, True)

######################### 必要参数 #############################################

    
    args = {'proc_list': proc_list
            , 'data_q': data_q
            , 'res_q': res_q
            , 'row_count': row_count
           }
    monitor_task = multiprocessing.Process(target=monitor, args=(args,))
    monitor_task.start()
    
    args = {'data_q': data_q
            , 'file_path': file_path
            , 'cols': target_cols
            , 'trigger': trigger
            , 'row_count': row_count
            }
    pre_task = multiprocessing.Process(target=pre_load, args=(args,))
    pre_task.start()
    
    args = {'res_path': res_path
            , 'res_q': res_q
            , 'trigger': trigger
            , 'save_size': save_size
            , 'res_q_wait': res_q_wait
            }
    save_task = multiprocessing.Process(target=save_data, args=(args,))
    save_task.start()
    
    task_list = []
    for i0 in range(proc_count):
        args = {'data_q': data_q
                , 'trigger': trigger
                , 'res_q': res_q
                , 'proc_list': proc_list
                }
        task = multiprocessing.Process(target=proc_data, args=(args,))
        task_list.append(task)
    
    for task in task_list:
        task.start()
    
    pre_task.join()

    for task in task_list:
        task.join()
        
    save_task.join()
    monitor_task.join()
    
# =============================================================================
#     sample.loc[:, 'res'] = sample['ALTBE'].apply(lambda s: exec_re(s, re_df))
# 
#     with pd.ExcelWriter(r'C:\Users\gooddata\Desktop\re_test%s.xlsx' %time.time()) as writer:  
#         sample[['ALTBE','res']].to_excel(writer, sheet_name='res')
#         pd.Series(re_df).to_excel(writer, sheet_name='re_str')
# =============================================================================

