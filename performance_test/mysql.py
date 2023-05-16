# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:38:04 2023

@author: Weave
"""

from faker import Faker

try:
    from .. import sql_manager
except:
    import sql_manager
    

# 测试本地MySQL参数
sql_args = {
    'db_dialect': 'MySQL'
    , "host": "192.168.1.23"
    , 'username': "test_usr"
    , "password": "Test_123456"
    , 'dbname': 'tmp'
}

# # print(sql_manager.run_sql(sql_args, 'SELECT * FROM `IN_202002_02_EXP` LIMIT 3'))
# def gen_data(rownum=10000):
#     faker = Faker()
    

if __name__ == "__main__":
    # gen_data()
    engine = sql_manager.__sql_engine(sql_manager.__standardize_args(sql_args))
    print(engine.get_table)