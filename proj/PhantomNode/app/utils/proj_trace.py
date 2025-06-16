# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 23:08:20 2025

@author: Dyson
"""
import logging
import os

# 添加跟踪参数和函数
trace = True  # 新增跟踪开关

def proj_trace(file_path, func_name, **kwargs):
    """
    跟踪函数调用并记录到process.log
    
    参数:
        file_path: 调用函数的源代码文件路径
        func_name: 函数名
        kwargs: 函数的所有参数（关键字参数形式）
    """
    if trace:
        # 创建跟踪日志记录器
        trace_logger = logging.getLogger("trace_logger")
        trace_logger.setLevel(logging.INFO)
        
        # 确保只有一个文件处理器
        if not trace_logger.handlers:
            # 创建文件处理器
            file_handler = logging.FileHandler("process.log", mode="a", encoding="utf-8")
            
            # 设置日志格式
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            file_handler.setFormatter(formatter)
            
            # 添加到日志记录器
            trace_logger.addHandler(file_handler)
            
            # 防止日志传播到根记录器
            trace_logger.propagate = False
        
        # 提取文件名（不带路径）
        filename = os.path.basename(file_path)
        
        # 构造日志消息
        params_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        message = f"{filename} - {func_name}({params_str})"
        
        # 记录日志
        trace_logger.info(message)
