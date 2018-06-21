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

import pymysql as mysql
import sys

import pandas as pd
import numpy as np
from itertools import chain
from contextlib import closing


# log_obj = set_log.Logger('mysql_connecter.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_connecter.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class mysql_connecter(object):

    def __init__(self):
        pass
    
    def connect(self,sql, mysql_args, args=None):
        """
        最常用的连接MySQL的方式
        sql 可以是一条sql语句， 也可以是sql语句组成的列表
        :return: list
        """
        data = []

        mysql_args = self.standardize_args(mysql_args)

        try:
            with closing(mysql.connect(mysql_args['host'],
                                       mysql_args['user'],
                                       mysql_args['password'],
                                       mysql_args['dbname'],
                                       charset = mysql_args['charset'])) as con:
                cur = con.cursor()
            
                # 多条SQL语句的话，循环执行
                if isinstance(sql,list):
                    for sql0 in sql:
                        cur.execute(sql0)
                else:
                    cur.execute(sql,args)

                data = cur.fetchall()
                con.commit()

        except:
            print("数据库交互出错：%s" %traceback.format_exc())

#        finally:
#            if con:
#                #无论如何，连接记得关闭
#                con.close()

        return [list(t) for t in data]

    def insert_df_data(self, df, table_name, mysql_args, method="INSERT", fill_na=None):
        """
        如果在INSERT语句末尾指定了ON DUPLICATE KEY UPDATE，并且插入行后会导致在一个UNIQUE索引或PRIMARY KEY中出现重复值，
        则在出现重复值的行执行UPDATE；如果不会导致唯一值列重复的问题，则插入新行。

        此处需在df的列中加入目标表格table_name中的key，不然key默认为空白值

        :param df:
        :param table_name:
        :param method:

        :return:
         
        df:
               A      B      C
          1   23.0  213.0    NaN
          2  434.0    NaN  213.0

        sql: INSERT INTO ``(`A`,`B`,`C`) VALUES(%s,%s,%s),(%s,%s,%s)

        args: [23.0, 213.0, nan, 434.0, nan, 213.0]

        """
        # 是否需要补全缺失值
        if fillna0 != None:
            df = df.fillna(fill_na)

        # 以df的列名作为INSERT语句中的表格字段名
        title_str = ','.join(['`%s`' %s for s in df.columns])

        # 讲df中的所有除去标题以外的数据组织成一段字符串
        data_str = ','.join(["(%s)" % (','.join(["%s", ] * df.shape[1])) for i in range(df.shape[0])])

        sql = "INSERT INTO `%s`(%s) VALUES%s" %(table_name, title_str, data_str)

        #print df
        data_l = list(chain(*np.array(df).tolist()))
        print(data_l)

        if method == 'UPDATE':
            sql = sql + 'ON DUPLICATE KEY UPDATE ' + ','.join(['`%s`=VALUES(`%s`)' %((s,) * 2) for s in df.columns])
            method = 'INSERT.... ON DUPLICATE KEY UPDATE'

        # print(sql)
        self.connect(sql, mysql_args, args=data_l)
        print("%s successfully !" %method)

    def update_df_data(self, df, table_name, index_name, mysql_args, fill_na=None):
        """
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

        self.connect(sql, mysql_args)
        print("UPDATE successfully !")

    def standardize_args(self, mysql_args):

        if not isinstance(mysql_args, dict):
            raise Exception("mysql_args格式错误！！！")

        needed_args = ['host', 'user', 'password', 'dbname']
        check_args = [s for s in needed_args if s not in mysql_args]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

        if 'charset' not in mysql_args:
            mysql_args['charset'] = 'utf8'

        return mysql_args




if __name__ == '__main__':
    mysql_connecter = mysql_connecter()
    mysql_args = {
        "host": "116.62.230.38",
        "user": "spider444",
        "password": "startspider",
        "dbname": "spider",
        "charset": "utf8"
    }
    # sql = "SELECT * FROM monitor limit 10"
    # print(mysql_connecter.connect(sql,
    #                               host = mysql_args["host"],
    #                               user = mysql_args["user"],
    #                               password = mysql_args["password"],
    #                               dbname = mysql_args["dbname"],
    #                               charset=mysql_args["charset"]
    #                               ))

    df = pd.DataFrame({1:{"A":23,"B":213}, 2:{"A":434,"C":213}}).T
    print(df)
    mysql_connecter.update_df_data(df,'', 'A',mysql_args , fill_na=0)
