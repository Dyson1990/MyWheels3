# -*- coding:utf-8 -*-  
#/usr/bin/python3
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: thread_template.py
--------------------------------
"""
import time
import threading
import queue


class threading_template(threading.Thread):

    def __init__(self, queue, lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock

    def run(self):
        while not self.queue.empty():
            args = self.queue.get()
            self._thread0(args)
            self.queue.task_done()


    def _thread0(self, args):

        start_time = time.time()


        print("总耗时： %s" %(time.time() - start_time))

if __name__ == '__main__':

    lock = threading.Lock()
    queue = queue.Queue()
    
    # main_proess = main_proess(queue, lock)
    arg_list = []
    for arg in arg_list:
        queue.put(arg)
    
    # 10个线程
    for i in range(10):
        t = threading_template(queue, lock)
        t.setDaemon(True)
        t.start()
        
    queue.join()
        
    time.sleep(36000)
    
