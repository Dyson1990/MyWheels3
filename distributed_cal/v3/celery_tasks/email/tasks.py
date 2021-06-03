#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 16:33:53 2021

@author: wolf
"""

import time
from celery_tasks.main import celery_app

@celery_app.task(name='cal1')   # 添加celery_app.task这个装饰器，指定该任务的任务名name='seed_email'
def cal1(x, y):
  time.sleep(10)
  return x*y
