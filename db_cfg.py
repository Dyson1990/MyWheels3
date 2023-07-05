# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:14:25 2023

@author: Weave
"""

from pathlib import Path
from loguru import logger

# 设计的还是有问题
defaults = {
    'oracle': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'sid': {'required': True},
        'database': {'required': True},
        'db_driver': {'default': 'cx_oracle', 'lower': True},
        'port': {'default': 1521},
    },
    'mysql': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'database': {'required': True},
        'db_driver': {'default': 'pymysql', 'lower': True},
        'port': {'default': 3306},
        'charset': {'default': 'UTF8MB4'},
    },
    'postgresql': {
        'host': {'required': True},
        'username': {'required': True},
        'password': {'required': True},
        'database': {'required': True},
        'db_driver': {'default': 'psycopg2', 'lower': True},
        'port': {'default': 5432},
    },
    'access': {
        'file_path': {'required': True},
        'username': {'required': True},
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
    """
    参数默认是根据sqlalchemy.engine.URL.create()来的，以下是不同数据库需要的参数。
    
    # SQLite
    drivername='sqlite': SQLite 数据库类型
    database: SQLite 数据库文件的绝对路径
    
    # PostgreSQL
    drivername='postgresql': PostgreSQL 数据库类型
    username: PostgreSQL 用户名
    password: PostgreSQL 密码
    host: PostgreSQL 服务器主机名
    port: PostgreSQL 服务器端口号（默认为 5432）
    database: 要连接的数据库名称
    
    # MySQL
    drivername='mysql': MySQL 数据库类型
    username: MySQL 用户名
    password: MySQL 密码
    host: MySQL 服务器主机名
    port: MySQL 服务器端口号（默认为 3306）
    database: 要连接的数据库名称
    
    # Oracle
    drivername='oracle+cx_oracle': Oracle 数据库类型
    username: Oracle 用户名
    password: Oracle 密码
    host: Oracle 服务器主机名
    port: Oracle 服务器端口号（默认为 1521）
    service_name: Oracle 服务名称
    
    # Microsoft SQL Server
    drivername='mssql+pyodbc'（使用 PyODBC 驱动）或 'mssql+pymssql'（使用 PyMSSQL 驱动）
    username: SQL Server 用户名
    password: SQL Server 密码
    host: SQL Server 服务器主机名
    port: SQL Server 服务器端口号（默认为 1433）
    database: 要连接的数据库名称
    
    # Firebird
    drivername='firebird': Firebird 数据库类型
    username: Firebird 用户名
    password: Firebird 密码
    host: Firebird 服务器主机名
    port: Firebird 服务器端口号（默认为 3050）
    database: 要连接的数据库路径
    
    # Sybase
    drivername='sybase': Sybase 数据库类型
    username: Sybase 用户名
    password: Sybase 密码
    host: Sybase 服务器主机名
    port: Sybase 服务器端口号（默认为 5000）
    database: 要连接的数据库名称
    
    # IBM DB2
    drivername='ibm_db_sa': IBM DB2 数据库类型
    username: DB2 用户名
    password: DB2 密码
    host: DB2 服务器主机名
    port: DB2 服务器端口号（默认为 50000）
    database: 要连接的数据库名称
    
    # Informix
    drivername='informix': Informix 数据库类型
    username: Informix 用户名
    password: Informix 密码
    host: Informix 服务器主机名
    port: Informix 服务器端口号（默认为 9088）
    database: 要连接的数据库名称
    
    # Microsoft Access
    drivername='access+pyodbc': Microsoft Access 数据库类型
    database: Microsoft Access 数据库文件的绝对路径
    """
    def __init__(self, dialect, is_compat=True, **kwargs):
        if is_compat:
            # 兼容新旧版本
            global key_mapping
            kwargs = {key_mapping.get(k0, k0): v0 for k0, v0 in kwargs.items()}
            
            if 'drivername' not in kwargs \
                and {'dialect', 'driver'}.issubset(key_mapping.values()):
                kwargs['drivername'] = f"{kwargs['dialect']}+{kwargs['driver']}".lower()
                                       
            
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
    
    def fit_peewee(self):
        mapping = {
            'user': 'username'
            }
        for k0, v0 in mapping.items():
            self[k0] = self.pop(v0)

        

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
    print(cfg.fit_peewee())
