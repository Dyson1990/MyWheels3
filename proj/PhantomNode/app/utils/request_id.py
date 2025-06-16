# -*- coding: utf-8 -*-
# app/utils/request_id.py
"""
请求ID生成工具
为每个请求生成唯一的ID用于追踪

功能说明:
1. 生成基于时间戳的唯一ID
2. 保证分布式环境中的唯一性
3. 支持自定义前缀
4. 简洁易读的ID格式

设计特点:
- 使用UUID保证全局唯一性
- 包含时间戳方便排序
- 支持自定义前缀区分请求类型
- 生成速度快，适合高并发环境

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import uuid
import time
import socket
import os
from .proj_trace import proj_trace

# 主机标识（使用主机名和进程ID）
HOST_ID = f"{socket.gethostname()}-{os.getpid()}"

def generate_request_id(prefix="REQ"):
    """
    生成唯一请求ID
    
    参数:
        prefix: 请求ID前缀
        
    返回:
        格式为 {前缀}-{时间戳}-{主机}-{随机UUID} 的字符串
    """
    proj_trace("app/utils/request_id.py", "generate_request_id", prefix=prefix)
    # 获取当前时间戳（毫秒级）
    timestamp = int(time.time() * 1000)
    
    # 生成UUID的一部分（保证唯一性）
    uuid_part = str(uuid.uuid4())[:8]
    
    # 组合ID
    return f"{prefix}-{timestamp}-{HOST_ID}-{uuid_part}"