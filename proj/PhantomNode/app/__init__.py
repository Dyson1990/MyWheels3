# -*- coding: utf-8 -*-
# app/__init__.py
"""
应用包初始化文件
定义应用包的结构和公共接口

功能说明:
1. 标记app为Python包
2. 定义包级别的公共变量
3. 提供快捷导入路径
4. 打印启动信息

设计原则:
- 保持简洁，仅包含必要的初始化代码
- 避免在__init__中执行复杂逻辑
- 提供包级别的元数据

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

# 包版本信息
__version__ = "1.0.0"
__author__ = "Dyson1990"
__license__ = "MIT"
__description__ = "PhantomNode - 协议转换代理服务器"

# 公共导入快捷方式
from .core import config_manager, logger  # noqa
from .utils import generate_request_id  # noqa

# 导入跟踪函数
from utils.proj_trace import proj_trace

# 打印启动信息
if __name__ == "__main__":
    proj_trace("app/__init__.py", "__main__")
    print(f"""
    ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝
    ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔██╗ ██║█████╗  
    ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╗██║██╔══╝  
    ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚████║███████╗
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    
    PhantomNode v{__version__} - 协议转换代理服务器
    Author: {__author__}
    License: {__license__}
    """)