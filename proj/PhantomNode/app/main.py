# -*- coding: utf-8 -*-
# app/main.py
"""
PhantomNode 主入口文件
FastAPI应用启动入口，处理生命周期事件

功能说明:
1. 创建FastAPI应用实例
2. 初始化核心调度器
3. 处理应用启动和关闭事件
4. 实现Windows兼容的信号处理

依赖模块:
- fastapi: Web框架
- uvicorn: ASGI服务器
- core.schedule: 核心调度器
- core.config_mgr: 配置管理
- core.cyber_logger: 日志记录

Windows兼容性:
- 使用WindowsSelectorEventLoopPolicy确保Windows兼容性
- 实现win32api信号处理作为替代方案

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import sys
import os
import asyncio
import signal
from pathlib import Path
from utils.proj_trace import proj_trace

# 将当前目录添加到系统路径，确保模块导入正确
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 导入FastAPI和相关模块
from fastapi import FastAPI
from core.schedule import Dispatcher
from core.config_mgr import config_manager
from core.cyber_logger import logger, log_p

# 导入uvicorn用于启动服务器
import uvicorn

# Windows兼容性设置
if sys.platform == "win32":
    proj_trace("app/main.py", "__windows_compatibility_setup")
    # 设置Windows兼容的事件循环策略
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Windows上的信号处理替代方案
    try:
        import win32api
        def handle_win_signal(sig):
            """处理Windows信号"""
            proj_trace("app/main.py", "handle_win_signal", sig=sig)
            logger.warning(f"🛑 接收到信号 {sig}，开始关闭应用...")
            loop = asyncio.get_event_loop()
            loop.create_task(shutdown())
            loop.stop()
    except ImportError:
        proj_trace("app/main.py", "__win32api_import_error")
        logger.warning("⚠️ win32api未安装，Windows信号处理不可用")

# 创建FastAPI应用实例
app = FastAPI(
    title="PhantomNode 代理服务器",
    description="基于FastAPI的协议转换代理服务器",
    version="1.0.0"
)

# 全局调度器实例
dispatcher = None

async def startup():
    """应用启动逻辑"""
    proj_trace("app/main.py", "startup")
    global dispatcher
    
    logger.info("🚀 应用启动中...")
    
    # 加载配置文件
    config_path = "config.yaml"
    config_manager.load_config(config_path)
    logger.info(f"📋 配置文件已加载: {config_path}")
    
    # 初始化调度器
    dispatcher = Dispatcher(app)
    
    # 加载插件
    dispatcher.load_plugins()
    
    # 设置路由
    dispatcher.setup_routes()
    
    logger.info("✅ 应用启动完成")

async def shutdown():
    """应用关闭逻辑"""
    proj_trace("app/main.py", "shutdown")
    global dispatcher
    if dispatcher:
        logger.info("🛑 开始关闭应用...")
        await dispatcher.close()
        logger.info("✅ 应用已关闭")        

@app.on_event("startup")
async def app_startup():
    """FastAPI启动事件处理函数"""
    proj_trace("app/main.py", "app_startup")
    await startup()

@app.on_event("shutdown")
async def app_shutdown():
    """FastAPI关闭事件处理函数"""
    proj_trace("app/main.py", "app_shutdown")
    await shutdown()

def handle_signal(signum, frame):
    """处理Unix信号 (SIGINT, SIGTERM)"""
    proj_trace("app/main.py", "handle_signal", signum=signum, frame=frame)
    logger.warning(f"🛑 接收到信号 {signum}，开始关闭应用...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())
    loop.stop()

if __name__ == "__main__":
    proj_trace("app/main.py", "__main__")
    # 注册信号处理器 (Unix系统)
    if sys.platform != "win32":
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
    
    # Windows信号处理
    if sys.platform == "win32" and "win32api" in sys.modules:
        win32api.SetConsoleCtrlHandler(handle_win_signal, True)
    
    # 从配置获取服务器设置
    server_config = config_manager.config.get("server", {})
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 8000)
    
    # 启动服务
    logger.info(f"🌐 启动服务: http://{host}:{port}")
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_config=None  # 使用自定义日志配置
    )