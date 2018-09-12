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


# log_obj = set_log.Logger('mysql_manager.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_manager.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


eng_str = {
        'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
        , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/?charset={charset}"
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
    
    def connect(self,sql, sql_args, args=None):
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
    
    def create_table_like_df(self, df_args, sql_args, args=None):
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

    def insert_df_data(self, df, table_name, sql_args):
        # 从dataframe中将数据插入数据库

        sql_args = self.standardize_args(sql_args)
        
        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = self.sql_engine(sql_args)
        
        # 映射到oracle的schema中
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(engine, schema=sql_args['dbname'])

        # print(metadata.tables.keys())
        base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
        base.prepare(engine, reflect=True)
# =============================================================================
#         print(dir(base.classes))
#         print(dir({}))
#         print(base.classes.keys())
# =============================================================================
        try:
            # 初始化会话
            mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
            session = mk_session()
            
            # 查询操作
            result = session.query(base.classes.jobs).all()
            print(result)

# =============================================================================
#             insert_args = {'COMMIT':'WTF'}
#             item = base.classes.jobs(**insert_args)
#             session.add(item)
# =============================================================================
            
            session.commit()
        except:
            session.rollback()
            raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
        finally:
            session.close()
        
        
        
    def update_df_data(self, df, table_name, index_name, sql_args, fill_na=None):
        """
        举例说明
        df:
               A      B      C
        1   23.0  213.0    NaN
        2  434.0    NaN  213.0

        sql:
        UPDATE  
        SET `C` = CASE `A` 
        WHEN '1' THEN '0.0'
        WHEN '2' THEN '213.0'
        END,
        `A` = CASE `A` 
        WHEN '1' THEN '23.0'
        WHEN '2' THEN '434.0'
        END,
        `B` = CASE `A` 
        WHEN '1' THEN '213.0'
        WHEN '2' THEN '0.0'
        END
        WHERE `A` IN ('1','2')

        """
        # 是否需要补全缺失值
        if fill_na != None:
            df = df.fillna(fill_na)


        sql = "UPDATE %s \n SET " % table_name
        d = df.to_dict()
        #print d
        sql_list = []
        for key in d:
            d0 = d[key]
            l = ["WHEN '%s' THEN '%s'" % (key0, d0[key0]) for key0 in d0]
            sql1 = "`%s` = CASE `%s` \n%s" % (key, index_name, '\n'.join(l))
            sql_list.append(sql1 + '\nEND')
        sql = sql + ',\n'.join(sql_list) + "\nWHERE `%s` IN (%s)" %(index_name, ','.join(["'%s'" %s for s in df.index.tolist()]))
        
        print(sql)

        self.connect(sql, sql_args)
        print("UPDATE successfully !")

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
   
# =============================================================================
#     # 测试本地MySQL参数
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
    
    
    df = pd.DataFrame({})
    sql_manager.insert_df_data(df, 'JOBS', sql_args)

