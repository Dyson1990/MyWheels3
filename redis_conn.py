# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 16:27:16 2022

@author: Weave
"""

import redis

pool = redis.ConnectionPool(host='192.168.1.23', port=6379, decode_responses=True, db=1)
redis_cli = redis.Redis(connection_pool=pool)
    
if __name__ == '__main__':
    import pprint
    