# -*- coding: utf-8 -*-
# /usr/bin/python3
"""
--------------------------------
Created on %(date)s
@author: Dyson
--------------------------------
"""
import os
import sys
import pandas as pd
import numpy as np

class dataframe_manager(object):

    def __init__(self):
        pass
    
    def split_row(self, df, col, sep):
        """
        以数据中某个符号将一行数据分割成多行数据
        例如：
        1 a,a
        2 b,c,d
        ==>
        1 a
        1 a
        2 b
        2 c
        2 d
        """
        if df.empty:
            return None
        
        # 将col列分割后， 生成新的列，
        splitted_col = (df[col]
                        .str
                        .split(sep, expand=True)
                        )
        stack_col = (splitted_col
                     .stack()
                     .reset_index(level=1, drop=True)
                     .rename(col)
                     )
        
        # 删除旧的col列，将前面生成的col列组合进去
        df = (df
              .drop(col, axis=1)
              .join(stack_col)
              )# 默认是左连接
        
        return df
    
    def comb_rows(self, df, groupby_col, sep, fill_na=''):
        """
        按某个符号合并为一行
        例如：
        1 a
        1 a
        2 b
        2 c
        2 d
        ==>
        1 a|a
        2 b|c|d
        """
        df = (df
              .groupby(groupby_col)
              .aggregate(lambda ser: sep.join(ser.fillna(fill_na)))
              )
        df = df.reset_index()
        return df
    
if __name__ == '__main__':
    dataframe_manager = dataframe_manager()
    df = pd.DataFrame({'A':{1:1,2:1,3:2,4:2,5:2}, 'B':{1:'b',2:None,3:'df',4:'2',5:'564'}})
    print(df)
    print(dataframe_manager.comb_rows(df, 'A', '/'))
