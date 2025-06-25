# -*- coding: utf-8 -*-
# app/plugins/parser/http.py
"""
HTTP 协议解析器插件
负责将HTTP请求转换为统一格式

功能说明:
1. 解析FastAPI的HTTP请求
2. 转换为BaseRequest统一格式
3. 处理请求体和头部信息
4. 支持配置参数：超时时间、最大请求体大小等
5. 向FastAPI注册路由

依赖模块:
- fastapi: Web框架
- core.base: 基础请求模型
- core.cyber_logger: 日志记录

设计特点:
- 默认配置参数内置
- 请求体大小限制
- 支持所有HTTP方法
- 自动处理路径参数

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

from fastapi import Request
from core.base import BaseRequest
from core.cyber_logger import logger
from utils.proj_trace import proj_trace

class Http:
    """HTTP解析器插件"""
    
    # 默认配置参数
    DEFAULT_CONFIG = {
        "port": 8080,               # 监听端口
        "timeout": 30,               # 请求超时时间（秒）
        "max_body_size": 1048576,    # 最大请求体大小（1MB）
        "allowed_methods": [         # 允许的HTTP方法
            "GET", "POST", "PUT", 
            "DELETE", "PATCH", "HEAD",
            "OPTIONS", "CONNECT"
        ]
    }
    
    def __init__(self):
        """初始化解析器，使用默认配置"""
        proj_trace("app/plugins/parser/http.py", "Http.__init__")
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info(f"🆕 HTTP解析器初始化完成，配置: {self.config}")
    
    async def parse_request(self, raw_request: Request) -> BaseRequest:
        """
        解析原始HTTP请求为统一格式
        
        参数:
            raw_request: FastAPI请求对象
            
        返回:
            BaseRequest: 统一格式的请求对象
            
        异常:
            ValueError: 如果请求体超过最大限制
        """
        proj_trace("app/plugins/parser/http.py", "Http.parse_request", raw_request=raw_request)
        # 记录请求信息
        logger.debug(f"🌐 解析HTTP请求: {raw_request.method} {raw_request.url}")
        
        # 检查HTTP方法是否允许
        if raw_request.method not in self.config["allowed_methods"]:
            error_msg = f"不允许的HTTP方法: {raw_request.method}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # 读取请求体（带大小限制）
        max_size = self.config["max_body_size"]
        body = await raw_request.body()
        
        # 检查请求体大小
        body_size = len(body)
        if body_size > max_size:
            error_msg = f"请求体大小超过限制: {body_size} > {max_size} 字节"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # 创建统一请求对象
        base_request = BaseRequest(
            method=raw_request.method,
            url=str(raw_request.url),
            headers=dict(raw_request.headers),
            params=dict(raw_request.query_params),
            cookies=dict(raw_request.cookies),
            body=body
        )
        
        logger.debug(f"📦 HTTP请求解析完成: {base_request}")
        return base_request
    
    def register_routes(self, app, handler):
        """
        向FastAPI应用注册路由
        
        参数:
            app: FastAPI应用实例
            handler: 请求处理函数
            
        功能:
        - 创建动态路由处理所有路径
        - 支持配置中定义的所有HTTP方法
        """
        proj_trace("app/plugins/parser/http.py", "Http.register_routes", app=app, handler=handler)
        # 获取允许的方法
        methods = self.config["allowed_methods"]
        
        # 创建路由装饰器
        @app.api_route(
            "/{path:path}",
            methods=methods,
            summary="HTTP代理端点",
            description="处理所有HTTP请求的代理端点",
            tags=["HTTP代理"]
        )
        async def proxy_endpoint(request: Request, path: str):
            """
            HTTP代理端点
            处理所有传入的HTTP请求
            
            参数:
                request: FastAPI请求对象
                path: URL路径
            """
            proj_trace("app/plugins/parser/http.py", "proxy_endpoint", request=request, path=path)
            return await handler(request)
        
        logger.info(f"🔗 注册HTTP路由: /{{path:path}} (方法: {methods})")