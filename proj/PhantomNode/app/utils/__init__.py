# -*- coding: utf-8 -*-
# app/utils/__init__.py
"""
工具包初始化文件
定义工具包的结构和公共接口

功能说明:
1. 标记utils为Python包
2. 提供常用工具的快捷导入
3. 封装通用工具函数
4. 提供版本信息

设计原则:
- 保持工具函数独立和无状态
- 提供清晰的文档和类型提示
- 避免在__init__中执行复杂逻辑

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

# 公共导入快捷方式
from .request_id import generate_request_id  # noqa
from .proj_trace import proj_trace

# 工具函数
def safe_get(dictionary, keys, default=None):
    """
    安全获取嵌套字典的值
    
    参数:
        dictionary: 目标字典
        keys: 键列表或单个键
        default: 默认值
        
    返回:
        找到的值或默认值
        
    示例:
        config = {"a": {"b": {"c": 1}}}
        safe_get(config, ["a", "b", "c"])  # 返回 1
        safe_get(config, "a.b.c")          # 返回 1
        safe_get(config, ["a", "x"], 0)    # 返回 0
    """
    proj_trace("app/utils/__init__.py", "safe_get")
    if isinstance(keys, str):
        keys = keys.split('.')
    
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# 版本信息
__version__ = "1.0.0"
__all__ = ['load_parser_plugin', 'load_sender_plugin', 'generate_request_id', 'safe_get']