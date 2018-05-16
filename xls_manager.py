# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: xls_manager.py
    @time: 2017/12/13 9:39
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

log_obj = set_log.Logger('xls_manager.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('xls_manager.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class xls_manager(object):

    def __init__(self):
        pass

    def dfs_to_excel(self, d, output_file):
        """
        将多个Exce工作表放在一个xls或者xlsx文件里
        :param d: {sheet name : df}
        :return:
        """
        writer = pd.ExcelWriter(output_file)

        for key in d:
            d[key].to_excel(writer, key, index=None)

        writer.save()


if __name__ == '__main__':
    xls_manager = xls_manager()