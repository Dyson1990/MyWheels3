# PhantomNode - 协议转换代理服务器

![PhantomNode Logo](https://via.placeholder.com/150?text=PN)

> 基于FastAPI的灵活协议转换代理服务器，支持任意协议转换

## 项目概述

PhantomNode 是一个高度灵活的代理服务器，灵感来源于DataX的插件架构。它的核心功能是：
- 接收任意协议的请求
- 转换为统一格式
- 转发到任意协议的目标服务

## 核心特性

- **插件化架构**：支持热插拔的解析器和发送器插件
- **协议转换**：实现HTTP、SOCKS等协议间的相互转换
- **请求追踪**：每个请求生成唯一ID，便于日志追踪
- **路由策略**：支持多种路由模式（默认/映射/自定义）
- **赛博日志**：增强的日志记录系统，支持请求追踪
- **Windows兼容**：全面支持Windows平台

## 快速开始

### 安装依赖
```bash
pip install fastapi uvicorn httpx pyyaml python-socks