# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: Logistic_regression.py
    @time: 2017/12/28 16:32
--------------------------------
"""
import sys
import os
import pandas as pd
import numpy as np

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger('Logistic_regression.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('Logistic_regression.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class Logistic_regression(object):

    def __init__(self):
        pass

    def gradient_ascent(self, df, class_col):
        alpha = 0.001
        max_cycles = 500

        target_col = df[class_col].copy()
        df = df.drop([class_col,], axis=1)
        for i in range(max_cycles):


if __name__ == '__main__':
    Logistic_regression = Logistic_regression()