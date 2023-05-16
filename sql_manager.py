# -*- coding:utf-8 -*-
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: sql_manager.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码，由于处于学习阶段，不打算用pandas中的read_csv、to_csv
--------------------------------
"""
import traceback

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import sqlalchemy.dialects.oracle

import pandas as pd
import numpy as np
from contextlib import closing
import json

# =============================================================================
# eng_str = {
#         'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
#         , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
#         , 'postgresql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}"
#         }
# =============================================================================

# 选择数据库
dbname_str = {
        'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
        , 'mysql':"USE `{}`"
        # , 'postgresql':"\c {}"
        }
np_type2sql_type = {
        np.dtype('int64'): sqlalchemy.sql.sqltypes.Integer
        , np.dtype('float64'): sqlalchemy.sql.sqltypes.FLOAT
        , np.dtype('O'): sqlalchemy.sql.sqltypes.VARCHAR
        }
sql_type2np_type = {
        sqlalchemy.sql.sqltypes.FLOAT: np.dtype('float64')
        , sqlalchemy.sql.sqltypes.Integer: np.dtype('int64')
        , sqlalchemy.sql.sqltypes.DateTime: np.dtype('datetime64[ns]')
        , sqlalchemy.sql.sqltypes.VARCHAR: np.dtype('O')
        }
np_type2oracle_type = {
        np.dtype('int64'): sqlalchemy.dialects.oracle.base.INTEGER
        , np.dtype('float64'): sqlalchemy.dialects.oracle.base.FLOAT
        , np.dtype('O'): sqlalchemy.dialects.oracle.base.VARCHAR2
        }
oracle_type2np_type = {
        sqlalchemy.dialects.oracle.base.FLOAT: np.dtype('float64')
        , sqlalchemy.dialects.oracle.base.INTEGER: np.dtype('int64')
        , sqlalchemy.dialects.oracle.base.DATE: np.dtype('datetime64[ns]')
        , sqlalchemy.dialects.oracle.base.VARCHAR2: np.dtype('O')
        , sqlalchemy.dialects.oracle.base.NUMBER: np.dtype('float64')
        }

def run_sql(sql_args, sql, args=None):
    """
    最常用的连接MySQL的方式
    sql 可以是一条sql语句， 也可以是sql语句组成的列表
    :return: list

    若要转换为dataframe
    data = [list(t) for t in data] # 要求传入列表，不能是元组
    data = pd.DataFrame(data, columns=rp.keys())
    """
    data = []

    sql_args = __standardize_args(sql_args)

    try:
        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = __sql_engine(sql_args)

        with closing(engine.connect()) as conn:
            # 选择数据库
            global dbname_str
            db_dialect = sql_args['db_dialect']
            if db_dialect in dbname_str:
                sql0 = sqlalchemy.text(dbname_str[db_dialect].format(sql_args['database']))
                conn.execute(sql0)

            # 多条SQL语句的话，循环执行
            # rp short for ResultProxy
            if isinstance(sql,list):
                for sql0 in sql:
                    sql0 = sqlalchemy.text(sql0)
                    rp = conn.execute(sql0)
            elif args:
                sql = sqlalchemy.text(sql)
                rp = conn.execute(sql,args)
            else:
                sql = sqlalchemy.text(sql)
                rp = conn.execute(sql)

            if rp is None:
                return None
            data = rp.fetchall()
            # 若要返回dataframe，使用pd.read_sql
            return data
    except:
        print("数据库交互出错：\n%s" % traceback.format_exc())
        return None



def __standardize_args(sql_args):
    # 检查所需参数是否都存在，规范输入的一些参数

    if not isinstance(sql_args, dict):
        raise Exception("sql_args格式错误！！！")
    
    # 规范输入的大小写
    sql_args['db_dialect'] = sql_args['db_dialect'].lower()
    db_dialect = sql_args['db_dialect']
    
    # 兼容新旧版本
    if 'user' in sql_args and 'username' not in sql_args:
        sql_args['username'] = sql_args.pop('user')
    if 'dbname' in sql_args and 'database' not in sql_args:
        sql_args['database'] = sql_args.pop('dbname')

    # 不同的数据库，需要的参数不同
    if db_dialect == 'oracle':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'sid', 'database']

        # Oracle的数据类型比较特殊
        global np_type2sql_type,sql_type2np_type,np_type2oracle_type,oracle_type2np_type
        np_type2sql_type = np_type2oracle_type
        sql_type2np_type = oracle_type2np_type
    elif db_dialect == 'mysql':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'database']
    elif db_dialect == 'postgresql':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'database']
    elif db_dialect == 'access':
        needed_args = ['db_dialect', 'file_path']

    # 缺少参数则报错，
    check_args = [s for s in needed_args if s not in sql_args]
    if check_args:
        raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

    # 规定默认的参数的值 ##################################################
    sql_args['method'] = sql_args.get('method', None) # 没有参数传入，则使用fetchall
    sql_args['data_type'] = sql_args.get('data_type', 'list')
    if db_dialect == 'oracle':
        sql_args['db_driver'] = sql_args.get('db_driver', 'cx_oracle').lower()
        sql_args['port'] = sql_args.get('port', '1521')
        sql_args['query']={"sid": sql_args['sid']}
        
    elif db_dialect == 'mysql':
        sql_args['db_driver'] = sql_args.get('db_driver', 'pymysql').lower()
        sql_args['port'] = sql_args.get('port', '3306')
        sql_args['charset'] = sql_args.get('charset', 'UTF8MB4')
        """
        这种错误很有可能是SQL驱动不完整
        也可能是数据库的编码与申请的编码不符
        1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 484")
        """
        
    elif db_dialect == 'postgresql':
        sql_args['db_driver'] = sql_args.get('db_driver', 'psycopg2').lower()
        sql_args['port'] = sql_args.get('port', '5432')

    elif db_dialect == 'access':
        sql_args['db_driver'] = sql_args.get('db_driver', 'pyodbc').lower()

        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={sql_args.pop('file_path')};"
            r"ExtendedAnsiSQL=1;"
            )
        sql_args['query']={"odbc_connect": connection_string}
        
    #######################################################################
    return sql_args

# =============================================================================
# def __sql_engine(sql_args):
#     # 编辑salalchemy中的数据库参数字符串
#     global eng_str
#     db_dialect = sql_args['db_dialect']
# 
#     # server_side_cursors_arg = db_dialect not in ("access")
#     engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args)
#                                       # , echo=True
#                                       , server_side_cursors=True
#                                       )
#     return engine
# =============================================================================

def __sql_engine(sql_args):
    sql_args = sql_args.copy()
    db_dialect = sql_args.pop('db_dialect')
    db_driver = sql_args.pop('db_driver')
    arg_list = ("username", "password","host","port","database","query") #URL.create()不接受其他参数 
    sql_args = {k0: v0 for k0, v0 in sql_args.items() if k0 in arg_list}
    
    conn_url = sqlalchemy.engine.URL.create(
        f"{db_dialect}+{db_driver}"
        , **sql_args
    )
    
    server_side_cursors_arg = db_dialect not in ("access")
    return sqlalchemy.create_engine(
        conn_url
        , server_side_cursors=server_side_cursors_arg
        )

def check_json(str0):
    try:
        json.loads(str0)
    except:
        return False
    else:
        return True

if __name__ == '__main__':
    # 测试本地MySQL参数
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.50.188"
        , 'username': "Dyson"
        , "password": "122321"
        , 'dbname': 'test'

    }
    # print(run_sql(sql_args, 'SELECT * FROM ``'))
    # pd.DataFrame([]).to_sql()