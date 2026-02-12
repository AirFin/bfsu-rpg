# -*- coding: utf-8 -*-
"""
输入处理模块
"""

import pyxel


class InputHandler:
    """输入处理器"""

    # 语义动作映射（键盘 + 虚拟手柄）
    MOVE_UP = [pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP]
    MOVE_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN]
    MOVE_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
    MOVE_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT]

    CONFIRM = [pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_Z, pyxel.GAMEPAD1_BUTTON_A]
    CANCEL = [pyxel.KEY_ESCAPE, pyxel.KEY_X, pyxel.GAMEPAD1_BUTTON_B]
    MENU = [pyxel.KEY_M, pyxel.GAMEPAD1_BUTTON_START]
    INTERACT = [pyxel.KEY_SPACE, pyxel.KEY_RETURN, pyxel.KEY_Z, pyxel.GAMEPAD1_BUTTON_A]
    SKATE_TOGGLE = [pyxel.KEY_B, pyxel.GAMEPAD1_BUTTON_X]
    EXIT_DIALOGUE = [pyxel.KEY_TAB, pyxel.GAMEPAD1_BUTTON_B]

    # 兼容旧命名
    KEY_UP = MOVE_UP
    KEY_DOWN = MOVE_DOWN
    KEY_LEFT = MOVE_LEFT
    KEY_RIGHT = MOVE_RIGHT
    KEY_CONFIRM = CONFIRM
    KEY_CANCEL = CANCEL
    KEY_MENU = MENU

    @staticmethod
    def is_pressed(keys):
        """检测按键是否被按下（持续）"""
        return any(pyxel.btn(key) for key in keys)

    @staticmethod
    def is_just_pressed(keys, hold=None, period=None):
        """检测按键是否刚被按下，可选重复触发参数"""
        if hold is None or period is None:
            return any(pyxel.btnp(key) for key in keys)
        return any(pyxel.btnp(key, hold, period) for key in keys)

    @classmethod
    def get_movement(cls):
        """获取移动方向"""
        dx, dy = 0, 0

        if cls.is_pressed(cls.MOVE_UP):
            dy = -1
        elif cls.is_pressed(cls.MOVE_DOWN):
            dy = 1

        if cls.is_pressed(cls.MOVE_LEFT):
            dx = -1
        elif cls.is_pressed(cls.MOVE_RIGHT):
            dx = 1

        return dx, dy
