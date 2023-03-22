# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:21:31 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent

from kazoo.client import KazooClient
import contextlib

from loguru import logger


class ZooKeeperConnect(KazooClient):
    def __init__(self, host, port):
        self.zk = KazooClient(hosts=f'{host}:{port}', use_ssl=False)
    
    @contextlib.contextmanager
    def connection(self):
        logger.info("Opening Zookeeper connection.")
        self.zk.start()
        yield self # 类似于使用__enter__
        
        logger.info("Closing Zookeeper connection.")
        self.zk.stop()
        return None # 类似于使用__exit__
    
# =============================================================================
#     def __enter__(self):
#         self.zk.start()
#         return self
#     
#     def __exit__(self, *args):
#         self.zk.stop()
# =============================================================================
        
    # 目前大部分功能用处不大已经删除

if __name__ == "__main__":
    # sharding_rules = ShardingRules()
    # sharding_rules.upload()
    with ZooKeeperConnect("192.168.1.24", "21810").connection() as obj:
        print(obj.get)
