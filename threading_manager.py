# -*- coding: utf-8 -*-
# /usr/bin/python3
"""
--------------------------------
Created on %(date)s
@author: Dyson
--------------------------------
"""
import threading
import queue

class threading_manager(object):
    def __init__(self):
        pass
    
    def run_threading(self, func, input_args, thread_count=3):
        """
        目前只支持def func(input_args, lock): 这种类型的函数
        input_args：为包含多个dict的list
        类似于[{input_args1}, {input_args2}, {input_args3}, {}， ..........]的Json格式
        func会读取每个dict进行运算
        
        lock：是线程锁，对同一个文件进行操作时需要用到
        return： 返回的也是类似于input_args的格式
        """
        lock = threading.Lock()
        input_queue = queue.Queue()
        output_queue = queue.Queue()
        
        # 将input_args中的每个字典编号，为了防止输出结果时候顺序混乱
        input_args = {i:input_args[i] for i in range(len(input_args))}
        # 将需要传入的Json格式的参数存入队列
        for key in input_args:
            d = {'thread_id':key
                 , 'input_args': input_args[key]}
            input_queue.put(d)
            
        for i in range(thread_count):
            t = threading_class(func, input_queue, output_queue, lock)
            """
            setDaemon
            主线程A启动了子线程B，
            调用b.setDaemaon(True)，
            则主线程结束时，会把子线程B也杀死
            """
            t.setDaemon(True)
            t.start()
            
        input_queue.join() # 实际上意味着等到队列为空，再执行别的操作
        
        # 读取数据
        result = {}
        while not output_queue.empty():
            output = output_queue.get()
            result[output['thread_id']] = output['output']
            
        print("程序运行完毕！！！！")
        return result.values()
        
# 用来定义threading的类
class threading_class(threading.Thread):
    def __init__(self, thread0, input_queue, output_queue, lock):
        threading.Thread.__init__(self)
        self.input_queue = input_queue
        self.lock = lock
        self.thread0 = thread0
        self.output_queue = output_queue

    def run(self):
        while True:
            input_args = self.input_queue.get() # 取得输入参数
            thread_id = input_args['thread_id']
            input_args = input_args['input_args']
            output = self.thread0(input_args, self.lock) # 运行函数
            output = {'thread_id': thread_id
                      , 'output': output}
            self.output_queue.put(output) # 存入输出结果
            self.input_queue.task_done() # input_queue中队列读取完毕以后退出循环

def func0(input_args, lock): 
    input_args['ser'].str.extract('({})'.format('|'.join(input_args['re_str'])))
    return 

if __name__ == '__main__':
    threading_manager = threading_manager()
    import time
    import pandas as pd
    import numpy as np
    ser = pd.Series(np.random.rand(1200000),dtype=np.str)
    
    re_str_list = list('1234567890QAZXSWEDCVFRTGBNHYUJMKILOP'*800)
    
    start_time = time.time()
    l = []
    for i in range(10):
        l.append(func0({'ser': ser,'re_str': re_str_list[i: i*800]}, 'lock'))
    print('单线程',time.time() - start_time)
    
    start_time = time.time()
    l1 = []
    for i in range(10):
        l1.append({'ser': ser,'re_str': re_str_list[i: i*800]})
    
    l2 = threading_manager.run_threading(func0, l1)
    print('3线程',time.time() - start_time)
