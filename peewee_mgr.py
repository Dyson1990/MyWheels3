# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:53:26 2023

@author: Weave
"""

import peewee
import importlib.util
import re

from loguru import logger
from pathlib import Path
py_dir = Path(__file__).parent

try:
    # 从同级文件夹里读取db_cfg.py
    spec = importlib.util.spec_from_file_location("db_cfg", py_dir/"db_cfg.py")
    db_cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db_cfg)
except Exception as e0:
    # 从github读取db_cfg.py
    import requests
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
        dialect = kwargs.get('dialect')
        if dialect and dialect in databases:
            database_class = databases[dialect]
            super().__init__(**kwargs)
            self.__class__ = type('CustomDB', (database_class, CustomDB), {})
        else:
            raise Exception("Unsupported database dialect")
            
        self.args = kwargs.copy()

    def self_inspection(self):
        """
        去除会引起连接数据库失败的参数
        """
        while True:
            try:
                # 尝试创建实例并传递关键字参数
                super().__init__(**self.args)
                with self:
                    pass
                break
            except TypeError as e:
                # 提取异常中的无效参数信息
                error_message = str(e)
                re_str = r"Connection\.__init__\(\) got an unexpected keyword argument\s*'(\w+)'"
                m = re.search(re_str, error_message)
                if m:
                    arg0 = m.groups()[0]
                    logger.warning(f"检查到无效参数，已剔除：{arg0}")
                    self.args.pop(arg0)
                else:
                    raise e

# =============================================================================
#         super().__init__(**kwargs)  # 继承父类 Database 的初始化方法
# 
#         global databases
#         print(kwargs['dialect'])
#         self.__class__ = type('CustomDB', (databases[kwargs['dialect']], CustomDB), {})
# =============================================================================


if __name__ == '__main__':
    import pandas as pd
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.1.190"
        , 'username': "Dyson"
        , "password": "1qqaq1"
        , 'dbname': 'test'
    }
    cfg = db_cfg.DBConfig('MySQL', **sql_args)
    cfg.fit_peewee()
    
    db = CustomDB(**cfg)
    db.self_inspection()
    
    # 运行原始 SQL 语句
    query = "SELECT * FROM employees_test LIMIT 10"
    df = pd.read_sql(query, db)
    print(df)

