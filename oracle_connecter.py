# -*- coding:utf-8 -*-  
#/usr/bin/python3
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: oracle_connecter.py
    @time: 2018/6/26 15:09
--------------------------------
"""
import sys
import os
import numpy as np
import pandas as pd
from contextlib import closing
import cx_Oracle
import traceback

#import set_log  

#log_obj = set_log.Logger('oracle_connecter.log', set_log.logging.WARNING,
#                         set_log.logging.DEBUG)
#log_obj.cleanup('oracle_connecter.log', if_cleanup = True)  # 是否需要在每次运行程序前清空Log文件

# print('cx_Oracle.version: ' + cx_Oracle.version)

sql_func = {
        'LOB':(lambda s: s.read() if isinstance(s, cx_Oracle.LOB) else s),
        }

class oracle_connecter(object):

    def __init__(self):
        pass

    def connect(self, sql, oracle_args, args=None):
        """
        最常用的连接MySQL的方式
        sql 可以是一条sql语句， 也可以是sql语句组成的列表

        ps：
        1.暂时只支持SID登录，服务名登录测试失败
        2.若存在CLOB格式的数据，SQL中需要用to_char

        :return: list
        """
        data = []

        oracle_args = self.standardize_args(oracle_args)

        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.%s' %oracle_args['charset']

        try:
            dsn = cx_Oracle.makedsn(oracle_args['host'], oracle_args['port'], sid = oracle_args['sid']) # , service_name=oracle_args['sevicename']
            con0 = cx_Oracle.connect(user = oracle_args['user'], password = oracle_args['password'], dsn=dsn)

            with closing(con0) as conn:
                cur = conn.cursor()

                # 选择需要操作的数据库
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = \"%s\"" %oracle_args['dbname'])

                # 多条SQL语句的话，循环执行
                if isinstance(sql, list):
                    for sql0 in sql:
                        cur.execute(sql0)
                else:
                    # 待确定，execute函数应该是可以传入args=None的
                    if args:
                        cur.execute(sql, args)
                    else:
                        cur.execute(sql)
                        
                data_info = cur.description # 获取到的数据的表结构
                
                # 实现对结果每个数据的处理方法
                if isinstance(oracle_args['method'], type(None)):
                    data = cur.fetchall()
                    
                elif isinstance(oracle_args['method'], str):
                    # 传入的参数是字符，则在sql_func中查询函数
                    method0 = oracle_args['method']
                    data = [[sql_func[method0](cell) for cell in row] for row in cur]
                    
                elif isinstance(oracle_args['method'], type(lambda :0)):
                    # 传入的参数是公式，则直接使用
                    method0 = oracle_args['method']
                    data = [[method0(cell) for cell in row] for row in cur]
                    
                elif isinstance(oracle_args['method'], list):
                    # 传入列表， 就一个个重复上面的两个判断
                    for method0 in oracle_args['method']:
                        if isinstance(oracle_args['method'], str):
                            method0 = oracle_args['method']
                            data = [[sql_func[method0](cell) for cell in row] for row in cur]
                        elif isinstance(oracle_args['method'], type(lambda :0)):
                            method0 = oracle_args['method']
                            data = [[method0(cell) for cell in row] for row in cur]
                        else:
                            raise(Exception('输入的参数method有误！！！'))
                else:
                    raise(Exception('输入的参数method有误！！！'))

                # 修改返回数据的类型
                if oracle_args['data_type'] == 'list':
                    data = [list(t) for t in data]
                elif oracle_args['data_type'] in ('DataFrame', 'dataframe'):
                    data = [list(t) for t in data] # 要求传入列表，不能是
                    data = pd.DataFrame(data, columns=[r[0] for r in data_info])
                else:
                    raise(Exception('输入的参数data_type有误！！！'))
                
                conn.commit() #插入数据的时候用到
                cur.close()
                
                return data
        except:
            print("数据库交互出错：%s" % traceback.format_exc())
            return None

    #        finally:
    #            if con:
    #                #无论如何，连接记得关闭
    #                con.close()

# =============================================================================
#     def df_output(self, sql, oracle_args):
#         # 用pandas来从MySQL读取数据
# 
#         oracle_args = self.standardize_args(oracle_args)
#         os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.%s' %oracle_args['charset']
# 
#         dsn = cx_Oracle.makedsn(oracle_args['host'], oracle_args['port'], sid = oracle_args['sid']) # , service_name=oracle_args['sevicename']
#         conn0 = cx_Oracle.connect(user = oracle_args['user'], password = oracle_args['password'], dsn=dsn)
# 
#         with closing(conn0) as conn:
#             cur = conn.cursor()
#             cur.execute("ALTER SESSION SET CURRENT_SCHEMA = \"%s\"" % oracle_args['dbname'])
# 
#             df = pd.read_sql(sql, conn)
# 
#         return df
# =============================================================================

    def standardize_args(self, oracle_args):
        # 检查所需参数是否都存在

        if not isinstance(oracle_args, dict):
            raise Exception("oracle_args格式错误！！！")

        needed_args = ['host', 'user', 'password', 'sid', 'dbname']
        check_args = [s for s in needed_args if s not in oracle_args]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

        # 设置默认参数

        if 'port' not in oracle_args:
            oracle_args['port'] = '1521'
        if 'charset' not in oracle_args:
            oracle_args['charset'] = 'UTF8'
        if 'method' not in oracle_args:
            # 没有参数传入，则使用fetchall
            oracle_args['method'] = None
        if 'data_type' not in oracle_args:
            oracle_args['data_type'] = 'list'

        return oracle_args


if __name__ == '__main__':
    oracle_connecter = oracle_connecter()

    # 本地测试案例cx_Oracle-6.4.1-cp36-cp36m-win_amd64.whl
    oracle_args = {'user': 'system'
        , 'password': '122321'
        , 'host': 'localhost'
        , 'sid': 'XE'
        , 'dbname': 'HR'
        , 'method': 'LOB'
        , 'data_type': 'DataFrame'}
    print(oracle_connecter.connect('SELECT JOB_ID, MIN_SALARY, COMMIT FROM JOBS', oracle_args))




# =============================================================================
#     # 服务器测试
#     oracle_args = {'user': 'VW_NOV06'
#         , 'password': 'C372M5c590'
#         , 'host': '172.17.32.2'
#         , 'sid': 'orcl'
#         , 'dbname': 'CDB_NOV'}
#     print(oracle_connecter.connect('SELECT * FROM F_QY_JBXX WHERE ROWNUM <= 10', oracle_args))
# =============================================================================
