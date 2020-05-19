# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:41:35 2019

@author: gooddata
"""
import pandas as pd
import numpy as np
import json

def multi_json2dataframes(json_obj, data_key='_id'):
    """
    万能JSON转DataFrame函数(努力中)
    json_obj: json格式的对象，可以是字典、列表、json字符串
    data_key：拆开JSON数据后，用来连接不同子表的键
    """
    # 如果是以字符串的形式传入的JSON数据，则需要
    if isinstance(json_obj, (str, bytes)):
        json_obj = json.loads(json_obj) 
        
    # 将初始数据转化为dataframes
    ori_df = pd.DataFrame(json_obj, dtype=np.object)
    
    # 包含JSON格式的数据，不适合作为key使用
    type_func = lambda obj: isinstance(obj, (dict, list))
    if ori_df.loc[:, data_key].apply(type_func).any():
        raise(Exception('{}列包含JSON格式的数据，不适合作为key使用'.format(data_key)))
    
    # 因为之后需要将不同维度的
    ori_df = ori_df.set_index(data_key)
    df_pool = {'$': ori_df} # 构建待处理的DataFrame池
    res = {}
    while bool(df_pool):
        # str_title是其对应的DataFrame中数据的json_path
        str_title, df_tmp = df_pool.popitem()
        
        # 判断一列中是否有JSON格式的数据
        json_dtype = df_tmp.apply(lambda col:col.apply(type_func).any(), axis=0)
        
        # 分离出不是JSON格式的列，保存下来
        str_part = df_tmp.loc[:, json_dtype[json_dtype==False].index]
        if not str_part.empty:
            str_part.index.name = data_key
            res[str_title] = str_part.copy()
        
        # 分离出是JSON格式的列，放回df_pool中
        json_part = df_tmp.loc[:, json_dtype[json_dtype==True].index]
        
        
        if json_part.empty: # 避免将空的DataFrame放入df_pool
            continue
        
        # 这里的ser_key的构造还有待商榷
        for col in json_part.columns:
            ser = json_part.loc[:, col]
            ser = ser.dropna() # 空数据没必要保存
            
            # 暂时不考虑同一阶JSON中字典与列表混用的情况
            type_detect = ser.apply(lambda obj: type(obj)).unique() 
            if len(type_detect) > 1:
                res['__unfinished_json__'] = ser.copy()
                continue
            
            ser_key = '{}.{}'.format(str_title, col)
            
            # 这里还有改良空间， 暂不考虑列表包含列表的情况     
            if type_detect[0] == list:  
                # series中没有什么好函数做索引与值的运算，所以转为DataFrame
                ser_df = ser.to_frame().reset_index() 
                """
                由于这里的ser中，每个值都是一个列表，并且不附带data_key
                我这里的做法，是把每个列表都先转为DataFrame，更改索引后，再合并
                """
                index_func = lambda row: pd.Index([row.iloc[0]]*len(row.iloc[-1]))
                list_func = lambda row: (pd.DataFrame(row.iloc[-1])
                                           .set_index(index_func(row)))
                """
                这里ser_df.apply出来以后，是个series。
                我不想附个新的变量了，就直接放进了concat里面
                """
                ser_df = pd.concat(ser_df.apply(list_func, axis=1) 
                                         .tolist()
                                  )
                df_pool[ser_key] = ser_df.copy()
                ser_df = None
            else:
                df_pool[ser_key] = pd.DataFrame(ser.to_dict()).T
    return res

def dataframes2multi_json(ori_df, output_type=str):
    """
    将DataFrame中的JSON格式
    """
    df = ori_df.apply(lambda col: col.apply(__load_json), axis=0)
    
    if output_type==str:
        res = df.to_dict(orient = 'records')
        return json.dumps(res, indent=2, ensure_ascii=False)
    elif output_type==list:
        return df.to_dict(orient = 'records')
    elif output_type==dict:
        return df.to_dict(orient = 'index')
    
def __load_json(s):
    try:
        return json.loads(s)
    except:
        return s 


if __name__ == '__main__':
    pass