# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: data_reader.py
    @time: 2017/6/21 9:07
--------------------------------
"""
import sys
import os
import json
import pandas as pd

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"
import mysql_connecter

class data_reader(object):
    def __init__(self):
        self.mysql_con = mysql_connecter.mysql_connecter()

    def get_data(self, table_name):
        sql = "SELECT * FROM `%s`" %table_name
        data = self.mysql_con.connect(sql, dbname='spider', ip='localhost', user='spider', password='startspider')

        return data

    def get_title(self, table_name):
        sql = "DESC `%s`" %table_name
        data = self.mysql_con.connect(sql, dbname='spider', ip='localhost', user='spider', password='startspider')

        title = [t[0] for t in data]
        return title

    def json_reader(self, table_name, json_col):
        data = self.get_data(table_name)
        title = self.get_title(table_name)

        df = pd.DataFrame(data, columns=title)

        d = {}

        for s in json_col:
            df0 = df.loc[:,['parcel_no', s]]
            df.pop(s)

            for i in xrange(df0.shape[0]):
                d[df0.iloc[i,0]] = json.loads(df0.iloc[i,1])

            df00 = pd.DataFrame(d).stack().swaplevel().unstack()

            df = df.merge(df00, on='parcel_no', how='left')

        df.to_csv('C:\Users\lenovo\Desktop\data_reader.csv', encoding='utf8')

if __name__ == '__main__':
    data_reader = data_reader()
    data_reader.json_reader('monitor', ['detail',])