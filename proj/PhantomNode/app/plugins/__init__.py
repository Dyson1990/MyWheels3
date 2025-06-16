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

from utils.proj_trace import proj_trace
proj_trace("app/plugins/__init__.py", "module_imported")

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