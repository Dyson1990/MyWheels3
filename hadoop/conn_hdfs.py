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
import pandas as pd
import pprint
from pathlib import Path

def create_client(ip='192.168.0.116', port='9870'):
    return pyhdfs.HdfsClient(hosts="{}:{}".format(ip, port)
                             , user_name="wolf")

if __name__ == '__main__':
    cli = create_client()
    cli.mkdirs('/tmp/test')
    
    file_name = "Alice.txt"
    local_dir = Path(r"C:\Users\Administrator.SC-202001091919")
    hdfs_dir = Path(r'/tmp/test')
    
    # local_path = os.path.join(local_dir, file_name)
    # hdfs_path = os.path.join(hdfs_dir, file_name)
    local_path = Path(local_dir, file_name)
    hdfs_path = Path(hdfs_dir, file_name)
    
    print(local_path,'\n', hdfs_path)
    
    if cli.exists(hdfs_path.as_posix()):
        cli.delete(hdfs_path.as_posix())
        
    cli.copy_from_local(local_path._str, hdfs_path.as_posix())
    
    # with cli.open(hdfs_path._str) as fp:
    #     if os.path.splitext(file_name)[-1] == '.csv':
    #         pprint.pprint(pd.read_table(fp, sep=','))
    #     else:
    #         pprint.pprint(fp.read(100))
        
    print(cli.listdir(hdfs_dir.as_posix()))
    print(cli.list_status(os.path.split(hdfs_path.as_posix())[0]))
    print(cli.list_status(hdfs_path.as_posix()))