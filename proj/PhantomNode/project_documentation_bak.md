# Project Code Documentation

## File: `app\main.py`
```python
# app\main.py
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

# 将当前目录添加到系统路径，确保模块导入正确
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 导入FastAPI和相关模块
from fastapi import FastAPI
from core.schedule import Dispatcher
from core.config_mgr import config_manager
from core.cyber_logger import logger

# 导入uvicorn用于启动服务器
import uvicorn

# Windows兼容性设置
if sys.platform == "win32":
    # 设置Windows兼容的事件循环策略
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Windows上的信号处理替代方案
    try:
        import win32api
        def handle_win_signal(sig):
            """处理Windows信号"""
            logger.warning(f"🛑 接收到信号 {sig}，开始关闭应用...")
            loop = asyncio.get_event_loop()
            loop.create_task(shutdown())
            loop.stop()
    except ImportError:
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
    global dispatcher
    if dispatcher:
        logger.info("🛑 开始关闭应用...")
        await dispatcher.close()
        logger.info("✅ 应用已关闭")

@app.on_event("startup")
async def app_startup():
    """FastAPI启动事件处理函数"""
    await startup()

@app.on_event("shutdown")
async def app_shutdown():
    """FastAPI关闭事件处理函数"""
    await shutdown()

def handle_signal(signum, frame):
    """处理Unix信号 (SIGINT, SIGTERM)"""
    logger.warning(f"🛑 接收到信号 {signum}，开始关闭应用...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())
    loop.stop()

if __name__ == "__main__":
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
```

## File: `app\__init__.py`
```python
# app\__init__.py
# -*- coding: utf-8 -*-
# app/__init__.py
"""
应用包初始化文件
定义应用包的结构和公共接口

功能说明:
1. 标记app为Python包
2. 定义包级别的公共变量
3. 提供快捷导入路径
4. 打印启动信息

设计原则:
- 保持简洁，仅包含必要的初始化代码
- 避免在__init__中执行复杂逻辑
- 提供包级别的元数据

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

# 包版本信息
__version__ = "1.0.0"
__author__ = "Dyson1990"
__license__ = "MIT"
__description__ = "PhantomNode - 协议转换代理服务器"

# 公共导入快捷方式
from .core import config_manager, logger  # noqa
from .utils import generate_request_id  # noqa

# 打印启动信息
if __name__ == "__main__":
    print(f"""
    ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝
    ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔██╗ ██║█████╗  
    ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╗██║██╔══╝  
    ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚████║███████╗
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    
    PhantomNode v{__version__} - 协议转换代理服务器
    Author: {__author__}
    License: {__license__}
    """)
```

## File: `app\core\base.py`
```python
# app\core\base.py
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
        return f"[{self.request_id}] {self.method} {self.url}"
    
    def to_dict(self):
        """将请求对象转换为字典（用于日志记录）"""
        return {
            "request_id": self.request_id,
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "body_size": len(self.body) if self.body else 0,
            "params": self.params,
            "cookies": self.cookies
        }
```

## File: `app\core\config_mgr.py`
```python
# app\core\config_mgr.py
# -*- coding: utf-8 -*-
# app/core/config_mgr.py
"""
配置管理器
负责加载、解析和管理应用的配置信息

功能说明:
1. 从YAML配置文件中加载配置
2. 提供配置信息的访问接口
3. 处理插件失败策略
4. 管理路由配置

依赖模块:
- PyYAML: YAML配置文件解析

设计特点:
- 单例模式确保全局唯一配置实例
- 自动处理配置文件路径问题
- 提供安全的配置访问方法

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import yaml
from pathlib import Path
from core.cyber_logger import logger

class ConfigManager:
    """配置管理器，单例模式实现"""
    
    # 单例实例
    _instance = None
    
    def __new__(cls):
        """确保单例模式"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # 初始化配置为空字典
            cls._instance.config = {}
        return cls._instance
    
    def load_config(self, config_path: str):
        """
        加载YAML配置文件
        
        参数:
            config_path: 配置文件路径
            
        异常:
            FileNotFoundError: 如果配置文件不存在
            yaml.YAMLError: 如果配置文件格式错误
        """
        # 获取绝对路径
        abs_path = Path(config_path).resolve()
        
        # 检查文件是否存在
        if not abs_path.exists():
            # 尝试在当前目录查找
            current_dir_path = Path.cwd() / config_path
            if current_dir_path.exists():
                abs_path = current_dir_path
            else:
                error_msg = f"配置文件不存在: {abs_path} 或 {current_dir_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
        
        try:
            # 读取并解析YAML文件
            with open(abs_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            logger.info(f"✅ 配置文件加载成功: {abs_path}")
            logger.debug(f"配置内容: {self.config}")
        except yaml.YAMLError as e:
            error_msg = f"配置文件解析错误: {str(e)}"
            logger.error(error_msg)
            raise yaml.YAMLError(error_msg)
        except Exception as e:
            error_msg = f"加载配置文件时发生未知错误: {str(e)}"
            logger.error(error_msg)
            raise
    
    def should_terminate_on_plugin_fail(self) -> bool:
        """
        检查插件失败时是否应终止应用
        
        返回:
            True: 如果配置为插件失败时终止应用
            False: 如果配置为隔离插件
        """
        policy = self.config.get("plugin_fail_policy", "isolate")
        return policy.lower() == "terminate"
    
    @property
    def log_level(self) -> str:
        """获取日志级别配置"""
        return self.config.get("log_level", "INFO").upper()
    
    @property
    def routing_config(self) -> dict:
        """获取路由配置"""
        return self.config.get("routing", {})
    
    @property
    def server_config(self) -> dict:
        """获取服务器配置"""
        return self.config.get("server", {})

# 全局配置管理器实例
config_manager = ConfigManager()
```

## File: `app\core\cyber_logger.py`
```python
# app\core\cyber_logger.py
# app\core\cyber_logger.py
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
```

## File: `app\core\plugin_loader.py`
```python
# app\core\plugin_loader.py
# -*- coding: utf-8 -*-
# app/utils/plugin_loader.py
"""
插件加载器
负责动态加载解析器和发送器插件

功能说明:
1. 根据插件文件名动态导入插件模块
2. 实例化插件类
3. 处理插件加载过程中的异常
4. 支持解析器和发送器插件的加载

设计特点:
- 约定优于配置：插件类名与文件名相同（首字母大写）
- 错误处理：提供明确的错误信息
- 日志记录：详细记录插件加载过程
- 异常处理：捕获并记录导入错误

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import importlib
import sys
from pathlib import Path
from core.cyber_logger import logger

def load_parser_plugin(plugin_file: str):
    """
    加载解析器插件
    
    参数:
        plugin_file: 插件文件名（不含.py扩展名），如 "http"
        
    返回:
        解析器插件实例
        
    异常:
        ImportError: 如果无法加载插件或找到插件类
    """
    try:
        # 动态导入解析器模块
        module_path = f"plugins.parser.{plugin_file}"
        logger.debug(f"🔍 尝试导入解析器模块: {module_path}")
        
        # 导入模块
        module = importlib.import_module(module_path)
        
        # 插件类名应为文件名首字母大写（去下划线）
        class_name = plugin_file.title().replace('_', '')
        logger.debug(f"查找解析器类: {class_name}")
        
        # 获取插件类
        plugin_class = getattr(module, class_name, None)
        
        # 如果找不到，尝试其他可能的类名
        if not plugin_class:
            logger.warning(f"⚠️ 找不到标准类 {class_name}，尝试备用查找")
            for attr_name in dir(module):
                if attr_name.lower() == plugin_file.lower():
                    plugin_class = getattr(module, attr_name)
                    logger.info(f"使用备用类名: {attr_name}")
                    break
        
        # 如果仍然找不到，抛出异常
        if not plugin_class:
            error_msg = f"在模块 {module_path} 中找不到解析器类"
            logger.error(error_msg)
            raise ImportError(error_msg)
        
        # 实例化插件
        instance = plugin_class()
        logger.info(f"🆕 创建解析器实例: {class_name}")
        return instance
    
    except ImportError as e:
        error_msg = f"导入解析器插件失败 {plugin_file}: {str(e)}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"初始化解析器插件失败 {plugin_file}: {str(e)}"
        logger.error(error_msg)
        raise

def load_sender_plugin(plugin_file: str):
    """
    加载发送器插件
    
    参数:
        plugin_file: 插件文件名（不含.py扩展名），如 "http"
        
    返回:
        发送器插件实例
        
    异常:
        ImportError: 如果无法加载插件或找到插件类
    """
    try:
        # 动态导入发送器模块
        module_path = f"plugins.sender.{plugin_file}"
        logger.debug(f"🔍 尝试导入发送器模块: {module_path}")
        
        # 导入模块
        module = importlib.import_module(module_path)
        
        # 插件类名应为文件名首字母大写（去下划线）
        class_name = plugin_file.title().replace('_', '')
        logger.debug(f"查找发送器类: {class_name}")
        
        # 获取插件类
        plugin_class = getattr(module, class_name, None)
        
        # 如果找不到，尝试其他可能的类名
        if not plugin_class:
            logger.warning(f"⚠️ 找不到标准类 {class_name}，尝试备用查找")
            for attr_name in dir(module):
                if attr_name.lower() == plugin_file.lower():
                    plugin_class = getattr(module, attr_name)
                    logger.info(f"使用备用类名: {attr_name}")
                    break
        
        # 如果仍然找不到，抛出异常
        if not plugin_class:
            error_msg = f"在模块 {module_path} 中找不到发送器类"
            logger.error(error_msg)
            raise ImportError(error_msg)
        
        # 实例化插件
        instance = plugin_class()
        logger.info(f"🆕 创建发送器实例: {class_name}")
        return instance
    
    except ImportError as e:
        error_msg = f"导入发送器插件失败 {plugin_file}: {str(e)}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"初始化发送器插件失败 {plugin_file}: {str(e)}"
        logger.error(error_msg)
        raise
```

## File: `app\core\schedule.py`
```python
# app\core\schedule.py
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

class Dispatcher:
    """核心调度器，管理请求处理流程"""
    
    def __init__(self, app):
        """
        初始化调度器
        
        参数:
            app: FastAPI应用实例
        """
        self.app = app
        
        # 存储加载的解析器插件 {插件文件名: 插件实例}
        self.parsers = {}
        
        # 存储加载的发送器插件 {插件文件名: 插件实例}
        self.senders = {}
        
        # 请求计数器
        self.request_count = 0
    
    def load_plugins(self):
        """加载所有插件 - 从路由配置中自动发现需要的插件"""
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
        
        async def handler(raw_request):
            """
            实际处理请求的函数
            1. 生成唯一请求ID
            2. 解析请求
            3. 路由到发送器
            4. 发送请求并返回响应
            """
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
```

## File: `app\core\__init__.py`
```python
# app\core\__init__.py
# -*- coding: utf-8 -*-


```

## File: `app\plugins\__init__.py`
```python
# app\plugins\__init__.py
# -*- coding: utf-8 -*-
# app/plugins/__init__.py
"""
插件包初始化文件
定义插件包的结构和公共接口

功能说明:
1. 标记plugins为Python包
2. 提供插件开发的公共工具和接口
3. 简化插件导入路径
4. 提供插件开发文档

设计原则:
- 保持轻量，避免复杂逻辑
- 提供插件开发文档的入口点
- 定义插件类型常量

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

# 插件类型常量
PARSER = "parser"  # 解析器插件类型
SENDER = "sender"  # 发送器插件类型

# 公共导入快捷方式
from .parser import http as http_parser  # noqa
from .parser import socks as socks_parser  # noqa
from .sender import http as http_sender  # noqa

# 插件开发文档
__doc__ = """
=== PhantomNode 插件开发指南 ===

1. 插件位置:
   - 解析器插件: app/plugins/parser/
   - 发送器插件: app/plugins/sender/

2. 命名规范:
   - 文件名: 小写字母，使用下划线分隔 (如: http.py)
   - 类名: 文件名首字母大写 (如: class Http)

3. 必须实现的方法:
   - 解析器:
     - parse_request(raw_request) -> BaseRequest
     - register_routes(app, handler)
   
   - 发送器:
     - send_request(request: BaseRequest) -> Response
     - close() [可选，用于资源清理]

4. 配置管理:
   - 所有配置参数直接在类中定义 DEFAULT_CONFIG
   - 配置在__init__方法中初始化

5. 日志记录:
   - 使用 from core.cyber_logger import logger
   - 记录关键操作和错误

6. 错误处理:
   - 抛出明确的异常
   - 使用logger记录错误详情

7. 依赖管理:
   - 在插件文件顶部声明依赖
   - 在README中提供安装说明

更多信息参考项目文档: https://github.com/Dyson1990/PhantomNode
"""
```

## File: `app\plugins\parser\http.py`
```python
# app\plugins\parser\http.py
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
            "OPTIONS"
        ]
    }
    
    def __init__(self):
        """初始化解析器，使用默认配置"""
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
            return await handler(request)
        
        logger.info(f"🔗 注册HTTP路由: /{{path:path}} (方法: {methods})")
```

## File: `app\plugins\parser\socks.py`
```python
# app\plugins\parser\socks.py
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
        # 注意: SOCKS协议需要独立TCP服务器
        logger.info("🔌 SOCKS协议需要独立TCP服务器，将在startup事件中初始化")
        
        # 在应用启动时创建SOCKS服务器
        @app.on_event("startup")
        async def start_socks_server():
            """启动SOCKS服务器"""
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
            
            # TODO: 调用处理函数
            # response = await handler(base_request)
            
            # 发送成功响应
            writer.write(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            await writer.drain()
            
        except Exception as e:
            logger.error(f"❌ SOCKS连接处理失败: {str(e)}")
            # 发送错误响应
            writer.write(b"\x05\x01\x00\x01\x00\x00\x00\x00\x00\x00")
            await writer.drain()
        finally:
            # 关闭连接
            writer.close()
            await writer.wait_closed()
    
    async def _handle_socks5_handshake(self, reader, writer):
        """处理SOCKS5握手和认证"""
        # 读取客户端支持的认证方法
        data = await reader.read(2)
        if not data or len(data) < 2:
            raise ConnectionError("Invalid SOCKS5 handshake")
        
        # 检查版本
        if data[0] != 0x05:
            raise ValueError("Invalid SOCKS version")
        
        # 读取认证方法
        nmethods = data[1]
        methods = await reader.read(nmethods)
        
        # 检查认证要求
        auth_required = self.config["auth_required"]
        if auth_required:
            # 要求用户名/密码认证
            if 0x02 not in methods:
                raise ValueError("Username/Password auth not supported by client")
            
            # 发送认证方法选择
            writer.write(b"\x05\x02")
            await writer.drain()
            
            # 处理认证
            await self._handle_socks5_auth(reader, writer)
        else:
            # 无认证
            if 0x00 not in methods:
                raise ValueError("No acceptable auth methods")
            
            # 发送无认证选择
            writer.write(b"\x05\x00")
            await writer.drain()
    
    async def _handle_socks5_auth(self, reader, writer):
        """处理SOCKS5用户名/密码认证"""
        # 读取认证请求
        data = await reader.read(2)
        if not data or data[0] != 0x01:
            raise ValueError("Invalid auth request")
        
        # 读取用户名
        ulen = data[1]
        username = (await reader.read(ulen)).decode('utf-8')
        
        # 读取密码
        plen_data = await reader.read(1)
        plen = plen_data[0]
        password = (await reader.read(plen)).decode('utf-8')
        
        # 验证凭据
        valid_password = self.config["users"].get(username)
        if valid_password is None or valid_password != password:
            # 认证失败
            writer.write(b"\x01\x01")
            await writer.drain()
            raise PermissionError("Authentication failed")
        
        # 认证成功
        writer.write(b"\x01\x00")
        await writer.drain()
    
    async def _handle_socks4_handshake(self, reader, writer):
        """处理SOCKS4握手"""
        # 读取请求
        data = await reader.read(9)
        if not data or len(data) < 9:
            raise ConnectionError("Invalid SOCKS4 request")
        
        # 检查版本
        if data[0] != 0x04:
            raise ValueError("Invalid SOCKS version")
        
        # 检查命令
        command = data[1]
        if command not in (0x01, 0x02):  # CONNECT or BIND
            raise ValueError("Unsupported command")
        
        # 跳过端口和IP
        user_end = data.index(b'\x00', 8)
        if user_end == -1:
            raise ValueError("Invalid user field")
        
        # 读取用户名
        username = data[8:user_end].decode('utf-8')
        
        # 验证用户
        if self.config["auth_required"]:
            if username not in self.config["users"]:
                # 认证失败
                writer.write(b"\x00\x5D\x00\x00\x00\x00\x00\x00")
                await writer.drain()
                raise PermissionError("Authentication failed")
        
        # 发送成功响应
        writer.write(b"\x00\x5A\x00\x00\x00\x00\x00\x00")
        await writer.drain()
```

## File: `app\plugins\parser\__init__.py`
```python
# app\plugins\parser\__init__.py
# -*- coding: utf-8 -*-


```

## File: `app\plugins\sender\http.py`
```python
# app\plugins\sender\http.py
# -*- coding: utf-8 -*-
# app/plugins/sender/http.py
"""
HTTP 协议发送器插件
负责将请求转发到目标HTTP服务器

功能说明:
1. 发送HTTP请求到目标服务器
2. 处理重试逻辑
3. 管理连接池
4. 支持HTTPS和证书验证
5. 支持HTTP/2
6. 代理配置支持

依赖模块:
- httpx: 异步HTTP客户端
- core.base: 基础请求模型
- core.cyber_logger: 日志记录

设计特点:
- 默认配置参数内置
- 智能重试机制
- 连接池管理
- 完整的错误处理

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import httpx
import asyncio
from core.base import BaseRequest
from core.cyber_logger import logger

class Http:
    """HTTP发送器插件"""
    
    # 默认配置参数
    DEFAULT_CONFIG = {
        "base_url": "http://example.com",  # 目标基础URL
        "timeout": 30.0,                  # 请求超时时间（秒）
        "retry_times": 3,                 # 失败重试次数
        "retry_delay": 0.5,               # 重试延迟（秒）
        "verify_ssl": True,               # SSL证书验证
        "http2": False,                   # 是否启用HTTP/2
        "proxy": None,                    # 代理服务器设置
        "headers": {                      # 默认请求头
            "User-Agent": "PhantomNode-HTTP-Sender/1.0",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
    }
    
    def __init__(self):
        """初始化发送器，使用默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.client = self._create_client()
        logger.info(f"🆕 HTTP发送器初始化完成，配置: {self.config}")
    
    def _create_client(self):
        """创建HTTP客户端实例"""
        return httpx.AsyncClient(
            base_url=self.config["base_url"],
            timeout=self.config["timeout"],
            verify=self.config["verify_ssl"],
            http2=self.config["http2"],
            proxies=self.config["proxy"],
            headers=self.config["headers"]
        )
    
    async def send_request(self, request: BaseRequest):
        """
        发送统一格式的HTTP请求
        
        参数:
            request: BaseRequest统一格式的请求对象
            
        返回:
            httpx.Response: HTTP响应对象
            
        异常:
            httpx.RequestError: 如果所有重试均失败
        """
        logger.info(f"🚀 发送HTTP请求: {request.method} {request.url}")
        
        # 准备请求参数
        request_args = {
            "method": request.method,
            "url": request.url,
            "headers": request.headers,
            "params": request.params,
            "cookies": request.cookies,
            "content": request.body
        }
        
        # 执行请求（带重试逻辑）
        for attempt in range(1, self.config["retry_times"] + 2):
            try:
                # 发送请求
                response = await self.client.request(**request_args)
                
                # 记录响应信息
                logger.debug(
                    f"📥 收到响应: {request.request_id} | "
                    f"状态: {response.status_code} | "
                    f"大小: {len(response.content)}字节"
                )
                
                return response
            
            except (httpx.ConnectError, httpx.ReadTimeout) as e:
                # 连接错误或超时，进行重试
                if attempt <= self.config["retry_times"]:
                    delay = self.config["retry_delay"] * attempt
                    logger.warning(
                        f"🔄 请求失败 ({e.__class__.__name__})，"
                        f"{attempt}/{self.config['retry_times']} 重试中... "
                        f"等待 {delay}秒"
                    )
                    await asyncio.sleep(delay)
                else:
                    # 重试次数用尽，抛出异常
                    error_msg = f"🚨 请求失败，超过最大重试次数: {str(e)}"
                    logger.error(error_msg)
                    raise
            
            except httpx.HTTPStatusError as e:
                # HTTP状态错误（4xx, 5xx），不重试
                error_msg = f"🚨 HTTP错误: {e.response.status_code} {str(e)}"
                logger.error(error_msg)
                return e.response
            
            except Exception as e:
                # 其他异常直接抛出
                error_msg = f"🚨 请求失败: {str(e)}"
                logger.error(error_msg)
                raise
    
    async def close(self):
        """关闭HTTP客户端连接，释放资源"""
        if hasattr(self, "client") and self.client:
            try:
                await self.client.aclose()
                logger.info("🔌 HTTP客户端连接已关闭")
            except Exception as e:
                logger.error(f"❌ 关闭HTTP客户端失败: {str(e)}")
```

## File: `app\plugins\sender\__init__.py`
```python
# app\plugins\sender\__init__.py
# -*- coding: utf-8 -*-


```

## File: `app\utils\request_id.py`
```python
# app\utils\request_id.py
# -*- coding: utf-8 -*-
# app/utils/request_id.py
"""
请求ID生成器
生成唯一的请求标识符，用于日志追踪

功能说明:
1. 生成格式为 YYYYMMDDHHMMSSsss_xxxx 的唯一ID
2. 每日自动重置计数器
3. 毫秒级时间戳保证同一时刻的请求可区分
4. 线程安全设计（适用于单线程异步环境）

设计特点:
- 使用全局变量管理计数器和日期
- 毫秒精度时间戳（13位）
- 每日计数器自动重置
- 高效无锁设计

作者: Dyson1990 (GitHub: https://github.com/Dyson1990)
创建时间: 2025-06-15 17:20:00
"""

import time
from datetime import datetime

# 全局计数器（每日重置）
_request_counter = 0

# 当前日期 (YYYYMMDD格式)
_current_date = datetime.now().strftime("%Y%m%d")

def generate_request_id() -> str:
    """
    生成唯一请求ID  
    格式: YYYYMMDDHHMMSSsss_xxxx  
    
    其中:  
    - YYYYMMDD: 日期  
    - HHMMSS: 时分秒  
    - sss: 毫秒  
    - xxxx: 每日自增序号 (4位数字)  
    
    返回:
        唯一请求ID字符串
    """
    global _request_counter, _current_date
    
    # 获取当前时间
    now = datetime.now()
    
    # 检查日期是否变更
    today = now.strftime("%Y%m%d")
    if today != _current_date:
        _current_date = today
        _request_counter = 0
        # 记录日期变更
        print(f"🔄 日期变更: {_current_date}, 计数器已重置")
    
    # 增加计数器
    _request_counter += 1
    
    # 生成时间戳部分 (YYYYMMDDHHMMSSsss)
    timestamp = now.strftime("%Y%m%d%H%M%S%f")[:-3]  # 保留到毫秒
    
    # 格式化计数器部分 (xxxx)
    counter_str = f"{_request_counter:04d}"
    
    # 组合成完整ID
    request_id = f"{timestamp}_{counter_str}"
    
    return request_id

# 测试函数
if __name__ == "__main__":
    # 生成10个测试ID
    for i in range(10):
        print(f"测试ID {i+1}: {generate_request_id()}")
        time.sleep(0.01)  # 确保时间戳不同
```

## File: `app\utils\__init__.py`
```python
# app\utils\__init__.py
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
```


```
import os
import pathlib

def project_to_markdown(project_dir, output_md="project_documentation.md"):
    """
    将整个Python项目代码合并到一个Markdown文件中，按文件分代码块

    Args:
        project_dir (str): 项目根目录路径
        output_md (str): 输出的Markdown文件名
    """
    markdown_content = ["# Project Code Documentation\n"]

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = pathlib.Path(root) / file
                rel_path = str(filepath.relative_to(project_dir))

                # 添加文件标题
                markdown_content.append(f"\n## File: `{rel_path}`\n")

                # 添加代码块
                markdown_content.append(f"```python\n# {rel_path}\n")
                with open(filepath, 'r', encoding='utf-8') as f:
                    markdown_content.append(f.read())
                markdown_content.append("\n```\n")

    # 写入Markdown文件
    with open(output_md, 'w', encoding='utf-8') as md_file:
        md_file.write("".join(markdown_content))

    print(f"Generated: {output_md}")
    

project_to_markdown(r"C:/Users/Dyson/Documents/MyWheels3/proj/PhantomNode")
```