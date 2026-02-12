# -*- coding: utf-8 -*-
"""
相机/视口模块
"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT


class Camera:
    """相机类"""
    
    def __init__(self, map_width, map_height):
        """
        初始化相机
        map_width, map_height: 地图的像素尺寸
        """
        self.x = 0
        self.y = 0
        self.map_width = map_width
        self.map_height = map_height
        
    def follow(self, target_x, target_y, smooth=0.1):
        """
        跟随目标
        smooth: 平滑系数（0-1），值越小越平滑
        """
        # 目标位置（将目标置于屏幕中心）
        target_cam_x = target_x - WINDOW_WIDTH // 2
        target_cam_y = target_y - WINDOW_HEIGHT // 2
        
        # 平滑移动
        self.x += (target_cam_x - self.x) * smooth
        self.y += (target_cam_y - self.y) * smooth
        
        # 边界限制
        self.x = max(0, min(self.x, self.map_width - WINDOW_WIDTH))
        self.y = max(0, min(self.y, self.map_height - WINDOW_HEIGHT))
        
    def set_position(self, x, y):
        """直接设置相机位置"""
        self.x = max(0, min(x, self.map_width - WINDOW_WIDTH))
        self.y = max(0, min(y, self.map_height - WINDOW_HEIGHT))
        
    def world_to_screen(self, world_x, world_y):
        """将世界坐标转换为屏幕坐标"""
        return world_x - self.x, world_y - self.y
        
    def screen_to_world(self, screen_x, screen_y):
        """将屏幕坐标转换为世界坐标"""
        return screen_x + self.x, screen_y + self.y
        
    def is_visible(self, x, y, width, height):
        """检查对象是否在视口内"""
        return (x + width > self.x and
                x < self.x + WINDOW_WIDTH and
                y + height > self.y and
                y < self.y + WINDOW_HEIGHT)
