# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: mysql_manager.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码
--------------------------------
"""
import traceback

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap

import pandas as pd
import numpy as np
from itertools import chain
from contextlib import closing
import random


# log_obj = set_log.Logger('mysql_manager.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_manager.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


eng_str = {
        'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
        , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
        }
# 选择数据库
dbname_str = {
        'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
        , 'mysql':"USE `{}`"
        }
np_type2sql_type = {
        np.dtype('int64'): sqlalchemy.Integer(),
        np.dtype('float64'): sqlalchemy.FLOAT(),
        np.dtype('O'): sqlalchemy.CHAR(),
        }

class sql_manager(object):

    def __init__(self):
        pass
    
    def connect(self, sql_args, sql, args=None):
        """
        最常用的连接MySQL的方式
        sql 可以是一条sql语句， 也可以是sql语句组成的列表
        :return: list
        """
        data = []
        
        sql_args = self.standardize_args(sql_args)

        try:
            # 使用哪种数据库，填入Oralce，MySQL等等
            engine = self.sql_engine(sql_args)
            
            with closing(engine.connect()) as conn:
                # 选择数据库
                global dbname_str
                db_dialect = sql_args['db_dialect'] 
                conn.execute(dbname_str[db_dialect].format(sql_args['dbname']))
                
                # 多条SQL语句的话，循环执行
                # rp short for ResultProxy
                if isinstance(sql,list):
                    for sql0 in sql:
                        rp = conn.execute(sql0)
                elif args:
                    rp = conn.execute(sql,args)
                else:
                    rp = conn.execute(sql)
                
                data = rp.fetchall()

                # 修改返回数据的类型
                if sql_args['data_type'] == 'list':
                    data = [list(t) for t in data]
                elif sql_args['data_type'] in ('DataFrame', 'dataframe'):
                    data = [list(t) for t in data] # 要求传入列表，不能是
                    data = pd.DataFrame(data, columns=rp.keys())
                else:
                    raise(Exception('输入的参数data_type有误！！！'))
                    
                return data
        except:
            print("数据库交互出错：%s" % traceback.format_exc())
            return None
    
    def create_table_like_df(self, sql_args, df_args, args=None):
        # 模仿dataframe的样式在数据库里简历表格
        # Column('id',Integer(),primary_key=True, autoincrement=True),
        
        # 检验所需参数是否齐全
        sql_args = self.standardize_args(sql_args)
        
        table_name = df_args['table_name']
        df = df_args['data']
        
        primary_key = df_args['primary_key'] if 'primary_key' in df_args else None
        
        if not isinstance(df, pd.core.frame.DataFrame):
            raise Exception('DataFrame类型错误！！！')

        try:
            # 使用哪种数据库，填入Oralce，MySQL等等
            engine = self.sql_engine(sql_args)

            # 初始化元数据表格
            metadata = sqlalchemy.schema.MetaData()
            metadata.reflect(engine, schema=sql_args['dbname'])
            
            # 初始化空白表格
            sql_table = sqlalchemy.Table(table_name, metadata)
            
            global np_type2sql_type
            # 为TABLE添加列映射
            for col in df.columns:
                sql_table.append_column(
                    sqlalchemy.Column(
                            col,
                            np_type2sql_type[df[col].dtype],
                            primary_key=(col==primary_key), # 此列是不是主键
                            ),
                    )
                    
            # 执行建表命令
            metadata.create_all(engine)
        except:
            print("数据库交互出错：%s" % traceback.format_exc())
        
        return None

    def insert_df_data(self, sql_args, df, table_name):
        # 从dataframe中将数据插入数据库
        sql_args = self.standardize_args(sql_args)

        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = self.sql_engine(sql_args)
        try:
            # 初始化会话
            mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
            session = mk_session()
            
            # 映射到oracle的schema中
            metadata = sqlalchemy.schema.MetaData()
            metadata.reflect(engine, schema=sql_args['dbname'].lower())
            base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
            base.prepare(engine, reflect=True)
            
            # 创建插入数据的队列
            for i in range(df.shape[0]):
                insert_values = df.iloc[i,:].to_dict()
                item = dict(base.classes.items())[table_name.lower()](**insert_values)
                session.add(item)
                
            print('数据库插入行数：', df.shape[0])
            # 没有发生错误，则提交提交结果
            session.commit()
        except:
            session.rollback()
            raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
        finally:
            session.close()
        
    def update_df_data(self, sql_args, df, table_name, fill_na=None, **col_args):
        """
        目前针对一个列做更新
        相当于
        update table_name set table_col = df_col where table_key = df_key
        df_key默认为df中的index
        
        col_args中必要的参数有
        df_col：输入的dataframe中，准备更新进入数据库的列
        table_col：数据库中需要更新数据的字段，相当于sql中的set后的数据
        table_key：数据库中的筛选列，相当于sql中的where后的数据
        """
        

        # 规范好参数，缺少参数则报错
        if 'df_col' not in col_args \
            or 'table_col' not in col_args \
            or 'table_key' not in col_args:
            raise Exception('df_col or table_col or table_key not given in update_df_data')
            
        table_col = col_args['table_col'].lower()
        table_key = col_args['table_key'].lower()
        df_col = col_args['df_col']
        df_key = col_args['df_key'] if 'df_key' in col_args else None
        
        # 检查输入数据的规范性，作为筛选字段，不能有重复值
        if df_key:
            if df[df_key].drop_duplicates().shape == df.shape[0]:
                raise Exception('duplicate values in update_df_data key column')
        else:
            if df.index.drop_duplicates().shape == df.shape[0]:
                raise Exception('duplicate index in update_df_data key column')
        
        table_name = table_name.lower()
        sql_args = self.standardize_args(sql_args)

        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = self.sql_engine(sql_args)
        try:
            # 初始化事务
            mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
            session = mk_session()
            
            # 映射到数据库中的schema
            metadata = sqlalchemy.schema.MetaData()
            metadata.reflect(engine, schema=sql_args['dbname'].lower())
            base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
            base.prepare(engine, reflect=True)
            
            # 定位到具体表格的类
            table_cls = getattr(base.classes, table_name)
            
            # 统一原表格（数据库）的格式
            table_col_cls = getattr(table_cls, table_col)
            table_key_cls = getattr(table_cls, table_key)
            
            table_df = pd.DataFrame(session.query(table_key_cls, table_col_cls).all())
            table_df = table_df.set_index(table_key)
            
            # 统一dataframe的格式
            if isinstance(df_key, str):
                df = df.set_index(df_key)
            
            # 筛选需要插入的数据
            target_df = pd.merge(df, table_df, how='left'
                                  , left_index=True, right_index=True
                                  , suffixes=['', '_'])
            table_col_new = table_col + '_' if table_col == df_col else table_col
            target_ser = target_df.loc[target_df[df_col] != target_df[table_col_new], df_col]
            
            # 将数据插入数据库
            for index0 in target_ser.index:
                query0 = session.query(table_cls).filter(table_key_cls==index0)
                query0.update({table_col_cls: target_ser.loc[index0]})
            
            print('数据库更新行数：', target_ser.shape[0])
            # 没有发生错误，则提交提交结果
            session.commit()
        except:
            session.rollback()
            raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
        finally:
            session.close()

    def standardize_args(self, sql_args):
        # 检查所需参数是否都存在

        if not isinstance(sql_args, dict):
            raise Exception("sql_args格式错误！！！")
        
        if sql_args['db_dialect'].lower() == 'oracle':
            needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'sid', 'dbname']
        elif sql_args['db_dialect'].lower() == 'mysql':
            needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'dbname']
        
        check_args = [s for s in needed_args if s not in sql_args]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

        if 'port' not in sql_args and sql_args['db_dialect'].lower() == 'oracle':
            sql_args['port'] = '1521'
        if 'port' not in sql_args and sql_args['db_dialect'].lower() == 'mysql':
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
            
        sql_args['db_dialect'] = sql_args['db_dialect'].lower()
        sql_args['db_driver'] = sql_args['db_driver'].lower()
            
        return sql_args
    
    def sql_engine(self, sql_args):
        global eng_str
        db_dialect = sql_args['db_dialect']
        engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args))
        return engine
    




if __name__ == '__main__':
    sql_manager = sql_manager()
    
    # 本地测试Oracle参数
    sql_args = {
        'db_dialect': 'oracle'
        , 'db_driver': 'cx_Oracle'
        , "host": "localhost"
        , "user": "Dyson"
        , "password": "122321"
        , 'sid': 'XE'
        , 'dbname': 'HR'
        , 'data_type': 'DataFrame'
    }
    # print(sql_manager.connect('SELECT JOB_ID, MIN_SALARY, COMMIT FROM JOBS', sql_args))
   
    # 测试本地MySQL参数
# =============================================================================
#     sql_args = {
#         'db_dialect': 'MySQL'
#         , 'db_driver': 'pymysql'
#         , "host": "localhost"
#         , "user": "Dyson"
#         , "password": "122321"
#         , 'dbname': 'sakila'
#         , 'data_type': 'DataFrame'
#     }
# =============================================================================
    # print(sql_manager.connect('SELECT * FROM `actor` LIMIT 20', sql_args))
    
    
# =============================================================================
#     df = pd.DataFrame({"job_id":{1:'{}'.format(random.randint(1,1000)), 2:'{}'.format(random.randint(1,1000))}
#                       ,"job_title":{1:'WTF',2:'WTF'}})
# =============================================================================
    df = pd.DataFrame({"job_id":{1:'AD_VP', 2:'AD_ASST'}
                      ,"commit":{1:'NEW{}'.format(random.randint(1,1000)),2:'NEW{}'.format(random.randint(1,1000))}})
    sql_manager.update_df_data(sql_args, df, 'JOBS'
                               , df_col='commit', table_col='commit'
                               , df_key='job_id', table_key='job_id')

