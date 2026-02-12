# -*- coding: utf-8 -*-
"""
标题场景
游戏开始画面
"""

import pyxel
import math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_YELLOW
from src.utils.font_manager import draw_text, text_width


class TitleScene:
    """标题场景"""
    
    def __init__(self, scene_manager):
        """初始化标题场景"""
        self.scene_manager = scene_manager
        self.blink_timer = 0
        self.show_text = True
        self.time = 0
        
    def on_enter(self):
        """进入场景时调用"""
        self.blink_timer = 0
        self.time = 0
        
    def on_exit(self):
        """退出场景时调用"""
        pass
        
    def update(self):
        """更新逻辑"""
        self.time += 1
        
        # 闪烁效果
        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.blink_timer = 0
            self.show_text = not self.show_text
        
        # 按键检测
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            from src.scenes.scene_manager import SceneType
            self.scene_manager.change_scene(SceneType.LLM_SETUP)
            
    def draw(self):
        """绘制画面"""
        # 绘制简单的校园背景
        self._draw_background()
        
        # 半透明遮罩
        for y in range(0, WINDOW_HEIGHT, 2):
            pyxel.line(0, y, WINDOW_WIDTH, y, 0)
        
        # 绘制标题
        title = "北外RPG"
        title_x = (WINDOW_WIDTH - text_width(title)) // 2
        # 标题阴影
        draw_text(title_x + 1, 81, title, 0)
        draw_text(title_x, 80, title, COLOR_YELLOW)
        
        # 副标题
        subtitle = "- 北京外国语大学 -"
        sub_x = (WINDOW_WIDTH - text_width(subtitle)) // 2
        draw_text(sub_x, 98, subtitle, 7)
        
        # 绘制提示文字（闪烁）
        if self.show_text:
            hint = "按 ENTER 继续"
            hint_x = (WINDOW_WIDTH - text_width(hint)) // 2
            draw_text(hint_x, 150, hint, COLOR_WHITE)
            
        # 操作说明
        help_text = "WASD - 移动"
        draw_text((WINDOW_WIDTH - text_width(help_text)) // 2, 180, help_text, 6)
        
        # 绘制版权信息
        copyright_text = "(C) 2024"
        draw_text(WINDOW_WIDTH - text_width(copyright_text) - 10, 
                   WINDOW_HEIGHT - 14, 
                   copyright_text, 
                   5)
                   
    def _draw_background(self):
        """绘制标题背景"""
        # 天空
        pyxel.rect(0, 0, WINDOW_WIDTH, 150, 12)
        
        # 草地
        pyxel.rect(0, 150, WINDOW_WIDTH, WINDOW_HEIGHT - 150, 3)
        
        # 简单的建筑轮廓
        pyxel.rect(50, 100, 60, 50, 4)
        pyxel.rect(150, 110, 50, 40, 4)
        
        # 窗户
        for i in range(3):
            pyxel.rect(55 + i * 18, 110, 8, 10, 12)
            pyxel.rect(55 + i * 18, 125, 8, 10, 12)
            
        # 树木
        wind = math.sin(self.time * 0.03) * 2
        self._draw_simple_tree(20, 130, wind)
        self._draw_simple_tree(220, 125, wind * 0.8)
        
    def _draw_simple_tree(self, x, y, sway):
        """绘制简单的树"""
        # 树干
        pyxel.rect(x + 6, y, 4, 20, 4)
        # 树冠
        pyxel.circ(x + 8 + sway, y - 5, 10, 3)
        pyxel.circ(x + 8 + sway * 0.5, y - 10, 8, 11)
