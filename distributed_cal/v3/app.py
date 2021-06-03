#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:44:08 2021

@author: wolf
"""

from celery_tasks.email.tasks import cal1

while True:
    cal1.delay(1,2)
