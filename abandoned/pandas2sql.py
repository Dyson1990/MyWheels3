# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: pandas2sql.py
    @time: 2017/9/11 13:46
--------------------------------
"""
import random
import sys
import os

import pandas as pd
import sqlalchemy
import time

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')


class pandas2sql(object):
    def __init__(self):
        pass

    def sql_engine(self, **kwargs):
        DB_CONNECT_STRING = 'mysql+pymysql://{user}:{passwd}@{host}/{db}?charset=utf8'\
            .format(user=kwargs['user'],passwd=kwargs['password'],host=kwargs['host'],db=kwargs['database'])
        engine = sqlalchemy.create_engine(DB_CONNECT_STRING, echo=True)
        return engine

    def df2sql(self, df, tablename, user, passwd, host, database):
        
        engine = self.sql_engine(user=user,password=passwd,host=host,database=database)
        pd.io.sql.to_sql(df, tablename, engine, if_exists='append', chunksize=1000, index=False)
        return


if __name__ == '__main__':
    pandas2sql = pandas2sql()
    df = pd.DataFrame({'id':random.randint(0,int(time.time())),'row0': time.time(), 'row1': random.random()}, index=[0, ])
    pandas2sql.df2sql(df,'testtable','Dyson','122321','localhost','spider')