# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:42:59 2020

@author: gooddata
"""

import pandas as pd
import codecs
import os
import sqlalchemy
import traceback
import datetime
import random
import numpy as np
import time

dbname_str = {
        'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
        , 'mysql':"USE `{}`"
        }
def __standardize_args(sql_args):
    # 检查所需参数是否都存在，规范输入的一些参数
    
    if not isinstance(sql_args, dict):
        raise Exception("sql_args格式错误！！！")
        
    # 规范输入的大小写
    sql_args['db_dialect'] = sql_args['db_dialect'].lower()
    sql_args['db_driver'] = sql_args['db_driver'].lower()
    
    # 不同的数据库，需要的参数不同
    if sql_args['db_dialect'] == 'oracle':
        needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'sid', 'dbname']
        
        # Oracle的数据类型比较特殊
        global np_type2sql_type,sql_type2np_type,np_type2oracle_type,oracle_type2np_type
        np_type2sql_type = np_type2oracle_type
        sql_type2np_type = oracle_type2np_type
        
    elif sql_args['db_dialect'] == 'mysql':
        needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'dbname']
    
    # 缺少参数则报错
    check_args = [s for s in needed_args if s not in sql_args]
    if check_args:
        raise Exception("缺少数据库参数：%s" % '，'.join(check_args))
    
    # 规定默认的参数的值 ##################################################
    if 'port' not in sql_args and sql_args['db_dialect'] == 'oracle':
        sql_args['port'] = '1521'
    if 'port' not in sql_args and sql_args['db_dialect'] == 'mysql':
        sql_args['port'] = '3306'
    if 'charset' not in sql_args:
        sql_args['charset'] = 'utf8'
        """
        这种错误很有可能是SQL驱动不完整
        也可能是数据库的编码与申请的编码不符
        1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 484")
        """
    if 'method' not in sql_args:
        # 没有参数传入，则使用fetchall
        sql_args['method'] = None
    if 'data_type' not in sql_args:
        sql_args['data_type'] = 'list'
    #######################################################################
    return sql_args

def __sql_engine(sql_args):
    # 编辑salalchemy中的数据库参数字符串
    global eng_str
    db_dialect = sql_args['db_dialect']
    engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args))#, echo=True)
    return engine

eng_str = {
        'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
        , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
        }

sql_args = {
    'db_dialect': 'MySQL'
    , 'db_driver': 'pymysql'
    , "host": "192.168.50.190"
    , "user": "usr_lyb"
    , "password": "qy123456"
    , 'dbname': 'pdb_usr_lyb'
    , 'data_type': 'DataFrame'
}
sql_args = __standardize_args(sql_args)
mysql_engine = __sql_engine(sql_args)

def float_gen(min0=100, max0=10000000, chunksize=10000):
    while True:
        yield (max0 - min0) * np.random.random(chunksize) + min0
        
def string_gen(str_len=10, chunksize=10000):
    func = lambda row: ''.join([chr(e) for e in row])
    while True:
        str_mat = np.random.randint(65, 123, size=(str_len, chunksize))
        yield np.apply_along_axis(func, 0, str_mat)
        
def date_gen(min0=946656000.0, max0=datetime.datetime.now().timestamp(), chunksize=10000):
    func = lambda e: datetime.datetime.fromtimestamp(e)
    while True:
        date_arr = (max0 - min0) * np.random.random(chunksize) + min0
        yield np.apply_along_axis(func, 0, [date_arr,])
        
        

if __name__ == '__main__':
    row_num = 100000000
    chunksize = 10000
    
    while row_num > 0:
        df = pd.DataFrame({
            'float': next(float_gen(chunksize=chunksize))
            , 'string': next(string_gen(chunksize=chunksize))
            , 'date1': next(date_gen(chunksize=chunksize))
            , 'date2': next(date_gen(chunksize=chunksize))
            # , 'id': [random.randint(1, 20) for i in range(chunksize)]
            })
        df.to_sql('random_data', mysql_engine, if_exists='append')
        row_num = row_num - chunksize
        print('running', datetime.datetime.now())
        # with codecs.open('random_data.csv', 'a', 'utf-8') as fp:
        #     df.to_csv(fp, index=0)  
        # break