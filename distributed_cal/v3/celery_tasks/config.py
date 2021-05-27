#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:04:53 2021

@author: wolf
"""

broker_url = 'redis://127.0.0.1:6379/1' # 使用Redis作为消息代理
 
result_backend = 'redis://127.0.0.1:6379/2' # 把任务结果存在了Redis
 
# task_serializer = 'msgpack' # 任务序列化和反序列化使用msgpack方案
 
result_serializer = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
 
result_expires = 60 * 60 * 24 # celery任务结果有效期
 
accept_content = ['json', 'msgpack'] # 指定接受的内容类型
 
timezone = 'Asia/Shanghai'       # celery使用的时区
CELERY_enable_utc = True            # 启动时区设置
CELERYD_LOG_FILE = "/var/log/celery/celery.log"   # celery日志存储位置