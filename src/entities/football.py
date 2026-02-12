# -*- coding: utf-8 -*-
"""
足球实体
可以被玩家或NPC踢动的足球
"""

import pyxel
import math
from config import TILE_SIZE


class Football:
    """足球类"""
    
    def __init__(self, x, y, field_bounds):
        """
        初始化足球
        
        参数:
            x: 初始X坐标（像素）
            y: 初始Y坐标（像素）
            field_bounds: 足球场边界 (min_x, min_y, max_x, max_y) 像素坐标
        """
        self.x = x
        self.y = y
        self.vx = 0  # X方向速度
        self.vy = 0  # Y方向速度
        self.radius = 4  # 足球半径
        self.friction = 0.92  # 摩擦力（速度衰减系数）
        self.kick_power = 3.0  # 踢球力度
        self.min_speed = 0.1  # 最小速度阈值
        
        # 足球场边界
        self.field_min_x = field_bounds[0]
        self.field_min_y = field_bounds[1]
        self.field_max_x = field_bounds[2]
        self.field_max_y = field_bounds[3]
        
        # 动画
        self.rotation = 0  # 旋转角度
        
    def update(self):
        """更新足球状态"""
        # 应用速度
        self.x += self.vx
        self.y += self.vy
        
        # 边界检测和反弹
        if self.x - self.radius < self.field_min_x:
            self.x = self.field_min_x + self.radius
            self.vx = -self.vx * 0.6  # 反弹并损失能量
        elif self.x + self.radius > self.field_max_x:
            self.x = self.field_max_x - self.radius
            self.vx = -self.vx * 0.6
            
        if self.y - self.radius < self.field_min_y:
            self.y = self.field_min_y + self.radius
            self.vy = -self.vy * 0.6
        elif self.y + self.radius > self.field_max_y:
            self.y = self.field_max_y - self.radius
            self.vy = -self.vy * 0.6
        
        # 应用摩擦力
        self.vx *= self.friction
        self.vy *= self.friction
        
        # 速度太小时停止
        if abs(self.vx) < self.min_speed:
            self.vx = 0
        if abs(self.vy) < self.min_speed:
            self.vy = 0
            
        # 更新旋转角度（根据速度）
        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        self.rotation += speed * 0.3
        
    def check_kick(self, entity_x, entity_y, entity_width, entity_height, target_x=None, target_y=None):
        """
        检查是否被实体（玩家或NPC）踢到
        
        参数:
            entity_x, entity_y: 实体位置
            entity_width, entity_height: 实体尺寸
            target_x, target_y: 目标位置（可选，如果指定则朝该方向踢）
            
        返回:
            bool: 是否被踢到
        """
        # 计算实体中心
        entity_cx = entity_x + entity_width / 2
        entity_cy = entity_y + entity_height / 2
        
        # 计算距离
        dx = self.x - entity_cx
        dy = self.y - entity_cy
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 检测碰撞范围
        kick_range = max(entity_width, entity_height) / 2 + self.radius + 2
        
        if distance < kick_range and distance > 0:
            # 被踢到，计算踢球方向
            if target_x is not None and target_y is not None:
                # 有目标位置，朝目标方向踢
                target_dx = target_x - self.x
                target_dy = target_y - self.y
                target_dist = math.sqrt(target_dx * target_dx + target_dy * target_dy)
                if target_dist > 0:
                    nx = target_dx / target_dist
                    ny = target_dy / target_dist
                else:
                    # 如果已在目标位置，用默认方向
                    nx = dx / distance
                    ny = dy / distance
            else:
                # 没有目标，从实体指向足球的方向
                nx = dx / distance
                ny = dy / distance
            
            # 应用踢球力度
            kick_strength = self.kick_power * 1.5  # 增加踢球力度
            self.vx += nx * kick_strength
            self.vy += ny * kick_strength
            
            # 限制最大速度
            max_speed = 6.0
            speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
            if speed > max_speed:
                self.vx = self.vx / speed * max_speed
                self.vy = self.vy / speed * max_speed
            
            return True
        return False
        
    def draw(self, camera_x, camera_y):
        """
        绘制足球
        
        参数:
            camera_x, camera_y: 相机偏移
        """
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # 只在屏幕范围内绘制
        if -10 < screen_x < 266 and -10 < screen_y < 266:
            # 足球本体（白色圆形）
            pyxel.circ(screen_x, screen_y, self.radius, 7)
            
            # 足球花纹（黑色五边形图案，简化版）
            # 根据旋转角度显示不同的花纹位置
            pattern_offset = int(self.rotation) % 4
            if pattern_offset == 0:
                pyxel.pset(screen_x - 1, screen_y - 1, 0)
                pyxel.pset(screen_x + 1, screen_y + 1, 0)
            elif pattern_offset == 1:
                pyxel.pset(screen_x + 1, screen_y - 1, 0)
                pyxel.pset(screen_x - 1, screen_y + 1, 0)
            elif pattern_offset == 2:
                pyxel.pset(screen_x, screen_y - 2, 0)
                pyxel.pset(screen_x, screen_y + 2, 0)
            else:
                pyxel.pset(screen_x - 2, screen_y, 0)
                pyxel.pset(screen_x + 2, screen_y, 0)
            
            # 中心点
            pyxel.pset(screen_x, screen_y, 0)
