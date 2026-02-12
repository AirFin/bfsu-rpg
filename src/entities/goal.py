# -*- coding: utf-8 -*-
"""
足球球门实体
"""

import pyxel
import math
from config import TILE_SIZE


class Goal:
    """足球球门类"""
    
    def __init__(self, x, y, side):
        """
        初始化球门
        
        参数:
            x: 球门中心X坐标（像素）
            y: 球门中心Y坐标（像素）
            side: 球门朝向 ('left' 或 'right')
                  'left' = 球门在左边，面向右
                  'right' = 球门在右边，面向左
        """
        self.x = x
        self.y = y
        self.side = side
        
        # 球门尺寸
        self.width = 8  # 球门深度
        self.height = 48  # 球门高度（3个tile高）
        
        # 球门区域（用于检测进球）
        if side == 'left':
            # 左侧球门，检测区域在球门右侧
            self.goal_area_x1 = x
            self.goal_area_x2 = x + self.width
        else:
            # 右侧球门，检测区域在球门左侧
            self.goal_area_x1 = x - self.width
            self.goal_area_x2 = x
            
        self.goal_area_y1 = y - self.height // 2
        self.goal_area_y2 = y + self.height // 2
        
        # 进球动画
        self.goal_scored = False
        self.goal_timer = 0
        self.score = 0  # 进球数
        
    def check_goal(self, ball_x, ball_y, ball_radius):
        """
        检测是否进球
        
        参数:
            ball_x, ball_y: 球的位置
            ball_radius: 球的半径
            
        返回:
            bool: 是否进球
        """
        # 检测球是否在球门区域内
        if (self.goal_area_x1 < ball_x < self.goal_area_x2 and
            self.goal_area_y1 < ball_y < self.goal_area_y2):
            if not self.goal_scored:
                self.goal_scored = True
                self.goal_timer = 60  # 1秒的进球动画
                self.score += 1
                return True
        return False
        
    def update(self):
        """更新球门状态"""
        if self.goal_timer > 0:
            self.goal_timer -= 1
            if self.goal_timer == 0:
                self.goal_scored = False
                
    def get_target_position(self):
        """
        获取射门目标位置（球门中心）
        
        返回:
            (x, y): 射门目标坐标
        """
        return (self.x, self.y)
        
    def draw(self, camera_x, camera_y):
        """
        绘制球门
        
        参数:
            camera_x, camera_y: 相机偏移
        """
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # 只在屏幕范围内绘制
        if -50 < screen_x < 306 and -50 < screen_y < 306:
            half_h = self.height // 2
            
            if self.side == 'left':
                # 左侧球门（面向右开口）
                # 球门框架 - 白色
                # 上横梁
                pyxel.rect(screen_x, screen_y - half_h, self.width, 3, 7)
                # 下横梁  
                pyxel.rect(screen_x, screen_y + half_h - 3, self.width, 3, 7)
                # 后立柱
                pyxel.rect(screen_x, screen_y - half_h, 3, self.height, 7)
                # 球门网（深色格子）
                for i in range(0, self.height, 4):
                    pyxel.line(screen_x + 3, screen_y - half_h + i, 
                              screen_x + self.width - 1, screen_y - half_h + i, 5)
                for i in range(3, self.width, 4):
                    pyxel.line(screen_x + i, screen_y - half_h + 3,
                              screen_x + i, screen_y + half_h - 3, 5)
            else:
                # 右侧球门（面向左开口）
                # 上横梁
                pyxel.rect(screen_x - self.width, screen_y - half_h, self.width, 3, 7)
                # 下横梁
                pyxel.rect(screen_x - self.width, screen_y + half_h - 3, self.width, 3, 7)
                # 后立柱
                pyxel.rect(screen_x - 3, screen_y - half_h, 3, self.height, 7)
                # 球门网
                for i in range(0, self.height, 4):
                    pyxel.line(screen_x - self.width + 1, screen_y - half_h + i,
                              screen_x - 3, screen_y - half_h + i, 5)
                for i in range(3, self.width, 4):
                    pyxel.line(screen_x - self.width + i, screen_y - half_h + 3,
                              screen_x - self.width + i, screen_y + half_h - 3, 5)
            
            # 进球特效
            if self.goal_scored and self.goal_timer > 0:
                # 闪烁效果
                if self.goal_timer % 10 < 5:
                    pyxel.circb(screen_x, screen_y, 20 + (60 - self.goal_timer) // 3, 10)
                    pyxel.circb(screen_x, screen_y, 15 + (60 - self.goal_timer) // 3, 8)
