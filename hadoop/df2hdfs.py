#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:30:27 2020

@author: wolf

https://pypi.org/project/PyHDFS/
https://blog.csdn.net/weixin_38070561/article/details/81289601
"""



import pyhdfs

def create_client(ip='192.168.0.116', port='9870'):
    return pyhdfs.HdfsClient(hosts="{}:{}".format(ip, port))
    
# def hdfs_write(cli, f_path):
    # with cli.open(f_path) as fp:
        
    
    
if __name__ == '__main__':
    cli = create_client()
    