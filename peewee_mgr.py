# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:53:26 2023

@author: Weave
"""

import peewee

from loguru import logger
from pathlib import Path

try:
    from . import db_cfg
except Exception as e0:
    import requests
    import importlib.util
    import types
    import sys
    owner = "Dyson1990"
    repo = "MyWheels3"
    branch = "master"
    module_p = "db_cfg.py"
    # 从GitHub API获取源代码并打包成字节码
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{module_p}'
    params = {'ref': branch} if branch else None
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    proxies = {'http': 'socks5://127.0.0.1:10808', 'https': 'socks5://127.0.0.1:10808'}
    response = requests.get(url,params=params,headers=headers,proxies=proxies)
    source_code_raw = response.text
    spec = importlib.util.spec_from_loader("db_cfg", loader=None, origin="<string>")
    db_cfg = types.ModuleType(spec.name)
    exec(source_code_raw, db_cfg.__dict__)
    sys.modules[spec.name] = db_cfg
    globals()[spec.name] = db_cfg
    logger.info(f"downloaded db_cfg.py from web, error: {e0}")
    
databases = {
    'sqlite': peewee.SqliteDatabase,
    'mysql': peewee.MySQLDatabase,
    'postgresql': peewee.PostgresqlDatabase,
}

class CustomDB(peewee.Database):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 继承父类 Database 的初始化方法
        
        global databases
        self.__class__ = type('CustomDB', (databases[kwargs['dialect']], CustomDB), {})


if __name__ == '__main__':
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.1.125"
        , 'username': "Dyson"
        , "password": "1qqaq1"
        , 'dbname': 'test'
        , 'table_name': 'vote_record'
    }
    cfg = db_cfg.DBConfig('MySQL', **sql_args)
    cfg.fit_peewee()
    
    db = CustomDB(**cfg)
    print(db)

# # 定义 MySQL 数据库连接
# # db = MySQLDatabase('mydatabase', user='myuser', password='mypassword',
# #                    host='myhost', port=3306)

# # 执行原生 SQL 查询
# cursor = db.execute_sql("SELECT * FROM mytable")

# # 一行一行读取数据并处理
# while True:
#     batch = cursor.fetchmany(1000)
#     if not batch:
#         break
#     for row in batch:
#         # 处理每一行数据
#         print(row)

# # 关闭游标
# cursor.close()