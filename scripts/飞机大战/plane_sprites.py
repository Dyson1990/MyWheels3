#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:08:30 2021

@author: wolf
"""
import random

import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700) # 定义屏幕大小常亮
FPS = 60 # 定义刷新率常量
CREATE_ENEMY_EVENT = pygame.USEREVENT # 创建生成敌人的事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1 # 英雄发射子弹事件

class GameSprite(pygame.sprite.Sprite):
    """
    飞机大战的游戏精灵
    """
    
    def __init__(self, image_name, speed=1):
        
        # 调用父类的初始化方法
        super().__init__()
        
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
    
    def update(self):
        
        # 在屏幕的垂直方向上移动
        self.rect.y = self.rect.y + self.speed
        
class Background(GameSprite):
    """游戏背景精灵"""
    
    def __init__(self, is_alt=False):
        
        # 1.调用父类方法，实现精灵创建(image/rect/speed)
        super().__init__("./images/background.png")
        # 2.判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height
    
    def update(self):
        
        # 1.调用父类的方法实现
        super().update()
        
        # 2.判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height
            
class Enemy(GameSprite):
    """敌机精灵"""
    
    def __init__(self):
        
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")
        # 2.指定敌机的初始速度
        self.speed = random.randint(1, 5)
        # 3.指定敌机的初始位置
        self.rect.x = random.randint(0, SCREEN_RECT.width-self.rect.width)
        self.rect.bottom = 0
        
    def update(self):
        
        # 1.调用父类方法，保持垂直方向飞行
        super().update()
        # 2.判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
#            print("飞出屏幕")
            
            # kill方法可以将精灵从所有精灵组中移出，精灵被自动销毁 
            self.kill()
            
#    def __del__(self):
#        print("敌机销毁", self.rect.x)
    
class Hero(GameSprite):
    """英雄精灵"""
    
    def __init__(self):
        
        # 1.调用父类方法，设置image/rect/speed
        super().__init__("./images/me1.png", 0)
        
        # 2.设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        
        # 3.创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        
    def update(self):
        
        # 英雄在水平方向上移动
        self.rect.x = self.rect.x + self.speed
        
        # 控制英雄不能离开屏幕
        if self.rect.left <= 0:
            self.rect.left = 0        
        elif self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
            
    def fire(self):
#        print("发射子弹")
        
        for i in range(3):
            # 1.创建子弹精灵
            bullet = Bullet()
            
            # 2.设置精灵位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet)
    
class Bullet(GameSprite):
    """子弹精灵"""
    
    def __init__(self):
        
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png", -2)
    
    def update(self):
        
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()
#    
#    def __del__(self):
#        print("子弹销毁")