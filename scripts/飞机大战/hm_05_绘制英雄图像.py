#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 11:06:59 2021

@author: wolf
"""

import pygame
import time

pygame.init()

# 创建游戏窗口
screen = pygame.display.set_mode((480, 700)) # 不传指定窗口大小时，默认全屏

# 绘制背景图像
# 1.加载图像数据
bg = pygame.image.load("./images/background.png")
# 2.blit绘制图像
screen.blit(bg, (0, 0))
# 3.update更新屏幕显示
pygame.display.update()

# 绘制英雄的飞机
hero = pygame.image.load("./images/me1.png")
screen.blit(hero, (200, 300))
pygame.display.update()


time.sleep(5)

pygame.quit()