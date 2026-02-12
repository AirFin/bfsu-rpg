# -*- coding: utf-8 -*-
"""
字体管理器
管理游戏中使用的自定义字体
"""

import pyxel

# 全局字体实例
_custom_font = None


def init_font(font_path="assets/font/ark-pixel-12px-proportional-zh_cn.bdf"):
    """
    初始化自定义字体
    
    参数:
        font_path: BDF 字体文件路径
    """
    global _custom_font
    try:
        _custom_font = pyxel.Font(font_path)
        print(f"[字体] 已加载自定义字体: {font_path}")
        return True
    except Exception as e:
        print(f"[字体] 加载字体失败: {e}")
        return False


def get_font():
    """获取自定义字体实例"""
    return _custom_font


def draw_text(x, y, text, color):
    """
    使用自定义字体绘制文字
    
    参数:
        x: X 坐标
        y: Y 坐标
        text: 要绘制的文字
        color: 颜色（0-15）
    """
    if _custom_font:
        pyxel.text(x, y, text, color, _custom_font)
    else:
        # 如果没有自定义字体，使用默认字体
        pyxel.text(x, y, text, color)


def text_width(text):
    """
    计算文字宽度
    
    参数:
        text: 要计算的文字
        
    返回:
        int: 文字宽度（像素）
    """
    if _custom_font:
        # 12px 字体，中文字符约12像素宽，英文约6像素宽
        width = 0
        for char in text:
            if ord(char) > 127:  # 中文或其他多字节字符
                width += 12
            else:
                width += 6
        return width
    else:
        # 默认字体每个字符4像素宽
        return len(text) * 4
