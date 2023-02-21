# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 16:27:16 2022

@author: Weave
"""

import redis

def status():
    global redis_cli
    type_dict = {}  # 统计数据类型
    for k0 in redis_cli.keys():
        type0 = redis_cli.type(k0) # 获取数据类型
        type_dict[k0] = type0
    return type_dict
    
if __name__ == '__main__':
    import pprint
    
    for db_num in range(16):
        pool = redis.ConnectionPool(host='192.168.1.23', port=6379, decode_responses=True, db=db_num)
        redis_cli = redis.Redis(connection_pool=pool)
        
        print(db_num)
        print(status())
    