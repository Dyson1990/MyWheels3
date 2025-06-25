# -*- coding: utf-8 -*-
# app/core/cyber_logger.py
"""
赛博风格日志记录器
提供增强的日志记录功能，支持赛博风格格式

功能说明:
1. 自定义日志格式（包含请求ID、时间戳、日志级别等）
2. 支持彩色终端输出
3. 动态设置日志级别
4. 集成请求ID追踪
5. 添加函数调用跟踪功能

设计特点:
- 使用Python标准logging模块
- 线程安全，适合异步环境
- 可扩展的文件/网络日志处理
- 自动从配置获取日志级别

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import logging
import sys
from logging import Formatter, StreamHandler
from utils.request_id import generate_request_id
from pathlib import Path


# 日志级别颜色映射
COLORS = {
    'DEBUG': '\033[94m',    # 蓝色
    'INFO': '\033[92m',     # 绿色
    'WARNING': '\033[93m',  # 黄色
    'ERROR': '\033[91m',    # 红色
    'CRITICAL': '\033[95m', # 紫色
    'ENDC': '\033[0m'       # 结束颜色
}

log_level = "INFO"
log_p = Path(__file__).parent.parent.joinpath("logs/process.log")
logging.basicConfig(level=logging.INFO
                    , filename=log_p.as_posix()
                    , encoding='utf-8'
                    )

class CyberFormatter(Formatter):
    """赛博风格日志格式化器"""
    
    def __init__(self, fmt=None, datefmt=None):
        # 使用父类默认格式或自定义格式
        fmt = fmt or '[%(asctime)s] [%(request_id)s] [%(name)s] [%(levelname)s] > %(message)s'
        datefmt = datefmt or '%Y-%m-%d %H:%M:%S'
        super().__init__(fmt=fmt, datefmt=datefmt)
    
    def format(self, record):
        """格式化日志记录"""
        # 确保有request_id属性
        if not hasattr(record, 'request_id'):
            record.request_id = 'SYSTEM'
        
        # 调用父类格式化
        message = super().format(record)
        
        # 添加颜色（如果终端支持）
        if sys.stderr.isatty():
            color = COLORS.get(record.levelname, COLORS['ENDC'])
            message = f"{color}{message}{COLORS['ENDC']}"
        
        return message

class RequestIDFilter(logging.Filter):
    """请求ID过滤器，为日志记录添加请求ID"""
    
    def filter(self, record):
        """添加请求ID到日志记录"""
        if not hasattr(record, 'request_id'):
            record.request_id = generate_request_id()
        return True

def setup_logger():
    """设置赛博风格日志记录器"""
    # 创建根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 设置最高级别，实际级别由处理器控制
    
    # 创建控制台处理器
    console_handler = StreamHandler(sys.stdout)
    
    # 设置日志级别（从配置获取）
    global log_level
    log_level = getattr(logging, log_level, logging.INFO)
    console_handler.setLevel(log_level)
    
    # 添加请求ID过滤器
    console_handler.addFilter(RequestIDFilter())
    
    # 设置赛博风格格式化器
    formatter = CyberFormatter()
    console_handler.setFormatter(formatter)
    
    # 添加到根日志记录器
    logger.addHandler(console_handler)
    
    return logger

# 初始化全局日志记录器
logger = setup_logger()