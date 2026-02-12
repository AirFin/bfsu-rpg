# -*- coding: utf-8 -*-
"""
图书馆内部渲染器
绘制图书馆内部场景：书架、桌椅、地板等
"""

import pyxel
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.map.campus_map import (
    LIBRARY_MAP, LIBRARY_WIDTH, LIBRARY_HEIGHT, LIBRARY_COLLISION_MAP,
    TILE_LIB_WALL, TILE_LIB_FLOOR, TILE_LIB_BOOKSHELF, TILE_LIB_CHAIR,
    TILE_LIB_TABLE, TILE_LIB_DOOR, TILE_LIB_COUNTER
)


class LibraryRenderer:
    """图书馆内部渲染器"""
    
    def __init__(self):
        self.time = 0
    
    def update(self, weather=None):
        """更新图书馆状态"""
        self.time += 1
    
    def render(self, camera_x, camera_y):
        """渲染图书馆内部"""
        # 背景色（室内暖色调）
        pyxel.cls(15)  # 米色背景
        
        # 渲染地图瓦片
        for tile_y in range(LIBRARY_HEIGHT):
            for tile_x in range(LIBRARY_WIDTH):
                screen_x = tile_x * TILE_SIZE - camera_x
                screen_y = tile_y * TILE_SIZE - camera_y
                
                # 跳过屏幕外的瓦片
                if screen_x < -TILE_SIZE or screen_x > WINDOW_WIDTH:
                    continue
                if screen_y < -TILE_SIZE or screen_y > WINDOW_HEIGHT:
                    continue
                
                tile = LIBRARY_MAP[tile_y][tile_x]
                self._draw_tile(int(screen_x), int(screen_y), tile, tile_x, tile_y)
        
        # 绘制装饰
        self._draw_decorations(camera_x, camera_y)
    
    def _draw_tile(self, screen_x, screen_y, tile, tile_x, tile_y):
        """绘制单个瓦片"""
        if tile == TILE_LIB_WALL:
            # 墙壁 - 米白色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 7)
            # 墙裙
            pyxel.rect(screen_x, screen_y + 12, TILE_SIZE, 4, 13)
            
        elif tile == TILE_LIB_FLOOR:
            # 地板 - 木地板纹理
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)  # 棕色基底
            # 木纹
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE - 1, screen_y + 4, 9)
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE - 1, screen_y + 10, 9)
            
        elif tile == TILE_LIB_BOOKSHELF:
            # 书架 - 先画地板
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)
            # 书架主体（深棕色）
            pyxel.rect(screen_x + 1, screen_y, TILE_SIZE - 2, TILE_SIZE - 2, 9)
            # 书架层板
            pyxel.line(screen_x + 1, screen_y + 5, screen_x + TILE_SIZE - 2, screen_y + 5, 4)
            pyxel.line(screen_x + 1, screen_y + 10, screen_x + TILE_SIZE - 2, screen_y + 10, 4)
            # 书籍（多彩）
            colors = [8, 11, 12, 2, 3, 10]  # 红、青、蓝、紫、绿、黄
            for i, col in enumerate(colors[:3]):
                pyxel.rect(screen_x + 2 + i * 4, screen_y + 1, 3, 4, col)
            for i, col in enumerate(colors[3:]):
                pyxel.rect(screen_x + 2 + i * 4, screen_y + 6, 3, 4, col)
            
        elif tile == TILE_LIB_CHAIR:
            # 椅子 - 先画地板
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE - 1, screen_y + 4, 9)
            # 椅子主体
            pyxel.rect(screen_x + 3, screen_y + 4, 10, 8, 9)  # 座位（棕色）
            pyxel.rect(screen_x + 4, screen_y + 1, 8, 4, 9)   # 椅背
            # 高光
            pyxel.pset(screen_x + 5, screen_y + 2, 15)
            pyxel.rect(screen_x + 4, screen_y + 5, 8, 2, 4)   # 座垫
            
        elif tile == TILE_LIB_TABLE:
            # 桌子 - 先画地板
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE - 1, screen_y + 4, 9)
            # 桌子主体（浅棕色）
            pyxel.rect(screen_x + 1, screen_y + 3, 14, 10, 15)  # 桌面
            pyxel.rect(screen_x + 1, screen_y + 3, 14, 2, 9)    # 桌沿
            # 桌腿
            pyxel.rect(screen_x + 2, screen_y + 12, 2, 4, 4)
            pyxel.rect(screen_x + 12, screen_y + 12, 2, 4, 4)
            
        elif tile == TILE_LIB_DOOR:
            # 门 - 可通行入口
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)  # 地板
            # 门框
            pyxel.rect(screen_x + 2, screen_y, 12, TILE_SIZE, 9)
            # 门
            pyxel.rect(screen_x + 3, screen_y + 1, 10, TILE_SIZE - 2, 4)
            # 门把手
            pyxel.pset(screen_x + 11, screen_y + 8, 10)
            
        elif tile == TILE_LIB_COUNTER:
            # 服务台 - 先画地板
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)
            # 柜台（深棕色）
            pyxel.rect(screen_x, screen_y + 2, TILE_SIZE, 12, 9)
            # 柜台面（浅色）
            pyxel.rect(screen_x, screen_y + 2, TILE_SIZE, 3, 15)
            # 细节
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE - 1, screen_y + 4, 4)
    
    def _draw_decorations(self, camera_x, camera_y):
        """绘制装饰元素"""
        # 天花板灯光效果（简单渐变）
        for x in range(0, LIBRARY_WIDTH * TILE_SIZE, 64):
            screen_x = x - camera_x + 32
            screen_y = 8 - camera_y
            if 0 <= screen_x <= WINDOW_WIDTH:
                # 灯泡
                pyxel.circ(int(screen_x), int(screen_y), 3, 10)
                pyxel.circ(int(screen_x), int(screen_y), 2, 7)
        
        # "阅览室"标志
        sign_x = 7 * TILE_SIZE - camera_x
        sign_y = 0 * TILE_SIZE - camera_y + 4
        if 0 <= sign_x <= WINDOW_WIDTH and 0 <= sign_y <= WINDOW_HEIGHT:
            pyxel.rect(int(sign_x) - 20, int(sign_y), 56, 10, 2)
            # 文字由game_scene绘制
    
    def is_collision(self, x, y, width, height):
        """检查碰撞"""
        # 将像素坐标转换为瓦片坐标
        left_tile = int(x // TILE_SIZE)
        right_tile = int((x + width - 1) // TILE_SIZE)
        top_tile = int(y // TILE_SIZE)
        bottom_tile = int((y + height - 1) // TILE_SIZE)
        
        # 检查边界
        if left_tile < 0 or right_tile >= LIBRARY_WIDTH:
            return True
        if top_tile < 0 or bottom_tile >= LIBRARY_HEIGHT:
            return True
        
        # 检查碰撞地图
        for ty in range(top_tile, bottom_tile + 1):
            for tx in range(left_tile, right_tile + 1):
                if 0 <= ty < LIBRARY_HEIGHT and 0 <= tx < LIBRARY_WIDTH:
                    if LIBRARY_COLLISION_MAP[ty][tx] == 1:
                        return True
        
        return False
    
    def get_tile_at(self, x, y):
        """获取指定像素位置的瓦片类型"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        if 0 <= tile_x < LIBRARY_WIDTH and 0 <= tile_y < LIBRARY_HEIGHT:
            return LIBRARY_MAP[tile_y][tile_x]
        return None
    
    def get_tile_pos(self, x, y):
        """获取指定像素位置的瓦片坐标"""
        return (int(x // TILE_SIZE), int(y // TILE_SIZE))
