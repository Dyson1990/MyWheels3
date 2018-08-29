# -*- coding: utf-8 -*-
# /usr/bin/python3
"""
--------------------------------
Created on %(date)s
@author: Dyson
--------------------------------
"""
import multiprocessing

"""
###############################################################################
特别注意：这个代码在spyder下运行时，输入进程的函数中的print会失效
###############################################################################
"""
class multiprocessing_manager(object):
    def __init__(self):
        pass
    
    def run_multiprocess(self, func, input_args, process_count=10):
        """
        目前只支持def func(input_args={}): 这种类型的函数
        input_args：为包含多个dict的list
        类似于[{input_args1}, {input_args2}, {input_args3}, {}， ..........]的Json格式
        func会读取每个dict进行运算
        
        关于lock线程锁，对同一个文件进行操作时需要用到，
        multiprocessing.Lock()需要在func中引用
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
            d.pop('process_lock')
        
        print("程序运行完毕！！！！")
        return output
        
# =============================================================================
#     def run_process(self, func, input_args, process_count=10):
#         """
#         此函数不支持控制进程数
#         """
#         
#         # 将需要传入的Json格式的参数存入队列
#         p_list = []
#         for args in input_args:
#             p = multiprocessing_class(func, args)
#             p.daemon = True
#             p.start()
#             p_list.append(p)
#         
#         # 等待其他进程结束
#         for p in p_list:
#             p.join()
#             
#         print("程序运行完毕！！！！")
#         
# class multiprocessing_class(multiprocessing.Process):
#     def __init__(self, func, input_args):
#         super().__init__()
#         self.func = func
#         self.input_args = input_args
#         
#     def run(self):
#         self.func(self.input_args)
# =============================================================================
        

def func0(input_args): 
    return input_args

if __name__ == '__main__':
    multiprocessing_manager = multiprocessing_manager()
    l1 = [ {j:j*j for j in range(i)} for i in range(3,8)]
    # l2 = multiprocessing_manager.run_process(func1, l1)
    print(multiprocessing_manager.run_multiprocess(func0, l1))
