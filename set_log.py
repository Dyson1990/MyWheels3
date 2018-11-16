# -*- coding:utf-8 -*-

"""
@version: beta2
@author: Dyson
@file: set_log.py
@time: 2016/7/28 17:46
@info: 个人常用代码
"""
import logging,os
import ctypes
import sys


FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

STD_OUTPUT_HANDLE= -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

class Logger:
    def __init__(self, path,clevel = logging.DEBUG,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [Time_Consuming: %(relativeCreated)d毫秒] => \n %('
                                'message)s', '%Y-%m-%d %H:%M:%S')
        #设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message,color=FOREGROUND_YELLOW):
        set_color(color)
        self.logger.warn(message)
        set_color(FOREGROUND_WHITE)

    def error(self,message,color=FOREGROUND_RED):
        set_color(color)
        self.logger.error(message)
        set_color(FOREGROUND_WHITE)

    def critical(self,message):
        self.logger.critical(message)
        
    def cleanup(self,file_name,if_cleanup = True):
        #file_path = os.path.abspath(file_name)
        if os.path.exists(file_name) and if_cleanup:
            with open(file_name, 'w') as f:
                f.truncate()



if __name__ =='__main__':
    log_path = r'C:\Users\gooddata\test.log'
    log_obj = Logger(log_path)
    log_obj.cleanup(log_path, if_cleanup=False) # 是否需要在每次运行程序前清空Log文件
    # logyyx = Logger('yyx.log',logging.WARNING,logging.DEBUG)
    # logyyx.debug('一个debug信息')
    # logyyx.info('一个info信息')
    # logyyx.war('一个warning信息')
    # logyyx.error('一个error信息')
    # logyyx.cri('一个致命critical信息')
