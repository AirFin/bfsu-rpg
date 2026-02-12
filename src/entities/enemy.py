# -*- coding: utf-8 -*-
"""
敌人类
"""

import pyxel
from config import TILE_SIZE, COLOR_RED


class Enemy:
    """敌人类"""
    
    def __init__(self, x, y, name="Slime", hp=30, attack=5):
        """初始化敌人"""
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.alive = True
        
    def update(self):
        """更新敌人状态"""
        if self.hp <= 0:
            self.alive = False
            
    def draw(self):
        """绘制敌人"""
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, COLOR_RED)
            
    def take_damage(self, amount):
        """受到伤害"""
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
        return not self.alive
        
    def do_attack(self):
        """执行攻击"""
        return self.attack
