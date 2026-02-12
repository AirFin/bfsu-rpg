# -*- coding: utf-8 -*-
"""
输入处理模块
"""

import math
import pyxel

try:
    from js import window as js_window  # Web(Pyodide) only
except Exception:  # pragma: no cover - desktop runtime
    js_window = None


class InputHandler:
    """输入处理器"""

    MOBILE_STATE_NAME = "__BFSU_MOBILE_INPUT"
    MOBILE_DEADZONE = 0.2

    # 语义动作映射（键盘 + 虚拟手柄）
    MOVE_UP = [pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP]
    MOVE_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN]
    MOVE_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
    MOVE_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT]

    CONFIRM = [pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_Z, pyxel.GAMEPAD1_BUTTON_A]
    CANCEL = [pyxel.KEY_ESCAPE, pyxel.KEY_X, pyxel.GAMEPAD1_BUTTON_B]
    SUBMIT = [pyxel.KEY_RETURN, pyxel.GAMEPAD1_BUTTON_A]
    BACK = [pyxel.KEY_ESCAPE, pyxel.GAMEPAD1_BUTTON_B]
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

    _mobile_last_sync_frame = -1
    _mobile_current = {
        "active": False,
        "axes": {"x": 0.0, "y": 0.0},
        "buttons": {"a": False, "b": False, "x": False, "start": False},
    }
    _mobile_previous = {
        "active": False,
        "axes": {"x": 0.0, "y": 0.0},
        "buttons": {"a": False, "b": False, "x": False, "start": False},
    }

    @classmethod
    def _blank_mobile_state(cls):
        return {
            "active": False,
            "axes": {"x": 0.0, "y": 0.0},
            "buttons": {"a": False, "b": False, "x": False, "start": False},
        }

    @classmethod
    def _copy_mobile_state(cls, state):
        return {
            "active": bool(state["active"]),
            "axes": {
                "x": float(state["axes"]["x"]),
                "y": float(state["axes"]["y"]),
            },
            "buttons": {
                "a": bool(state["buttons"]["a"]),
                "b": bool(state["buttons"]["b"]),
                "x": bool(state["buttons"]["x"]),
                "start": bool(state["buttons"]["start"]),
            },
        }

    @classmethod
    def _clamp_axis(cls, value):
        return max(-1.0, min(1.0, float(value)))

    @classmethod
    def _sync_mobile_state(cls):
        frame = getattr(pyxel, "frame_count", -1)
        if frame == cls._mobile_last_sync_frame:
            return
        cls._mobile_last_sync_frame = frame

        cls._mobile_previous = cls._copy_mobile_state(cls._mobile_current)
        cls._mobile_current = cls._blank_mobile_state()

        if js_window is None:
            return

        try:
            state = getattr(js_window, cls.MOBILE_STATE_NAME)
        except Exception:
            return

        if state is None:
            return

        try:
            active = bool(getattr(state, "active"))
        except Exception:
            active = False

        if not active:
            return

        cls._mobile_current["active"] = True

        try:
            axes = getattr(state, "axes")
            cls._mobile_current["axes"]["x"] = cls._clamp_axis(getattr(axes, "x"))
            cls._mobile_current["axes"]["y"] = cls._clamp_axis(getattr(axes, "y"))
        except Exception:
            pass

        try:
            buttons = getattr(state, "buttons")
            cls._mobile_current["buttons"]["a"] = bool(getattr(buttons, "a"))
            cls._mobile_current["buttons"]["b"] = bool(getattr(buttons, "b"))
            cls._mobile_current["buttons"]["x"] = bool(getattr(buttons, "x"))
            cls._mobile_current["buttons"]["start"] = bool(getattr(buttons, "start"))
        except Exception:
            pass

    @classmethod
    def _match_mobile_direction(cls, keys):
        if keys is cls.MOVE_UP or keys == cls.MOVE_UP:
            return "up"
        if keys is cls.MOVE_DOWN or keys == cls.MOVE_DOWN:
            return "down"
        if keys is cls.MOVE_LEFT or keys == cls.MOVE_LEFT:
            return "left"
        if keys is cls.MOVE_RIGHT or keys == cls.MOVE_RIGHT:
            return "right"
        return None

    @classmethod
    def _match_mobile_buttons(cls, keys):
        if keys is cls.CONFIRM or keys == cls.CONFIRM:
            return ("a",)
        if keys is cls.SUBMIT or keys == cls.SUBMIT:
            return ("a",)
        if keys is cls.INTERACT or keys == cls.INTERACT:
            return ("a",)
        if keys is cls.CANCEL or keys == cls.CANCEL:
            return ("b",)
        if keys is cls.BACK or keys == cls.BACK:
            return ("b",)
        if keys is cls.EXIT_DIALOGUE or keys == cls.EXIT_DIALOGUE:
            return ("b",)
        if keys is cls.MENU or keys == cls.MENU:
            return ("start",)
        if keys is cls.SKATE_TOGGLE or keys == cls.SKATE_TOGGLE:
            return ("x",)
        return tuple()

    @classmethod
    def _mobile_direction_pressed(cls, direction):
        if not cls._mobile_current["active"]:
            return False

        axis_x = cls._mobile_current["axes"]["x"]
        axis_y = cls._mobile_current["axes"]["y"]
        if direction == "up":
            return axis_y <= -cls.MOBILE_DEADZONE
        if direction == "down":
            return axis_y >= cls.MOBILE_DEADZONE
        if direction == "left":
            return axis_x <= -cls.MOBILE_DEADZONE
        if direction == "right":
            return axis_x >= cls.MOBILE_DEADZONE
        return False

    @classmethod
    def _mobile_direction_just_pressed(cls, direction):
        if not cls._mobile_current["active"]:
            return False

        prev_x = cls._mobile_previous["axes"]["x"]
        prev_y = cls._mobile_previous["axes"]["y"]
        curr_x = cls._mobile_current["axes"]["x"]
        curr_y = cls._mobile_current["axes"]["y"]

        if direction == "up":
            return prev_y > -cls.MOBILE_DEADZONE and curr_y <= -cls.MOBILE_DEADZONE
        if direction == "down":
            return prev_y < cls.MOBILE_DEADZONE and curr_y >= cls.MOBILE_DEADZONE
        if direction == "left":
            return prev_x > -cls.MOBILE_DEADZONE and curr_x <= -cls.MOBILE_DEADZONE
        if direction == "right":
            return prev_x < cls.MOBILE_DEADZONE and curr_x >= cls.MOBILE_DEADZONE
        return False

    @staticmethod
    def is_pressed(keys):
        """检测按键是否被按下（持续）"""
        InputHandler._sync_mobile_state()

        if any(pyxel.btn(key) for key in keys):
            return True

        direction = InputHandler._match_mobile_direction(keys)
        if direction and InputHandler._mobile_direction_pressed(direction):
            return True

        for button_name in InputHandler._match_mobile_buttons(keys):
            if InputHandler._mobile_current["buttons"][button_name]:
                return True

        return False

    @staticmethod
    def is_just_pressed(keys, hold=None, period=None):
        """检测按键是否刚被按下，可选重复触发参数"""
        InputHandler._sync_mobile_state()

        if hold is None or period is None:
            if any(pyxel.btnp(key) for key in keys):
                return True
        else:
            if any(pyxel.btnp(key, hold, period) for key in keys):
                return True

        direction = InputHandler._match_mobile_direction(keys)
        if direction and InputHandler._mobile_direction_just_pressed(direction):
            return True

        for button_name in InputHandler._match_mobile_buttons(keys):
            if (
                InputHandler._mobile_current["buttons"][button_name]
                and not InputHandler._mobile_previous["buttons"][button_name]
            ):
                return True

        return False

    @classmethod
    def get_movement(cls):
        """获取移动方向"""
        cls._sync_mobile_state()

        if cls._mobile_current["active"]:
            axis_x = cls._mobile_current["axes"]["x"]
            axis_y = cls._mobile_current["axes"]["y"]

            if abs(axis_x) < cls.MOBILE_DEADZONE:
                axis_x = 0.0
            if abs(axis_y) < cls.MOBILE_DEADZONE:
                axis_y = 0.0

            if axis_x != 0.0 or axis_y != 0.0:
                return axis_x, axis_y

        left = any(pyxel.btn(key) for key in cls.MOVE_LEFT)
        right = any(pyxel.btn(key) for key in cls.MOVE_RIGHT)
        up = any(pyxel.btn(key) for key in cls.MOVE_UP)
        down = any(pyxel.btn(key) for key in cls.MOVE_DOWN)

        dx = float(right) - float(left)
        dy = float(down) - float(up)

        if dx != 0.0 and dy != 0.0:
            diagonal_scale = 1.0 / math.sqrt(2.0)
            dx *= diagonal_scale
            dy *= diagonal_scale

        return dx, dy
