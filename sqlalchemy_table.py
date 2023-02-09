#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:14:50 2021

@author: wolf

还在研究中，不用peewee主要是pandas不支持
"""
import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm

import base64

class TableObj:
    
    def __init__(self, table_name, engine=None):
        self.schema = engine.url.database
        self.name = table_name
        self.full_name = '.'.join([self.schema, self.name])
        self.engine = engine
        self.table = None
        
        # 映射到数据库中的schema
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(engine, schema=self.schema) # sql_args['dbname'].lower()
        self.t_meta = metadata.tables.get(self.full_name)
        # print(dir(engine.url))
        # print((engine.url.database))
        
        if isinstance(self.t_meta, type(None)):
            print(metadata.tables.keys())
            raise Exception('数据库表格“'+table_name+'”不存在')
        self.metadata = metadata
        

    def prepare(self, add_primary_key='rownum'):
        if not self.t_meta.primary_key.columns.items():
            print('warning: 表格“'+self.t_meta.name+\
                  '”中不包括主键，准备添加'+add_primary_key+'主键')
            sql_str = 'ALTER TABLE `{}`.`{}` ADD COLUMN `{}` BIGINT(30) AUTO_INCREMENT PRIMARY KEY'
            self.engine.execute(sql_str.format(self.t_meta.schema
                                               , self.t_meta.name
                                               , add_primary_key
                                               )
            )
        
        self.base = sqlalchemy.ext.automap.automap_base(metadata=self.metadata)
        self.base.prepare()
        
        self.table = self.base.classes.get(self.name)
        # self.table = getattr(self.base.classes, self.name)
        
if __name__ == '__main__':
    eng_str = {
            'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
            , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
            }
    
    sql_args = {'db_dialect': 'mysql'
                 , 'db_driver': 'pymysql'
                 , 'host': '127.0.0.1'
                 , 'user': 'Dyson'
                 , 'password': base64.b64decode(b'MXFxYXEx').decode()
                 , 'dbname': 'employees'
                 # , 'data_type': 'DataFrame'
                 , 'charset': 'utf8mb4'
                 , 'port': '3306'
                 # , 'method': None
     }
    
    db_dialect = sql_args['db_dialect']
    data_engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args)
                                            # , execution_options={'stream_results': True}
                                            # , pool_recycle=3
                                            # , pool_pre_ping=True
                                            )
    obj = TableObj('employees', engine=data_engine)
    obj.prepare()
    
    stmt = sqlalchemy.select(obj.table).where(obj.table.gender == 'M')
    with obj.engine.connect() as conn:
         for row in conn.execute(stmt):
             print(row)
             break
