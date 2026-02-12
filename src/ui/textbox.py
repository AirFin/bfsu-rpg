# -*- coding: utf-8 -*-
"""
文本框模块
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK
from src.utils.font_manager import draw_text


class TextBox:
    """文本框类"""
    
    def __init__(self):
        """初始化文本框"""
        self.visible = False
        self.text = ""
        self.speaker = ""
        
    def show(self, text, speaker=""):
        """显示文本框"""
        self.visible = True
        self.text = text
        self.speaker = speaker
        
    def hide(self):
        """隐藏文本框"""
        self.visible = False
        
    def update(self):
        """更新文本框"""
        if not self.visible:
            return False
            
        # 按键关闭
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.hide()
            return True
            
        return False
        
    def draw(self):
        """绘制文本框"""
        if not self.visible:
            return
            
        # 文本框尺寸和位置
        box_width = WINDOW_WIDTH - 20
        box_height = 50
        x = 10
        y = WINDOW_HEIGHT - box_height - 10
        
        # 背景
        pyxel.rect(x, y, box_width, box_height, COLOR_BLACK)
        pyxel.rectb(x, y, box_width, box_height, COLOR_WHITE)
        
        # 说话者名字
        if self.speaker:
            draw_text(x + 8, y + 6, self.speaker, COLOR_WHITE)
            draw_text(x + 8, y + 20, self.text, COLOR_WHITE)
        else:
            draw_text(x + 8, y + 14, self.text, COLOR_WHITE)
