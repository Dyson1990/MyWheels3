#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:08:30 2021

@author: wolf
"""
import random
import math
import time

import pygame
from PIL import Image

bg_path = "./images/toronto.jpg"
bg_img = Image.open(bg_path)
SCREEN_RECT = pygame.Rect(0, 0, bg_img.width/1.5, bg_img.height) # 定义屏幕大小常量
FPS = 60 # 定义刷新率常量
CREATE_ENEMY_EVENT = pygame.USEREVENT # 创建生成敌人的事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1 # 英雄发射子弹事件

class GameSprite(pygame.sprite.Sprite):
    """
    fans的游戏精灵
    """
    
    def __init__(self, image_name, movement_x=0, movement_y=0):
        
        # 调用父类的初始化方法
        super().__init__()
        
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
    
    def update(self):
        
        self.rect.y = self.rect.y + self.movement_y
        self.rect.x = self.rect.x + self.movement_x
        
class Background(GameSprite):
    """游戏背景精灵"""
    
    def __init__(self):
        
        global bg_path, bg_img
        
        # 1.调用父类方法，实现精灵创建(image/rect/speed)
        super().__init__(bg_path)
        
        # 将图片居中
        self.rect.centerx = bg_img.width/3
        self.rect.y = 0
    
    def update(self):
        
        # 1.调用父类的方法实现
        super().update()
        
#        # 2.判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
#        if self.rect.y >= SCREEN_RECT.height:
#            self.rect.y = -self.rect.height
            
class Girl(GameSprite):
    """女孩精灵"""
    
    def __init__(self):
        
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/T.jpeg")
 
        # 指定女孩的初始位置
        global bg_img
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.top = 20
        self.direction_x = 1
        self.direction_y = 1
        
    def update(self):
        
        movement = random.randint(0, 360)
        self.rect.y = self.rect.y + self.direction_y * movement * 0.02
        self.rect.x = self.rect.x + self.direction_x * 6 * abs(math.sin(movement))
        
        if self.rect.top <= 0:
            self.direction_y = 1
            
        if self.rect.bottom >= self.rect.height * 2:
            self.direction_y = -1
            
        if self.rect.left <= 0:
            self.direction_x = 1
            
        if self.rect.right >= SCREEN_RECT.right:
            self.direction_x = -1
#        time.sleep(1)
            
#    def __del__(self):
#        print("敌机销毁", self.rect.x)
    
class Joker(GameSprite):
    """Joker精灵"""
    
    def __init__(self):
        
        # 1.调用父类方法，设置image/rect/speed
        super().__init__("./images/joker.png")
        
        # 2.设置joker初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 80
        
        self.roses = pygame.sprite.Group()
        self.signs = pygame.sprite.Group()
        
    def update(self):
        
        super().update()
        
        # 控制英雄不能离开屏幕
        if self.rect.left <= 0:
            self.rect.left = 0        
        elif self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
            
    def throw(self):
        rose = Rose()
        rose.rect.bottom = self.rect.y - 20
        rose.rect.centerx = self.rect.centerx
        self.roses.add(rose)
        
    def win(self):
        sign = WinSign()
        sign.rect.centerx = SCREEN_RECT.centerx
        sign.rect.centery = SCREEN_RECT.centery
        self.rect.bottom = SCREEN_RECT.bottom
        self.signs.add(sign)

class Rose(GameSprite):
    """rose精灵"""
    
    def __init__(self):
        
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/rose.png")
        self.movement_y = -6
    
    def update(self):
        
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        
        # 判断子弹是否飞出屏幕
        if self.rect.top < 0:
            self.kill()
#    
#    def __del__(self):
#        print("子弹销毁")

class WinSign(GameSprite):
    """winsign精灵"""
    
    def __init__(self):
        
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/win_sign.png")
