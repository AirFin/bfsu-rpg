# -*- coding: utf-8 -*-
"""
辅助函数
"""

import math


def clamp(value, min_val, max_val):
    """将值限制在范围内"""
    return max(min_val, min(value, max_val))


def lerp(start, end, t):
    """线性插值"""
    return start + (end - start) * t


def distance(x1, y1, x2, y2):
    """计算两点之间的距离"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def normalize(x, y):
    """向量归一化"""
    length = math.sqrt(x ** 2 + y ** 2)
    if length == 0:
        return 0, 0
    return x / length, y / length


def sign(value):
    """返回值的符号"""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


def approach(current, target, step):
    """逐步接近目标值"""
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return target


def wrap(value, min_val, max_val):
    """循环值在范围内"""
    range_size = max_val - min_val
    return ((value - min_val) % range_size) + min_val
