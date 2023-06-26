# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:14:25 2023

@author: Weave
"""

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import urllib.parse as urlparse

from pathlib import Path
from contextlib import closing
from loguru import logger

# 设计的还是有问题
defaults = {
    'oracle': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'sid': {'required': True},
        'database': {'required': True},
        'method': {'default': None},
        'db_driver': {'default': 'cx_oracle', 'lower': True},
        'port': {'default': 1521},
    },
    'mysql': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'database': {'required': True},
        'method': {'default': None},
        'db_driver': {'default': 'pymysql', 'lower': True},
        'port': {'default': 3306},
        'charset': {'default': 'UTF8MB4'},
    },
    'postgresql': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'database': {'required': True},
        'method': {'default': None},
        'db_driver': {'default': 'psycopg2', 'lower': True},
        'port': {'default': 5432},
    },
    'access': {
        'file_path': {'required': True},
        'username': {'required': True},
        'method': {'default': None},
        'db_driver': {'default': 'pyodbc', 'lower': True},
    }
}

key_mapping = {
    'user': 'username'
    , 'dbname': 'database'
    , 'db_dialect': 'dialect'
    , 'db_driver': 'driver'
    }

# =============================================================================
# # 选择数据库
# dbname_str = {
#         'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
#         , 'mysql':"USE `{}`"
#         # , 'postgresql':"\c {}"
#         }
# =============================================================================

class DBConfig(dict):
    def __init__(self, dialect, **kwargs):
        # 兼容新旧版本
        global key_mapping
        kwargs = {key_mapping.get(k0, k0): v0 for k0, v0 in kwargs.items()}
        super().__init__(**kwargs)
        
        # 确定哪个数据库
        self.dialect = dialect.lower()
        global defaults
        defaults0 = defaults[self.dialect].copy()

        # 缺少参数则报错
        needed_args = [k0 for k0, d0 in defaults0.items() if d0.get('required')==True]
        check_args = [s for s in needed_args if s not in self]
        if check_args:
            raise Exception("缺少数据库参数：%s" % '，'.join(check_args))
            
        # 规定默认的参数的值 ##################################################
        
        for k0 in defaults0.keys():
            if k0 not in self \
            and k0 in defaults0 \
            and 'default' in defaults0[k0]:
                self[k0] = defaults0[k0]['default']
        
        # 额外的参数赋值
        if dialect == 'oracle':
            self['query']={"sid": self['sid']}
        elif dialect == 'access':
            self['db_driver'] = self.get('db_driver', 'pyodbc').lower()
    
            connection_string = (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                f"DBQ={self.pop('file_path')};"
                r"ExtendedAnsiSQL=1;"
                )
            self['query']={"odbc_connect": connection_string}
        
        # 将键值存到对象的属性里，并统一值
        for k0, v0 in self.items():
            if not hasattr(self, k0):
                setattr(self, k0, v0)
            elif getattr(self, k0) != v0:
                self[k0] = getattr(self, k0)
            else:
                logger.warning(f"DBConfig中出现未知属性=>{k0}:{v0}")
    
    def to_json(self):
        import json
        return json.dumps(self, indent=2)

if __name__ == "__main__":
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.1.125"
        , 'username': "Dyson"
        , "password": "1qqaq1"
        , 'dbname': 'test'
        , 'table_name': 'vote_record'
    }
    
    cfg = DBConfig("MySQL", **sql_args)
    print(cfg)
    print(cfg.to_json())
