#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:48:42 2021

@author: wolf
"""

import time

import pygame

from fans_sprites import *


class FansGame:
    """
    fans主游戏
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
#        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
#        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        
        self.win = False
    
    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)
        
        # 创建敌机精灵组
        self.girl = Girl()
        self.girl_group = pygame.sprite.Group(self.girl)
        
        # 创建英雄精灵和精灵组
        self.joker = Joker()
        self.joker_group = pygame.sprite.Group(self.joker)
        
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
                FansGame.__game_over()
                
# =============================================================================
#             if event.type == CREATE_ENEMY_EVENT:
#                 # 创建敌机精灵
#                 enemy0 = Enemy()
#                 
#                 # 将敌机精灵添加到敌机精灵组
#                 self.enemy_group.add(enemy0)
# =============================================================================
                
# =============================================================================
#             if event.type == HERO_FIRE_EVENT:
#                 self.joker.throw()
# =============================================================================
                
        key_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键的索引值是不是1
        if key_pressed[pygame.K_RIGHT]:
            self.joker.movement_x = 10
        elif key_pressed[pygame.K_LEFT]:
            self.joker.movement_x = -10
        else:
            self.joker.movement_x = 0
            
        if key_pressed[pygame.K_SPACE]:
            self.joker.throw()
            
    def __check_collide(self):
        event_collide = pygame.sprite.groupcollide(self.joker.roses
                                                   , self.girl_group
                                                   , True
                                                   , True)
        if event_collide:
            self.joker.win()
            self.__update_sprites()
            pygame.display.update()
            
            time.sleep(60)
            
            self.joker.kill()
            
            FansGame.__game_over()

# =============================================================================
#         # 1.子弹摧毁敌机
#         pygame.sprite.groupcollide(self.joker.bullets
#                                    , self.enemy_group
#                                    , True
#                                    , True)
#         
#         # 2.敌机撞毁英雄
#         enemies = pygame.sprite.spritecollide(self.joker
#                                               , self.enemy_group
#                                               , True)
#         
#         # 判断列表是否有内容
#         if len(enemies) > 0:
#             
#             # 让英雄牺牲
#             self.joker.kill()
#             # 结束游戏
#             FansGame.__game_over()
# =============================================================================
    
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        
#        self.enemy_group.update()
#        self.enemy_group.draw(self.screen)

        self.joker_group.update()
        self.joker_group.draw(self.screen)
      
        self.girl_group.update()
        self.girl_group.draw(self.screen)
        
        self.joker.roses.update()
        self.joker.roses.draw(self.screen)
        
        self.joker.signs.update()
        self.joker.signs.draw(self.screen)
    
    @staticmethod
    def __game_over():
        print("游戏结束")
        
        pygame.quit()
        exit()
        
if __name__ == "__main__":
    game = FansGame()
    game.start_game()