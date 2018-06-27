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

class oracle_connecter(object):

    def __init__(self):
        pass

    def connect(self, sql, oracle_args, args=None):
        """
        最常用的连接MySQL的方式
        sql 可以是一条sql语句， 也可以是sql语句组成的列表
        :return: list
        """
        data = []

        oracle_args = self.standardize_args(oracle_args)

        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

        try:

            # con0 = cx_Oracle.connect("%s/%s@%s:%s/%s" %(oracle_args['user']
            #                                         , oracle_args['password']
            #                                         , oracle_args['host']
            #                                         , oracle_args['port']
            #                                         , oracle_args['sevicename']))

            dsn = cx_Oracle.makedsn(oracle_args['host'], oracle_args['port'], sid = oracle_args['sid']) # , service_name=oracle_args['sevicename']

            con0 = cx_Oracle.connect(user = oracle_args['user'], password = oracle_args['password'], dsn=dsn)

            with closing(con0) as con:
                cur = con.cursor()

                # 选择需要操作的数据库
                cur.execute("ALTER SESSION SET CURRENT_SCHEMA = \"%s\"" %oracle_args['dbname'])

                # 多条SQL语句的话，循环执行
                if isinstance(sql, list):
                    for sql0 in sql:
                        cur.execute(sql0)
                else:
                    if args:
                        cur.execute(sql, args)
                    else:
                        print(sql)
                        cur.execute(sql)

                data = cur.fetchall()
                con.commit()

        except:
            print("数据库交互出错：%s" % traceback.format_exc())

    #        finally:
    #            if con:
    #                #无论如何，连接记得关闭
    #                con.close()

        return [list(t) for t in data]

    def standardize_args(self, oracle_args):
        # 检查所需参数是否都存在

        if not isinstance(oracle_args, dict):
            raise Exception("oracle_args格式错误！！！")

        needed_args = ['host', 'user', 'password', 'sid', 'dbname']
        check_args = [s for s in needed_args if s not in oracle_args]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

        if 'port' not in oracle_args:
            oracle_args['port'] = '1521'

        return oracle_args


if __name__ == '__main__':
    oracle_connecter = oracle_connecter()

    # 本地测试案例
    oracle_args = {'user': 'system'
        , 'password': '122321'
        , 'host': 'localhost'
        , 'sid': 'XE'
        , 'dbname': 'HR'}
    print(oracle_connecter.connect('SELECT * FROM JOBS', oracle_args))

    # 服务器测试
    # oracle_args = {'user': 'VW_NOV06'
    #     , 'password': 'C372M5c590'
    #     , 'host': '172.17.32.2'
    #     , 'sid': 'orcl'
    #     , 'dbname': 'CDB_NOV'}
    # print(oracle_connecter.connect('SELECT * FROM F_QY_JBXX WHERE ROWNUM <= 10', oracle_args))