#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-06-21

@author: wolf

代码使用和解析在我的博客
https://blog.csdn.net/weixin_39461443/article/details/93220737?spm=1001.2014.3001.5501
"""

import pkgutil
import os

def get_obj(dir_path, mod_name, obj_name=None):
    """
    dir_path: str 允许传入相对路径
    mod_name: str
    """
    dir_path = os.path.abspath(dir_path) 
    importer = pkgutil.get_importer(dir_path) # 返回一个FileFinder对象
    loader = importer.find_module(mod_name) # 返回一个SourceFileLoader对象
    mod = loader.load_module() # 返回需要的模块
    if obj_name:
        obj = getattr(mod, obj_name)
        return obj
    else:
        return mod
