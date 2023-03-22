#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:30:27 2020

@author: wolf

https://pypi.org/project/PyHDFS/
https://blog.csdn.net/weixin_38070561/article/details/81289601
"""



import pyhdfs
import os
import contextlib

from pathlib import Path
from loguru import logger

class HDFSConn():
    
    def __init__(self, host='192.168.1.190', port='9870'):
        self.cli = pyhdfs.HdfsClient(hosts=f"{host}:{port}", user_name="wolf")

if __name__ == '__main__':
    with HDFSConn().connection() as conn:
        print(dir(conn.cli))
        
    # cli.copy_from_local(local_path._str, hdfs_path.as_posix())
        
    # print(cli.listdir(hdfs_dir.as_posix()))
    # print(cli.list_status(os.path.split(hdfs_path.as_posix())[0]))
    # print(cli.list_status(hdfs_path.as_posix()))