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
from utils.proj_trace import proj_trace


class ConfigManager:
    """配置管理器，单例模式实现"""
    
    # 单例实例
    _instance = None
    
    def __new__(cls):
        """确保单例模式"""
        proj_trace("app/core/config_mgr.py", "ConfigManager.__new__")
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
        proj_trace("app/core/config_mgr.py", "ConfigManager.load_config", config_path=config_path)
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
        proj_trace("app/core/config_mgr.py", "ConfigManager.should_terminate_on_plugin_fail")
        policy = self.config.get("plugin_fail_policy", "isolate")
        return policy.lower() == "terminate"
    
    @property
    def log_level(self) -> str:
        """获取日志级别配置"""
        proj_trace("app/core/config_mgr.py", "ConfigManager.log_level")
        return self.config.get("log_level", "INFO").upper()
    
    @property
    def routing_config(self) -> dict:
        """获取路由配置"""
        proj_trace("app/core/config_mgr.py", "ConfigManager.routing_config")
        return self.config.get("routing", {})
    
    @property
    def server_config(self) -> dict:
        """获取服务器配置"""
        proj_trace("app/core/config_mgr.py", "ConfigManager.server_config")
        return self.config.get("server", {})

# 全局配置管理器实例
config_manager = ConfigManager()