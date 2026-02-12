# -*- coding: utf-8 -*-
"""
HUD 模块
游戏内界面显示
"""

import pyxel
from config import COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_BLACK
from src.utils.font_manager import draw_text


class HUD:
    """游戏内 HUD"""
    
    def __init__(self):
        """初始化 HUD"""
        self.visible = True
        
    def draw(self, player):
        """绘制 HUD"""
        if not self.visible:
            return
            
        # HP 条
        self._draw_hp_bar(4, 4, 60, 8, player.hp, player.max_hp)
        
        # 玩家坐标（调试用）
        draw_text(4, 16, f"X:{int(player.x)} Y:{int(player.y)}", COLOR_WHITE)
        
    def _draw_hp_bar(self, x, y, width, height, current, maximum):
        """绘制生命条"""
        # 背景
        pyxel.rect(x, y, width, height, COLOR_BLACK)
        
        # 当前生命值
        hp_width = int((current / maximum) * (width - 2))
        color = COLOR_GREEN if current > maximum * 0.3 else COLOR_RED
        pyxel.rect(x + 1, y + 1, hp_width, height - 2, color)
        
        # 边框
        pyxel.rectb(x, y, width, height, COLOR_WHITE)
        
        # 数值
        draw_text(x + width + 4, y + 1, f"{current}/{maximum}", COLOR_WHITE)
        
    def toggle(self):
        """切换 HUD 显示"""
        self.visible = not self.visible
