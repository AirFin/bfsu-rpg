# -*- coding: utf-8 -*-
"""
菜单模块
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW
from src.utils.font_manager import draw_text, text_width
from src.systems.input_handler import InputHandler


class Menu:
    """菜单类"""
    
    def __init__(self, options, title="菜单"):
        """
        初始化菜单
        options: 菜单选项列表
        """
        self.options = options
        self.title = title
        self.selected = 0
        self.active = False
        
    def open(self):
        """打开菜单"""
        self.active = True
        self.selected = 0
        
    def close(self):
        """关闭菜单"""
        self.active = False
        
    def update(self):
        """更新菜单"""
        if not self.active:
            return None
            
        # 上下选择
        if InputHandler.is_just_pressed(InputHandler.MOVE_UP):
            self.selected = (self.selected - 1) % len(self.options)
        elif InputHandler.is_just_pressed(InputHandler.MOVE_DOWN):
            self.selected = (self.selected + 1) % len(self.options)
            
        # 确认选择
        if InputHandler.is_just_pressed(InputHandler.CONFIRM):
            return self.options[self.selected]
            
        # 取消
        if InputHandler.is_just_pressed(InputHandler.CANCEL):
            self.close()
            return None
            
        return None
        
    def draw(self):
        """绘制菜单"""
        if not self.active:
            return
            
        # 计算菜单宽度（基于最长选项）
        max_option_width = max(text_width(opt) for opt in self.options)
        menu_width = max(max_option_width + 40, text_width(self.title) + 20)
        menu_height = len(self.options) * 18 + 36
        x = (WINDOW_WIDTH - menu_width) // 2
        y = (WINDOW_HEIGHT - menu_height) // 2
        
        pyxel.rect(x, y, menu_width, menu_height, COLOR_BLACK)
        pyxel.rectb(x, y, menu_width, menu_height, COLOR_WHITE)
        
        # 标题
        draw_text(x + 10, y + 8, self.title, COLOR_WHITE)
        
        # 选项
        for i, option in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected else COLOR_WHITE
            prefix = "> " if i == self.selected else "  "
            draw_text(x + 10, y + 28 + i * 18, prefix + option, color)
