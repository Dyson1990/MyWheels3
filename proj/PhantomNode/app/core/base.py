# -*- coding: utf-8 -*-
# app/core/base.py
"""
基础请求模型
定义统一的数据结构，用于在解析器和发送器之间传递请求信息

功能说明:
1. 封装HTTP请求的核心元素：方法、URL、头信息、参数等
2. 提供统一的数据结构，便于不同协议插件之间的转换
3. 包含请求ID用于追踪

设计特点:
- 使用简单类结构，无复杂继承关系
- 包含所有必要的HTTP请求元素
- 提供友好的字符串表示

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

from utils.proj_trace import proj_trace

class BaseRequest:
    """统一请求模型，用于在不同协议插件间传递请求信息"""
    
    def __init__(self, **kwargs):
        """
        初始化基础请求对象
        
        参数:
            request_id: 唯一请求ID (自动生成)
            method: HTTP方法 (GET/POST/PUT/DELETE等)
            url: 目标URL
            headers: 请求头字典
            body: 请求体内容 (bytes)
            params: 查询参数字典
            cookies: Cookies字典
        """
        proj_trace("app/core/base.py", "BaseRequest.__init__", kwargs=kwargs)
        # 请求唯一标识
        self.request_id = kwargs.get('request_id', '')
        
        # HTTP方法
        self.method = kwargs.get('method', 'GET')
        
        # 目标URL
        self.url = kwargs.get('url', '')
        
        # 请求头
        self.headers = kwargs.get('headers', {})
        
        # 请求体
        self.body = kwargs.get('body', None)
        
        # 查询参数
        self.params = kwargs.get('params', {})
        
        # Cookies
        self.cookies = kwargs.get('cookies', {})
    
    def __str__(self):
        """返回请求的简要描述"""
        proj_trace("app/core/base.py", "BaseRequest.__str__")
        return f"[{self.request_id}] {self.method} {self.url}"
    
    def to_dict(self):
        """将请求对象转换为字典（用于日志记录）"""
        proj_trace("app/core/base.py", "BaseRequest.to_dict")
        return {
            "request_id": self.request_id,
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "body_size": len(self.body) if self.body else 0,
            "params": self.params,
            "cookies": self.cookies
        }