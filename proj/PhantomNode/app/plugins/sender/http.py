# -*- coding: utf-8 -*-
# app/plugins/sender/http.py
"""
HTTP 发送器插件
负责将统一请求格式发送到目标HTTP服务器

功能说明:
1. 接收BaseRequest统一格式的请求
2. 转换为HTTP请求并发送到目标服务器
3. 处理响应并转换为标准格式
4. 支持连接池和超时设置

依赖模块:
- aiohttp: 异步HTTP客户端
- core.base: 基础请求模型
- core.cyber_logger: 日志记录

设计特点:
- 使用HTTP连接池提高性能
- 支持HTTPS
- 自动处理重定向
- 详细的错误处理机制

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import aiohttp
from core.cyber_logger import logger
from utils.proj_trace import proj_trace

class Http:
    """HTTP发送器插件"""
    
    # 默认配置参数
    DEFAULT_CONFIG = {
        "timeout": 30,             # 默认超时时间（秒）
        "max_connections": 100,    # 最大连接数
        "keepalive_timeout": 15,   # 连接保持时间（秒）
        "verify_ssl": True,        # 是否验证SSL证书
        "user_agent": "PhantomNode/1.0"  # 默认用户代理
    }
    
    def __init__(self):
        """初始化HTTP发送器"""
        proj_trace("app/plugins/sender/http.py", "Http.__init__")
        self.config = self.DEFAULT_CONFIG.copy()
        self.session = None
        logger.info(f"🆕 HTTP发送器初始化完成，配置: {self.config}")
    
    async def send_request(self, base_request):
        """
        发送HTTP请求到目标服务器
        
        参数:
            base_request: 统一格式的请求对象
            
        返回:
            响应对象 (status_code, headers, body)
        """
        proj_trace("app/plugins/sender/http.py", "Http.send_request", base_request=base_request)
        logger.info(f"🚀 发送HTTP请求 [{base_request.request_id}]: {base_request.method} {base_request.url}")
        
        if not self.session:
            await self._create_session()
        
        try:
            # 准备请求参数
            headers = base_request.headers.copy()
            headers.setdefault("User-Agent", self.config["user_agent"])
            
            # 发送请求
            async with self.session.request(
                method=base_request.method,
                url=base_request.url,
                params=base_request.params,
                headers=headers,
                cookies=base_request.cookies,
                data=base_request.body,
                allow_redirects=True,
                ssl=not self.config["verify_ssl"]
            ) as response:
                # 读取响应内容
                response_body = await response.read()
                
                # 构建响应对象
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": response_body
                }
        
        except aiohttp.ClientError as e:
            logger.error(f"❌ HTTP请求失败 [{base_request.request_id}]: {str(e)}")
            return {
                "status": 502,
                "headers": {"Content-Type": "text/plain"},
                "body": f"HTTP Proxy Error: {str(e)}".encode()
            }
        except Exception as e:
            logger.error(f"💥 未知HTTP错误 [{base_request.request_id}]: {str(e)}")
            return {
                "status": 500,
                "headers": {"Content-Type": "text/plain"},
                "body": f"Internal Server Error: {str(e)}".encode()
            }
    
    async def _create_session(self):
        """创建aiohttp会话"""
        proj_trace("app/plugins/sender/http.py", "Http._create_session")
        # 创建连接池
        connector = aiohttp.TCPConnector(
            limit=self.config["max_connections"],
            ssl=not self.config["verify_ssl"]
        )
        
        # 创建会话
        timeout = aiohttp.ClientTimeout(total=self.config["timeout"])
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        logger.info(f"🔗 创建HTTP会话 (连接数: {self.config['max_connections']})")
    
    async def close(self):
        """关闭HTTP会话"""
        proj_trace("app/plugins/sender/http.py", "Http.close")
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("🔌 HTTP会话已关闭")