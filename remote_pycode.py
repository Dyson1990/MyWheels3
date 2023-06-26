# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:22:13 2023

@author: Weave
"""


import requests
import importlib.util
import types
import sys

def from_github(branch, module_p):
    owner = "Dyson1990"
    repo = "MyWheels3"
    # 从GitHub API获取源代码并打包成字节码
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{module_p}'
    params = {'ref': branch} if branch else None
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = requests.get(url, params=params, headers=headers)
    source_code_raw = response.text
    
    return source_code_raw

def create_module(long_text, module_name):
    # 创建规范
    spec = importlib.util.spec_from_loader(module_name, loader=None, origin="<string>")
    
    # 创建新模块对象
    new_module = types.ModuleType(spec.name)
    
    # 在新模块中执行 Python 代码
    exec(long_text, new_module.__dict__)
    
    # 将新模块添加到 sys.modules 字典中和全局命名空间中
    sys.modules[spec.name] = new_module
    globals()[spec.name] = new_module
    
    # 返回新创建的模块对象
    return new_module

if __name__ == "__main__":
    branch = "master"
    module_p = "sql_manager.py"

    # 从Github中读取mysql_manager.py文件，得到my_module对象
    source_code_raw = from_github(branch, module_p)
    module_name = "my_module"
    new_module = create_module(source_code_raw, module_name)
    
    # 调用新模块的 hello() 函数
    print(new_module.check_json)
    
    
    # bytecode = cloudpickle.dumps(obj)
    # print(bytecode)
    # 在远程服务器上反序列化并执行字节码
    # my_module = cloudpickle.loads(bytecode)
    # return my_module