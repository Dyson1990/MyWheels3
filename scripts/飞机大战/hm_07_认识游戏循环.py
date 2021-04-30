#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 11:06:59 2021

@author: wolf
"""

import pygame
import time

# 游戏初始化
pygame.init()

# 创建游戏窗口
screen = pygame.display.set_mode((480, 700)) # 不传指定窗口大小时，默认全屏

# 绘制背景图像
bg = pygame.image.load("./images/background.png")
screen.blit(bg, (0, 0))

# 绘制英雄的飞机
hero = pygame.image.load("./images/me1.png")
screen.blit(hero, (200, 300))

# 完成所有绘制工作后，统一调用update方法
pygame.display.update()

# 创建时钟对象
clock = pygame.time.Clock()

# 游戏循环 -> 意味着游戏的开始
i = 0
while True:
    
    # 可以指定循环体内部代码执行的频率
    clock.tick(60)
    


pygame.quit()