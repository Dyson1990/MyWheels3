# -*- coding: utf-8 -*-
# app/core/schedule.py
"""
核心调度模块
负责管理插件、处理请求路由和任务调度

功能说明:
1. 加载解析器和发送器插件
2. 为解析器设置路由处理
3. 实现三种路由模式：默认模式、映射模式、自定义模式
4. 管理请求处理的生命周期
5. 处理插件加载异常

依赖模块:
- utils.plugin_loader: 动态加载插件
- utils.request_id: 生成唯一请求ID
- core.config_mgr: 管理应用配置
- core.cyber_logger: 日志记录

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import asyncio
from .plugin_loader import load_parser_plugin, load_sender_plugin
from utils.request_id import generate_request_id
from .config_mgr import config_manager
from .cyber_logger import logger
from utils.proj_trace import proj_trace

class Dispatcher:
    """核心调度器，管理请求处理流程"""
    
    def __init__(self, app):
        """
        初始化调度器
        
        参数:
            app: FastAPI应用实例
        """
        proj_trace("app/core/schedule.py", "Dispatcher.__init__", app=app)
        self.app = app
        
        # 存储加载的解析器插件 {插件文件名: 插件实例}
        self.parsers = {}
        
        # 存储加载的发送器插件 {插件文件名: 插件实例}
        self.senders = {}
        
        # 请求计数器
        self.request_count = 0
    
    def load_plugins(self):
        """加载所有插件 - 从路由配置中自动发现需要的插件"""
        proj_trace("app/core/schedule.py", "Dispatcher.load_plugins")
        config = config_manager.config
        routing = config["routing"]
        
        # 收集所有需要加载的解析器插件
        parser_files = set()
        
        # 收集所有需要加载的发送器插件
        sender_files = set()
        
        # 添加默认发送器
        default_sender = routing["default_sender"]
        sender_files.add(default_sender)
        
        # 映射模式中的插件
        if routing["mode"] == "mapping":
            for mapping in routing["mapping"]:
                parser_files.add(mapping["parser"])
                sender_files.add(mapping["sender"])
        
        # 自定义模式中的插件（预留）
        if routing["mode"] == "custom":
            # 这里可以添加自定义模式需要的插件
            pass
        
        # 加载解析器插件
        for plugin_file in parser_files:
            try:
                self.parsers[plugin_file] = load_parser_plugin(plugin_file)
                logger.info(f"✅ 加载解析器插件: {plugin_file}")
            except Exception as e:
                logger.error(f"❌ 加载解析器插件失败 {plugin_file}: {str(e)}")
                if config_manager.should_terminate_on_plugin_fail():
                    raise RuntimeError(f"解析器插件加载失败: {plugin_file}")
        
        # 加载发送器插件
        for plugin_file in sender_files:
            try:
                self.senders[plugin_file] = load_sender_plugin(plugin_file)
                logger.info(f"✅ 加载发送器插件: {plugin_file}")
            except Exception as e:
                logger.error(f"❌ 加载发送器插件失败 {plugin_file}: {str(e)}")
                if config_manager.should_terminate_on_plugin_fail():
                    raise RuntimeError(f"发送器插件加载失败: {plugin_file}")
    
    def setup_routes(self):
        """为每个解析器设置路由处理"""
        proj_trace("app/core/schedule.py", "Dispatcher.setup_routes")
        for parser_name, parser in self.parsers.items():
            # 为每个解析器创建请求处理函数
            handler = self.create_handler(parser_name)
            
            # 注册路由
            parser.register_routes(self.app, handler)
            logger.info(f"🔗 为解析器注册路由: {parser_name}")
    
    def create_handler(self, parser_name):
        """
        创建请求处理函数闭包
        
        参数:
            parser_name: 解析器名称
            
        返回:
            请求处理函数
        """
        proj_trace("app/core/schedule.py", "Dispatcher.create_handler", parser_name=parser_name)
        
        async def handler(raw_request):
            """
            实际处理请求的函数
            1. 生成唯一请求ID
            2. 解析请求
            3. 路由到发送器
            4. 发送请求并返回响应
            """
            proj_trace("app/core/schedule.py", "Dispatcher.create_handler.handler", raw_request=raw_request)
            # 生成唯一请求ID
            request_id = generate_request_id()
            self.request_count += 1
            
            try:
                logger.info(f"🔁 处理请求 [{request_id}] (总数: {self.request_count})")
                
                # 使用解析器转换请求
                base_request = await self.parsers[parser_name].parse_request(raw_request)
                base_request.request_id = request_id
                
                # 记录解析后的请求信息
                logger.debug(f"📦 解析后的请求: {base_request}")
                
                # 路由到发送器
                sender_name = self.route_to_sender(parser_name)
                sender = self.senders.get(sender_name)
                
                if not sender:
                    logger.error(f"🚫 找不到发送器: {sender_name}")
                    return {"error": "Internal server error"}, 500
                
                # 发送请求
                logger.debug(f"🚀 发送请求到 {sender_name}")
                response = await sender.send_request(base_request)
                
                # 返回响应
                return response
            except Exception as e:
                logger.error(f"💥 请求处理失败 [{request_id}]: {str(e)}")
                return {"error": "Internal server error"}, 500
        
        return handler
    
    def route_to_sender(self, parser_name):
        """
        路由到发送器 - 实现三种路由模式
        
        参数:
            parser_name: 当前请求的解析器名称
            
        返回:
            目标发送器的名称
        """
        proj_trace("app/core/schedule.py", "Dispatcher.route_to_sender", parser_name=parser_name)
        routing = config_manager.routing_config
        mode = routing["mode"]
        
        # 1. 默认模式 - 所有请求使用同一个发送器
        if mode == "default":
            return routing["default_sender"]
        
        # 2. 映射模式 - 根据解析器映射到特定发送器
        elif mode == "mapping":
            for mapping in routing["mapping"]:
                if mapping["parser"] == parser_name:
                    return mapping["sender"]
            # 未找到映射时使用默认发送器
            return routing["default_sender"]
        
        # 3. 自定义模式 - 预留接口
        elif mode == "custom":
            # 这里可以实现更复杂的路由逻辑
            # 目前使用默认发送器作为占位符
            logger.warning("⚠️ 自定义路由模式尚未实现")
            return routing["default_sender"]
        
        # 未知模式使用默认发送器
        logger.error(f"❓ 未知路由模式: {mode}")
        return routing["default_sender"]
    
    async def close(self):
        """关闭所有插件，释放资源"""
        proj_trace("app/core/schedule.py", "Dispatcher.close")
        logger.info("🛑 开始关闭插件...")
        
        # 关闭发送器插件
        for sender_name, sender in self.senders.items():
            try:
                if hasattr(sender, "close"):
                    await sender.close()
                    logger.info(f"🔌 已关闭发送器: {sender_name}")
            except Exception as e:
                logger.error(f"❌ 关闭发送器失败 {sender_name}: {str(e)}")
        
        logger.info("✅ 所有插件已关闭")