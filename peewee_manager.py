# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:53:26 2023

@author: Weave
"""

import peewee

# 定义 MySQL 数据库连接
db = MySQLDatabase('mydatabase', user='myuser', password='mypassword',
                   host='myhost', port=3306)

# 执行原生 SQL 查询
cursor = db.execute_sql("SELECT * FROM mytable")

# 一行一行读取数据并处理
while True:
    batch = cursor.fetchmany(1000)
    if not batch:
        break
    for row in batch:
        # 处理每一行数据
        print(row)

# 关闭游标
cursor.close()