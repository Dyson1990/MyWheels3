# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: mysql_connecter.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码
--------------------------------
"""
import traceback

import sqlalchemy

import pandas as pd
import numpy as np
from itertools import chain
from contextlib import closing


# log_obj = set_log.Logger('mysql_connecter.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_connecter.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


eng_str = {
        'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
        , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/?charset={charset}"
        }
dbname_str = {
        'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
        , 'mysql':"USE `{}`"
        }
np_type2sql_type = {
        np.str: sqlalchemy.CHAR(),
        np.int64: sqlalchemy.Integer(),
        np.float64: sqlalchemy.FLOAT(),
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
        
        global eng_str
        sql_args = self.standardize_args(sql_args)

        try:
            # 使用哪种数据库，填入Oralce，MySQL等等
            db_dialect = sql_args['db_dialect'] 
            engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args))
            
            with closing(engine.connect()) as conn:
                # 选择数据库
                global dbname_str
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
        # 暂定所有字段都是字符串，默认为空白字符
        # Column('id',Integer(),primary_key=True, autoincrement=True),
        
        table_name = df_args['table_name']
        df = df_args['data']
        primary_key = df_args['primary_key']
        raise isinstance(df, pd.core.frame.DataFrame)
        
        sql_table = sqlalchemy.Table(table_name,sqlalchemy.BaseModel.metadata)
        
        for col in df.columns:
            sql_table.append_column(
                sqlalchemy.Column(
                        col,
                        np_type2sql_type(df[col].dtype),
                        primary_key=(col == primary_key), 
                        ),
                )
        
        
        

    def create_table(self, col_names, table_name, sql_args):
        # 暂定所有字段都是字符串，默认为空白字符

        col_str = ',\n'.join(["`%s` VARCHAR(255) default ''" %s for s in col_names])

        sql = """
        CREATE TABLE IF NOT EXISTS `%s`(
           %s
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """ %(table_name, col_str)

        self.connect(sql, sql_args)
        print("create successfully !")

    def insert_df_data(self, df, table_name, sql_args, method="INSERT", fill_na=None):
        """
        如果在INSERT语句末尾指定了ON DUPLICATE KEY UPDATE，并且插入行后会导致在一个UNIQUE索引或PRIMARY KEY中出现重复值，
        则在出现重复值的行执行UPDATE；如果不会导致唯一值列重复的问题，则插入新行。

        此处需在df的列中加入目标表格table_name中的key，不然key默认为空白值

        :param df:
        :param table_name:
        :param method:

        :return:

        举例说明
         
        df:
               A      B      C
          1   23.0  213.0    NaN
          2  434.0    NaN  213.0

        sql: INSERT INTO ``(`A`,`B`,`C`) VALUES(%s,%s,%s),(%s,%s,%s)

        args: [23.0, 213.0, nan, 434.0, nan, 213.0]

        """
        # 是否需要补全缺失值
        if fill_na != None:
            df = df.fillna(fill_na)

        # 以df的列名作为INSERT语句中的表格字段名
        title_str = ','.join(['`%s`' %s for s in df.columns])

        # 讲df中的所有除去标题以外的数据组织成一段字符串
        data_str = ','.join(["(%s)" % (','.join(["%s", ] * df.shape[1])) for i in range(df.shape[0])])

        sql = "INSERT INTO `%s`(%s) VALUES%s" %(table_name, title_str, data_str)

        #print df
        data_l = list(chain(*np.array(df).tolist()))
        # print(data_l)

        if method == 'UPDATE':
            sql = sql + 'ON DUPLICATE KEY UPDATE ' + ','.join(['`%s`=VALUES(`%s`)' %((s,) * 2) for s in df.columns])
            method = 'INSERT.... ON DUPLICATE KEY UPDATE'

        # print(sql)
        self.connect(sql, sql_args, args=data_l)
        print("%s successfully !" %method)

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
    
    




if __name__ == '__main__':
    sql_connecter = sql_connecter()
    
# =============================================================================
#     # 本地测试Oracle参数
#     sql_args = {
#         'db_dialect': 'oracle'
#         , 'db_driver': 'cx_Oracle'
#         , "host": "localhost"
#         , "user": "Dyson"
#         , "password": "122321"
#         , 'sid': 'XE'
#         , 'dbname': 'HR'
#         , 'data_type': 'DataFrame'
#     }
#    print(sql_connecter.connect('SELECT JOB_ID, MIN_SALARY, COMMIT FROM JOBS', sql_args))
# =============================================================================
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
#     print(sql_connecter.connect('SELECT * FROM `actor` LIMIT 20', sql_args))
# =============================================================================
    print(dir(sqlalchemy.Table))

