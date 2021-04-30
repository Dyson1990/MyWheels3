#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:48:42 2021

@author: wolf
"""

import time

import pygame

from plane_sprites import *


class PlaneGame:
    """
    飞机大战主游戏
    """
    
    def __init__(self):
        print("游戏初始化")
        
        pygame.init()
        
        # 1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵族
        self.__create_sprites()
        # 4.设置定时事件（创建敌机）
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
    
    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(is_alt=True)
#        bg2.rect.y = -bg2.rect.height
        self.back_group = pygame.sprite.Group(bg1, bg2)
        
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        
        # 创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        
    def start_game(self):
        print("游戏开始")
#        time.sleep(5)
        
        while True:
            # 1.设置事件刷新帧率
            self.clock.tick(FPS)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵和精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()
            
    def __event_handler(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
                
            if event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵
                enemy0 = Enemy()
                
                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy0)
                
            if event.type == HERO_FIRE_EVENT:
                self.hero.fire()
                
        key_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键的索引值是不是1
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0
    
    def __check_collide(self):
        
        # 1.子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets
                                   , self.enemy_group
                                   , True
                                   , True)
        
        # 2.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero
                                              , self.enemy_group
                                              , True)
        
        # 判断列表是否有内容
        if len(enemies) > 0:
            
            # 让英雄牺牲
            self.hero.kill()
            # 结束游戏
            PlaneGame.__game_over()
    
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
    
    @staticmethod
    def __game_over():
        print("游戏结束")
        
        pygame.quit()
        exit()
        
if __name__ == "__main__":
    game = PlaneGame()
    game.start_game()