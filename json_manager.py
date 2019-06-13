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
    万能JSON转DataFrame函数
    """
    if isinstance(json_obj, (str, bytes)):
        json_obj = json.loads(json_obj)
    ori_df = pd.DataFrame(json_obj, dtype=np.object)
    ori_df = ori_df.set_index(data_key)
    df_pool = {'$': ori_df}
    res = {}
    while bool(df_pool):
        str_title, df_tmp = df_pool.popitem()
        type_func = lambda obj: isinstance(obj, (dict, list))
        json_dtype = df_tmp.apply(lambda col:col.apply(type_func).any(), axis=0)
        str_part = df_tmp.loc[:, json_dtype[json_dtype==False].index]
        if not str_part.empty:
            res[str_title] = str_part.copy()
        
        json_part = df_tmp.loc[:, json_dtype[json_dtype==True].index]
        
        if json_part.empty:
            continue
        
        for col in json_part.columns:
            ser = json_part.loc[:, col]
            if isinstance(col, int):
                ser_key = '{}[{}]'.format(str_title, col)
            else:
                ser_key = '{}.{}'.format(str_title, col)
                
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