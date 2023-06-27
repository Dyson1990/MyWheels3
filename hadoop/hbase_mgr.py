# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:13:01 2023

@author: Weave
"""

import happybase
import contextlib
import time

from loguru import logger

class HbaseConn():
    
    def __init__(self, host="192.168.1.122", port=9090, size=3):

        # HOST: HBase数据库ip
        # PORT: 端口号
        self.pool = happybase.ConnectionPool(size=3, host=host, port=port)
        
    @contextlib.contextmanager
    def connection(self):
        logger.info("Opening Hbase connection.")
        self.conn = self.pool.connection().__enter__()
        
        yield self # 类似于使用__enter__
        
        logger.info("Closing Hbase connection.")
        self.conn.close()
        return None # 类似于使用__exit__
    
    def show_tables(self):
        return self.conn.tables()
        
        
if __name__ == "__main__":
    
    # host = "192.168.1.122"
    # port = 9090
    # conn = happybase.Connection(host, port, timeout=3000000)

    # # conn.open()
    # print(type(conn))
    # # print(conn.tables())
    # # conn.close()
    
    with HbaseConn().connection() as conn:
        print(conn.show_tables())
        time.sleep(10)
