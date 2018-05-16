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

import pymysql as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import set_log
import pandas as pd
import numpy as np
from itertools import chain


#import sqlalchemy
#import sqlalchemy.ext.declarative
#import sqlalchemy.orm

log_obj = set_log.Logger('mysql_connecter.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('mysql_connecter.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class mysql_connecter(object):

    def __init__(self):
        pass
    
    def connect(self,sql,args=None,host='localhost',user='spider',password = 'jlspider', dbname = 'spider', charset='utf8'):
        """
        :return: list
        """
        con = ''
        try:
            con = mysql.connect(host,user,password,dbname,charset = charset)
            cur = con.cursor()
            
            # 多条SQL语句的话，循环执行
            if isinstance(sql,list):
                for sql0 in sql:
                    cur.execute(sql0)
            else:
                cur.execute(sql,args)
                
            data = cur.fetchall()
            con.commit()
            # data.decode('uft8').encode('gbk')
        finally:
            if con:
                #无论如何，连接记得关闭
                con.close()
                
        return [list(t) for t in data]

    def insert_df_data(self, df, table_name, method='INSERT',host='localhost',user='spider',password = 'jlspider', dbname = 'spider', charset='utf8'):
        """
        如果在INSERT语句末尾指定了ON DUPLICATE KEY UPDATE，并且插入行后会导致在一个UNIQUE索引或PRIMARY KEY中出现重复值，
        则在出现重复值的行执行UPDATE；如果不会导致唯一值列重复的问题，则插入新行。

        此处需在df的列中加入目标表格table_name中的key，不然key默认为空白值

        :param df:
        :param table_name:
        :param method:
        :param host:
        :param user:
        :param password:
        :param dbname:
        :param charset:
        :return:
        """

        title_str = ','.join(['`%s`' %s for s in df.columns])
        data_str = ','.join(["(%s)" % (','.join(["%s", ] * df.shape[1])) for i in range(df.shape[0])])

        sql = "INSERT INTO `%s`(%s) VALUES%s" %(table_name, title_str, data_str)

        #print df
        data_l = list(chain(*np.array(df).tolist()))

        if method == 'UPDATE':
            sql = sql + 'ON DUPLICATE KEY UPDATE ' + ','.join(['`%s`=VALUES(`%s`)' %((s,) * 2) for s in df.columns])
            method = 'INSERT.... ON DUPLICATE KEY UPDATE'

        # print sql
        self.connect(sql, args=data_l, host=host, user=user, password=password, dbname=dbname, charset=charset)
        print "%s successfully !" %method

    def update_df_data(self, df, table_name, index_name,host='localhost',user='spider',password = 'jlspider', dbname = 'spider', charset='utf8'):
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
        #print sql
        self.connect(sql, host=host, user=user, password=password, dbname=dbname, charset=charset)
        print "UPDATE successfully !"




if __name__ == '__main__':
    mysql_connecter = mysql_connecter()
    #print mysql_connecter.connect('select * from actor', dbname = 'sakila')
    # df = pd.read_csv('C:\\Users\\Administrator\\Desktop\\20171122.csv', dtype=np.str)
    # df.index = df['fund_code']
    # print df.head(6)
    # mysql_connecter.update_df_data(df, 'fund_info', 'fund_code')

    import re
    df = pd.read_excel(u'C:\\Users\\Administrator\\Desktop\\公募基金核心库前十持股分类.xlsx', dtype=np.str)
    # print df
    drop_l = []
    for s in df.index:
        # print s, type(s)
        if not re.search(r'^\d+$', s):
            drop_l.append(s)
    df = df.drop(drop_l, axis=0).drop([u'2017年三季度主题',u'基金名称'], axis=1)

    df = df.rename(columns={u'2017年四季度主题':'3rd_class'})
    df['fund_code'] = df.index
    df['3rd_class'] = df['3rd_class'].apply(lambda s:None if s == 'nan' else s)
    # df = df.reset_index()
    # df = df.fillna(None)
    print df
    mysql_connecter.insert_df_data(df, 'fund_info', method='UPDATE')


"""
mysql -P 3306 -h rm-bp1ks9kestihy4wy1o.mysql.rds.aliyuncs.com -u test1 -p
"""