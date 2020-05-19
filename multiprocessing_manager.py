# -*- coding: utf-8 -*-
# /usr/bin/python3
"""
--------------------------------
Created on %(date)s
@author: Dyson
--------------------------------
"""
import multiprocessing
import requests_manager
import time
import re
import codecs
import os
import json
import traceback


"""
###############################################################################
特别注意：这个代码在spyder下运行时，输入进程的函数中的print会失效
###############################################################################
"""
#class multiprocessing_manager(object):
#    def __init__(self):
#        pass
    
def run_multiprocess(func, input_args, process_count=10):
    """
    目前只支持def func(input_args={}): 这种类型的函数
    input_args：为包含多个dict的list
    类似于[{input_args1}, {input_args2}, {input_args3}, {}， ..........]的Json格式
    func会读取每个dict进行运算
    
    关于lock线程锁，对同一个文件进行操作时需要用到，
    return： 返回的也是类似于input_args的格式
    """
    # 为每个进程分配一个进程锁
    lock = multiprocessing.Manager().Lock()
    for d in input_args:
        d.update({'process_lock': lock})
        
    pool = multiprocessing.Pool(process_count)
    map_res = pool.map_async(func, input_args)
    pool.close() # 关闭进程池，不再接受新的进程
    pool.join() # 主进程阻塞等待子进程的退出
    
    # 将进程锁从结果中剔除
    output = map_res.get()
    for d in output:
        if 'process_lock' in d:
            d.pop('process_lock')
    
    print("程序运行完毕！！！！")
    return output
        

def get_data(arg_dict):
    try:
        url = arg_dict['url']
        lock = arg_dict['process_lock']
        
        html = requests_manager.get_html(url)
        time.sleep(1)
        
        ent_name = re.search('<span itemprop=\'name\'><.*?>(.*?)</a>', html).group(1)

        res_path = 'res.txt'
        with lock:
            with codecs.open(res_path, 'a', 'utf-8') as f:
                f.write(ent_name + '\n')
        
    except:
        with lock:
            with codecs.open('http_error.log', 'a', 'utf-8') as f:
                f.write(url + '\n' + traceback.format_exc() + '\n')
    finally:
        return arg_dict


if __name__ == '__main__':
    with codecs.open('firm.txt', 'r', 'utf-8') as f:
        urls = f.read().split('\r\n')
    urls = [{'url': url} for url in urls]
    run_multiprocess(get_data, urls, process_count=10)
