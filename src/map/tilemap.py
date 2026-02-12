# -*- coding: utf-8 -*-
"""
瓦片地图模块
"""

import pyxel
from config import TILE_SIZE


class TileMap:
    """瓦片地图"""
    
    def __init__(self, width, height):
        """
        初始化地图
        width, height: 地图尺寸（瓦片数量）
        """
        self.width = width
        self.height = height
        self.tiles = [[0 for _ in range(width)] for _ in range(height)]
        self.collision_layer = [[False for _ in range(width)] for _ in range(height)]
        
    def get_tile(self, x, y):
        """获取指定位置的瓦片"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return -1
        
    def set_tile(self, x, y, tile_id):
        """设置指定位置的瓦片"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_id
            
    def is_collision(self, x, y):
        """检查指定位置是否有碰撞"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.collision_layer[tile_y][tile_x]
        return True  # 边界外视为碰撞
        
    def set_collision(self, x, y, is_solid):
        """设置碰撞"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.collision_layer[y][x] = is_solid
            
    def draw(self, camera_x=0, camera_y=0):
        """
        绘制地图
        使用 Pyxel 的 bltm 函数从资源文件绘制瓦片地图
        """
        # 计算可见区域
        start_x = max(0, int(camera_x // TILE_SIZE))
        start_y = max(0, int(camera_y // TILE_SIZE))
        
        # 简单绘制（使用颜色块代替瓦片）
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                screen_x = x * TILE_SIZE - camera_x
                screen_y = y * TILE_SIZE - camera_y
                
                # 根据 tile_id 选择颜色
                color = 3 if tile_id == 0 else 4  # 草地/泥土
                pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, color)
                
    def load_from_data(self, data):
        """从数据加载地图"""
        if "tiles" in data:
            self.tiles = data["tiles"]
            self.height = len(self.tiles)
            self.width = len(self.tiles[0]) if self.tiles else 0
        if "collision" in data:
            self.collision_layer = data["collision"]
