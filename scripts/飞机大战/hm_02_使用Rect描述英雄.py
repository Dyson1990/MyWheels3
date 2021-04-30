#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:58:35 2021

@author: wolf
"""

import pygame

hero_rect = pygame.Rect(100, 500, 120, 125)

print("英雄原点", hero_rect.x, hero_rect.y)
print("英雄尺寸", hero_rect.width, hero_rect.height)

print(hero_rect.size)