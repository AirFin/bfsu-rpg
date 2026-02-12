# -*- coding: utf-8 -*-
"""
输入处理模块
"""

import pyxel


class InputHandler:
    """输入处理器"""
    
    # 按键映射
    KEY_UP = [pyxel.KEY_UP, pyxel.KEY_W]
    KEY_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S]
    KEY_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A]
    KEY_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D]
    KEY_CONFIRM = [pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_Z]
    KEY_CANCEL = [pyxel.KEY_ESCAPE, pyxel.KEY_X]
    KEY_MENU = [pyxel.KEY_M]
    
    @staticmethod
    def is_pressed(keys):
        """检测按键是否被按下（持续）"""
        return any(pyxel.btn(key) for key in keys)
    
    @staticmethod
    def is_just_pressed(keys):
        """检测按键是否刚被按下"""
        return any(pyxel.btnp(key) for key in keys)
    
    @classmethod
    def get_movement(cls):
        """获取移动方向"""
        dx, dy = 0, 0
        
        if cls.is_pressed(cls.KEY_UP):
            dy = -1
        elif cls.is_pressed(cls.KEY_DOWN):
            dy = 1
            
        if cls.is_pressed(cls.KEY_LEFT):
            dx = -1
        elif cls.is_pressed(cls.KEY_RIGHT):
            dx = 1
            
        return dx, dy
