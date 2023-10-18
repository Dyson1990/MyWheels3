# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:22:13 2023

@author: Weave
"""


import requests
import importlib.util
import types
import sys

from loguru import logger

class RemotePyCode():
    def __init__(self, source="github", owner="Dyson1990", repo="MyWheels3", branch=None):
        self.owner=owner
        self.repo=repo
        self.source=source
        self.branch=branch
        self.pycode_raw=None
        
        if self.source.lower() == "github": # 从GitHub API获取源代码并打包成字节码
            self.api_url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{{module_p}}'
            self.params = {'ref': self.branch} if self.branch else None
            self.headers = {'Accept': 'application/vnd.github.v3.raw'}
        else:
            raise Exception(f"unknown source: {self.source}")
    
    def create_module(self, module_p, module_name='', version=None, v2ray=True):
        # 如果指定了版本，构建带版本信息的 URL
        if version:
            url = self.api_url.format(module_p=module_p) + f"?ref={version}"
        else:
            url = self.api_url.format(module_p=module_p)
            logger.warning("unknown version, may receive unwanted module!")
        
        if v2ray:
            proxies = {'http': 'socks5://127.0.0.1:10808'
                       , 'https': 'socks5://127.0.0.1:10808'}
        else:
            proxies = None
        response = requests.get(url
                                , params=self.params
                                , headers=self.headers
                                , proxies=proxies
                               )
        pycode_raw = response.text

        if not pycode_raw:
            raise Exception(f"empty remote python file.")

        if not module_name:
            module_name = module_p.split("/")[-1].split(".")[0]
        
        spec = importlib.util.spec_from_loader(module_name, loader=None, origin="<string>") # 创建规范
        new_module = types.ModuleType(spec.name) # 创建新模块对象
        
        try:
            exec(pycode_raw, new_module.__dict__) # 在新模块中执行 Python 代码
        except Exception as e0:
            logger.error(f"error in py code:{e0}\n{pycode_raw}")
            return None
        
        # 将新模块添加到 sys.modules 字典中和全局命名空间中
        sys.modules[spec.name] = new_module
        globals()[spec.name] = new_module

        # 为新对象增加一些常用属性
        new_module.__script__ = pycode_raw 
        
        return new_module # 返回新创建的模块对象

if __name__ == "__main__":
    github_con = RemotePyCode()
    requests_mgr = github_con.create_module("requests_mgr.py")

    print(dir(requests_mgr))
