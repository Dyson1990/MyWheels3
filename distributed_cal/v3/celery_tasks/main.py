#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:03:59 2021

@author: wolf
"""

from celery import Celery
# 生成celery应用
celery_app = Celery("caicai")
# 加载配置文件
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.email']) # 注意：传递的参数是任务列表