# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:22:13 2023

@author: Weave
"""


import requests
import importlib.util
import types
import sys

class RemotePyCode():
    def __init__(self, source="github", owner="Dyson1990", repo="MyWheels3", branch=None):
        self.owner=owner
        self.repo=repo
        self.source=source
        self.branch=branch
        
        if self.source.lower() == "github": # 从GitHub API获取源代码并打包成字节码
            self.api_url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{{module_p}}'
            self.params = {'ref': self.branch} if self.branch else None
            self.headers = {'Accept': 'application/vnd.github.v3.raw'}
        else:
            raise Exception(f"unknown source: {self.source}")
    
    def create_module(self, module_p, module_name=''):
        url = self.api_url.format(module_p=module_p)
        response = requests.get(url
                                , params=self.params
                                , headers=self.headers
                               )
        self.pycode_raw = response.text
        
        # 创建规范
        spec = importlib.util.spec_from_loader(module_name, loader=None, origin="<string>")
        
        # 创建新模块对象
        new_module = types.ModuleType(spec.name)
        
        # 在新模块中执行 Python 代码
        exec(self.pycode_raw, new_module.__dict__)
        
        # 将新模块添加到 sys.modules 字典中和全局命名空间中
        sys.modules[spec.name] = new_module
        globals()[spec.name] = new_module
        
        # 返回新创建的模块对象
        return new_module

if __name__ == "__main__":
    github_con = RemotePyCode()
    requests_mgr = github_con.create_module("requests_mgr.py")

    print(dir(requests_mgr))
