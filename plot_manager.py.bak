# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: plot_manager.py
    @time: 2017/12/27 8:58
--------------------------------
"""
import sys
import os

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger('plot_manager.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('plot_manager.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class plot_manager(object):

    def __init__(self):
        pass

    def two_axis(self, df, ax_cols1, ax_cols2, **kwargs):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        if 'x_axis' in kwargs:
            df = df.set_index(kwargs['x_axis'])

        print df
        for c in ax_cols1:
            color = ax_cols1[c] if isinstance(ax_cols1, dict) else 'r'
            ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))  # 设置时间标签显示格式
            # plt.xticks(pd.date_range(df.index[0], df.index[-1]))
            ser = df[c]
            # print [ser.index[i] for i in range(ser.shape[0]) if i%5==0]
            ax1.set_xticks([ser.iloc[i] for i in range(ser.shape[0]) if i%5==0])
            ser = ser.fillna(0)
            ax1.plot(ser, color=color)


        # ax2 = ax1.twinx()  # 创建第二个坐标轴
        # for c in ax_cols2:
        #     color = ax_cols2[c] if isinstance(ax_cols2, dict) else 'b'
        #     # ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))  # 设置时间标签显示格式
        #     plt.xticks()
        #     ax2.plot(df[c], color=color)
        fig.autofmt_xdate()
        plt.savefig('text.png')


if __name__ == '__main__':
    plot_manager = plot_manager()
    # df = pd.DataFrame(np.array([4,3,50,6,7,80,4,3,122]).reshape(-1,3), columns=['c1', 'c2', 'c3'])
    # print df
    # plot_manager.two_axis(df, ['c1','c2'], ['c3',])
    df = pd.read_excel('book1.xlsx')
    plot_manager.two_axis(df, [u'主力净流入净额5日累计', u'主力净流入净额10日累计',u'主力净流入净额20日累计'], [u'收盘价', ], x_axis=u'日期')