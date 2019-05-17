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
import codecs

def split_row(df, col, sep):
    """
    以数据中某个符号将一行数据分割成多行数据
    df：DataFrame
    col：需要拆分的列名
    sep：分隔符
    
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

def comb_rows(df, groupby_col, sep, fill_na=''):
    """
    按某个符号合并为一行
    df：DataFrame
    groupby_col：合并行所依据的列名
    sep：分隔符
    fill_na：替换空值的字符
    
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
    if df.empty:
        return None
    
    df = (df
          .groupby(groupby_col)
          .aggregate(lambda ser: sep.join(ser.fillna(fill_na)))
          )
    df = df.reset_index()
    return df

def expand_json(df, cols, error='ignore'):
    """
    将DataFrame中的某几列的JSON格式的数据展开
    df：DataFrame
    cols：需要转换的列，需要传入列表。
    """
    if df.empty:
        return None
    
    if isinstance(cols, list):
        raise Exception('expand_json => 参数cols必须为列表')
    res = pd.DataFrame([])
    for i in df.index:
        nrows = None
        row_temp = df.loc[[i], [col0 for col0 in df.columns if col0 not in cols]]
        for col in cols:
            df_temp = pd.read_json(df.loc[i, col])
            
            # 检查JSON中的数据是否行数对应
            if nrows is None:
                nrows = df_temp.shape[0]
            elif not nrows == df_temp.shape[0]:
                if error == 'ignore':
                    print('WARNING：DataFrame行索引{}中的JSON数据行数不等，已忽视'
                          .format(i))
                    break
                else:
                    raise Exception('ERROR：DataFrame行索引{}中的JSON数据行数不等'
                                    .format(i))
            
            df_temp = df_temp.sort_index()
            # df_temp.index = np.arange(df_temp.shape[0])
            # 合并第一列后，row_temp
            if row_temp.shape[0] == df_temp.shape[0]\
               and (row_temp.index == df_temp.index).all():
                row_temp = pd.merge(row_temp
                                    , df_temp
                                    , how='inner'
                                    , left_index=True
                                    , right_index=True
                                    , sort=False
                                    , suffixes=['', '_dup'])
            else:
                row_temp = df_temp.apply(
                        lambda ser: pd.concat([ser
                                               , row_temp.iloc[0,:]
                                               ]
                                               , sort=False)
                            , axis=1)
                        
        row_temp.index = np.repeat(i, row_temp.shape[0])
        df = df.drop([i], axis=0)
        res = pd.concat([res, row_temp], sort=False)
    return res
    
    
    
if __name__ == '__main__':

#    df = pd.DataFrame({'A':{1:1,2:1,3:2,4:2,5:2}, 'B':{1:'b',2:None,3:'df',4:'2',5:'564'}})
#    print(df)
#    print(comb_rows(df, 'A', '/'))
    with codecs.open(r'C:\Users\gooddata\Desktop\test.csv', 'r', 'utf-8') as f:
        df = pd.read_csv(f)
    res = expand_json(df, ["project_info","info_test"])