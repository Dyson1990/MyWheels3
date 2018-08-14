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

import pymysql
import sys

import pandas as pd
import numpy as np
from itertools import chain
from contextlib import closing


# log_obj = set_log.Logger('mysql_connecter.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_connecter.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件

sql_func = {
        }

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
            with closing(pymysql.connect(mysql_args['host'],
                                       mysql_args['user'],
                                       mysql_args['password'],
                                       mysql_args['dbname'],
                                       charset = mysql_args['charset'])) as conn:
                cur = conn.cursor()
            
                # 多条SQL语句的话，循环执行
                if isinstance(sql,list):
                    for sql0 in sql:
                        cur.execute(sql0)
                else:
                    cur.execute(sql,args)

                data_info = cur.description # 获取到的数据的表结构
                
                # 实现对结果每个数据的处理方法
                if isinstance(mysql_args['method'], type(None)):
                    data = cur.fetchall()
                    
                elif isinstance(mysql_args['method'], str):
                    # 传入的参数是字符，则在sql_func中查询函数
                    method0 = mysql_args['method']
                    data = [[sql_func[method0](cell) for cell in row] for row in cur]
                    
                elif isinstance(mysql_args['method'], type(lambda :0)):
                    # 传入的参数是公式，则直接使用
                    method0 = mysql_args['method']
                    data = [[method0(cell) for cell in row] for row in cur]
                    
                elif isinstance(mysql_args['method'], list):
                    # 传入列表， 就一个个重复上面的两个判断
                    for method0 in mysql_args['method']:
                        if isinstance(mysql_args['method'], str):
                            method0 = mysql_args['method']
                            data = [[sql_func[method0](cell) for cell in row] for row in cur]
                        elif isinstance(mysql_args['method'], type(lambda :0)):
                            method0 = mysql_args['method']
                            data = [[method0(cell) for cell in row] for row in cur]
                        else:
                            raise(Exception('输入的参数method有误！！！'))
                else:
                    raise(Exception('输入的参数method有误！！！'))

                # 修改返回数据的类型
                if mysql_args['data_type'] == 'list':
                    data = [list(t) for t in data]
                elif mysql_args['data_type'] in ('DataFrame', 'dataframe'):
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
#     def df_output(self, sql, mysql_args):
#         # 用pandas来从MySQL读取数据
# 
#         mysql_args = self.standardize_args(mysql_args)
# 
#         with closing(pymysql.connect(mysql_args['host'],
#                                      mysql_args['user'],
#                                      mysql_args['password'],
#                                      mysql_args['dbname'],
#                                      charset=mysql_args['charset'])) as conn:
#             df = pd.read_sql(sql, conn)
#         return df
# =============================================================================

    def create_table(self, col_names, table_name, mysql_args):
        # 暂定所有字段都是字符串，默认为空白字符

        col_str = ',\n'.join(["`%s` VARCHAR(255) default ''" %s for s in col_names])

        sql = """
        CREATE TABLE IF NOT EXISTS `%s`(
           %s
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """ %(table_name, col_str)

        self.connect(sql, mysql_args)
        print("create successfully !")

    def insert_df_data(self, df, table_name, mysql_args, method="INSERT", fill_na=None):
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
        self.connect(sql, mysql_args, args=data_l)
        print("%s successfully !" %method)

    def update_df_data(self, df, table_name, index_name, mysql_args, fill_na=None):
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

        self.connect(sql, mysql_args)
        print("UPDATE successfully !")

    def standardize_args(self, mysql_args):
        # 检查所需参数是否都存在

        if not isinstance(mysql_args, dict):
            raise Exception("mysql_args格式错误！！！")

        needed_args = ['host', 'user', 'password', 'dbname']
        check_args = [s for s in needed_args if s not in mysql_args]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

        if 'charset' not in mysql_args:
            mysql_args['charset'] = 'utf8'
        if 'method' not in mysql_args:
            # 没有参数传入，则使用fetchall
            mysql_args['method'] = None
        if 'data_type' not in mysql_args:
            mysql_args['data_type'] = 'list'
            
        return mysql_args




if __name__ == '__main__':
    mysql_connecter = mysql_connecter()
    mysql_args = {
        "host": "localhost",
        "user": "Dyson",
        "password": "122321",
        "dbname": "sakila",
        "charset": "utf8",
        "data_type":"DataFrame"
    }
    print(mysql_connecter.connect('SELECT * FROM `actor` LIMIT 20', mysql_args))

