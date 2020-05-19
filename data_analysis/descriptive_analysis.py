# -*- coding:utf-8 -*-  
#/usr/bin/python3
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: descriptive_analysis.py
    @time: 18-5-21 下午3:40
--------------------------------
"""
import sys
import os
import numpy as np
import pandas as pd
import scipy.stats

#import set_log  

#log_obj = set_log.Logger('descriptive_analysis.log', set_log.logging.WARNING,
#                         set_log.logging.DEBUG)
#log_obj.cleanup('descriptive_analysis.log', if_cleanup = True)  # 是否需要在每次运行程序前清空Log文件


def get_data(df):
    return df

def normal_distribution(start=0, end=10, size=10):
    # 正态分布
    return np.random.normal(start, end, size=size)

def uniform_distribution(start=0, end=10, size=10):
    # 均匀分布
    return np.random.randint(start, end, size=size)

def data_characteristics(df, col_name):

    ser = df[col_name]

    res = {}

    res["均值"] = np.mean(ser)
    res["中位数"] = np.median(ser)
    res["众数"] = scipy.stats.mode(ser).mode[0]
    res["极差"] = np.ptp(ser)
    res["方差"] = np.var(ser)
    res["标准差"] = np.std(ser)

    return res

def z_score(df, col_name):

    ser = df[col_name]

    return df[col_name].apply(lambda x: (x - np.mean(ser)) / np.std(ser))

def correlation(df, col_name1, col_name2):

    data = np.array([df[col_name1], df[col_name2]])

    return {"协方差": np.cov(data, bias=1), # 参数bias=1便是结果需要除以N， 否则只计算了分子部分
            "相关系数": np.corrcoef(data)[0,-1]
            }


if __name__ == '__main__':

    df = pd.DataFrame(np.arange(10).reshape(5,2), columns=["A","B"], index=range(5))
    df.loc[0, "B"] = 3
    print(df)
    print(data_characteristics(df, "B"))
    print(correlation(df, "A", "B"))