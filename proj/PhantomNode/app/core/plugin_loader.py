# -*- coding: utf-8 -*-
# app/core/plugin_loader.py
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
from utils.proj_trace import proj_trace

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
    proj_trace("app/core/plugin_loader.py", "load_parser_plugin", plugin_file=plugin_file)
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
    proj_trace("app/core/plugin_loader.py", "load_sender_plugin", plugin_file=plugin_file)
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