# -*- coding: utf-8 -*-
# app/plugins/parser/socks.py
"""
SOCKS 协议解析器插件
负责将SOCKS请求转换为统一格式

功能说明:
1. 解析SOCKS协议请求
2. 转换为BaseRequest统一格式
3. 支持SOCKS4和SOCKS5协议
4. 处理认证和连接请求
5. 向FastAPI注册路由

依赖模块:
- python-socks: SOCKS协议处理库 (需安装: `pip install python-socks`)
- core.base: 基础请求模型
- core.cyber_logger: 日志记录

设计特点:
- 支持SOCKS4和SOCKS5协议
- 内置认证机制
- 异步连接处理
- 详细的日志记录

注意:
- 此插件需要额外依赖python-socks
- 实际实现需要创建TCP服务器处理连接

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import asyncio
from core.base import BaseRequest
from core.cyber_logger import logger
from utils.proj_trace import proj_trace

class Socks:
    """SOCKS解析器插件"""
    
    # 默认配置参数
    DEFAULT_CONFIG = {
        "port": 1080,           # 监听端口
        "protocol": "socks5",   # 支持的协议版本 (socks4/socks5)
        "auth_required": True,  # 是否需要认证
        "users": {              # 认证用户列表
            "admin": "password123"
        }
    }
    
    def __init__(self):
        """初始化解析器，使用默认配置"""
        proj_trace("app/plugins/parser/socks.py", "Socks.__init__")
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info(f"🆕 SOCKS解析器初始化完成，配置: {self.config}")
    
    async def parse_request(self, raw_request) -> BaseRequest:
        """
        解析原始SOCKS请求为统一格式
        
        参数:
            raw_request: SOCKS请求对象（来自python-socks）
            
        返回:
            BaseRequest: 统一格式的请求对象
        """
        proj_trace("app/plugins/parser/socks.py", "Socks.parse_request", raw_request=raw_request)
        # 记录请求信息
        logger.debug(f"🌐 解析SOCKS请求: {raw_request.cmd} {raw_request.dest_host}:{raw_request.dest_port}")
        
        # 创建统一请求对象
        base_request = BaseRequest(
            method="CONNECT",  # SOCKS总是连接请求
            url=f"{raw_request.dest_host}:{raw_request.dest_port}",
            headers=self._extract_headers(raw_request),
            body=None
        )
        
        logger.debug(f"📦 SOCKS请求解析完成: {base_request}")
        return base_request
    
    def _extract_headers(self, raw_request):
        """从SOCKS请求中提取头部信息"""
        proj_trace("app/plugins/parser/socks.py", "Socks._extract_headers", raw_request=raw_request)
        headers = {}
        
        # 添加源地址信息
        headers["X-SOCKS-Source-Address"] = raw_request.src_addr
        headers["X-SOCKS-Source-Port"] = str(raw_request.src_port)
        
        # 添加协议版本
        headers["X-SOCKS-Protocol"] = self.config["protocol"]
        
        # 添加命令类型
        headers["X-SOCKS-Command"] = raw_request.cmd
        
        return headers
    
    def register_routes(self, app, handler):
        """
        向FastAPI应用注册路由
        
        参数:
            app: FastAPI应用实例
            handler: 请求处理函数
            
        功能:
        - 创建TCP服务器处理SOCKS连接
        - 集成到FastAPI生命周期
        """
        proj_trace("app/plugins/parser/socks.py", "Socks.register_routes", app=app, handler=handler)
        # 注意: SOCKS协议需要独立TCP服务器
        logger.info("🔌 SOCKS协议需要独立TCP服务器，将在startup事件中初始化")
        
        # 在应用启动时创建SOCKS服务器
        @app.on_event("startup")
        async def start_socks_server():
            """启动SOCKS服务器"""
            proj_trace("app/plugins/parser/socks.py", "start_socks_server")
            try:
                # 创建TCP服务器
                server = await asyncio.start_server(
                    self.handle_socks_connection,
                    host="0.0.0.0",
                    port=self.config["port"]
                )
                
                # 存储服务器实例
                app.state.socks_server = server
                logger.info(f"🔌 SOCKS服务器启动: 0.0.0.0:{self.config['port']}")
            except Exception as e:
                logger.error(f"❌ 启动SOCKS服务器失败: {str(e)}")
        
        # 在应用关闭时关闭SOCKS服务器
        @app.on_event("shutdown")
        async def stop_socks_server():
            """关闭SOCKS服务器"""
            proj_trace("app/plugins/parser/socks.py", "stop_socks_server")
            if hasattr(app.state, 'socks_server'):
                server = app.state.socks_server
                server.close()
                await server.wait_closed()
                logger.info("🔌 SOCKS服务器已关闭")
    
    async def handle_socks_connection(self, reader, writer):
        """
        处理SOCKS连接
        
        参数:
            reader: asyncio.StreamReader
            writer: asyncio.StreamWriter
            
        功能:
        1. 处理SOCKS握手
        2. 认证客户端
        3. 解析请求
        4. 调用处理函数
        """
        proj_trace("app/plugins/parser/socks.py", "Socks.handle_socks_connection", reader=reader, writer=writer)
        # 获取客户端地址
        addr = writer.get_extra_info('peername')
        logger.info(f"🔌 新SOCKS连接: {addr[0]}:{addr[1]}")
        
        try:
            # SOCKS握手和认证
            if self.config["protocol"] == "socks5":
                await self._handle_socks5_handshake(reader, writer)
            elif self.config["protocol"] == "socks4":
                await self._handle_socks4_handshake(reader, writer)
            
            # 解析请求
            # 这里需要实现完整的SOCKS请求解析
            # 实际开发中应使用python-socks库
            
            # 创建虚拟请求对象
            class DummyRequest:
                def __init__(self):
                    self.cmd = "CONNECT"
                    self.dest_host = "example.com"
                    self.dest_port = 80
                    self.src_addr = addr[0]
                    self.src_port = addr[1]
            
            # 解析请求
            base_request = await self.parse_request(DummyRequest())
            
            # 调用处理函数
            response = await handler(base_request)
            
            # 处理响应（这里简化处理）
            writer.write(b"HTTP/1.1 200 OK\r\n\r\nSOCKS Proxy Connected")
            await writer.drain()
            
        except Exception as e:
            logger.error(f"❌ SOCKS连接处理失败: {str(e)}")
            writer.write(f"HTTP/1.1 500 Error: {str(e)}\r\n\r\n".encode())
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def _handle_socks5_handshake(self, reader, writer):
        """处理SOCKS5握手和认证"""
        proj_trace("app/plugins/parser/socks.py", "Socks._handle_socks5_handshake", reader=reader, writer=writer)
        # 读取客户端支持的认证方法
        data = await reader.read(2)
        nmethods = data[1]
        methods = await reader.read(nmethods)
        
        # 选择认证方法（无认证或用户名密码认证）
        if self.config["auth_required"]:
            writer.write(b"\x05\x02")  # 选择用户名/密码认证
            await writer.drain()
            
            # 处理认证
            auth = await reader.read(2)
            ulen = auth[1]
            username = (await reader.read(ulen)).decode()
            plen = auth[ulen+1]
            password = (await reader.read(plen)).decode()
            
            # 验证用户名和密码
            if username in self.config["users"] and self.config["users"][username] == password:
                writer.write(b"\x01\x00")  # 认证成功
                await writer.drain()
            else:
                writer.write(b"\x01\x01")  # 认证失败
                await writer.drain()
                raise ConnectionError("SOCKS5认证失败")
        else:
            writer.write(b"\x05\x00")  # 不需要认证
            await writer.drain()
    
    async def _handle_socks4_handshake(self, reader, writer):
        """处理SOCKS4握手"""
        proj_trace("app/plugins/parser/socks.py", "Socks._handle_socks4_handshake", reader=reader, writer=writer)
        # 读取请求
        data = await reader.read(9)
        command = data[1]
        port = int.from_bytes(data[2:4], 'big')
        ip = ".".join(str(b) for b in data[4:8])
        
        # 读取用户ID
        user_id = ""
        while True:
            b = await reader.read(1)
            if b == b"\x00":
                break
            user_id += b.decode()
        
        # 验证SOCKS4请求
        if command != 0x01:
            writer.write(b"\x00\x5b")  # 连接拒绝
            await writer.drain()
            raise ValueError(f"不支持的SOCKS4命令: {command}")
        
        # 不需要认证时直接接受连接
        writer.write(b"\x00\x5a")  # 连接成功
        await writer.drain()