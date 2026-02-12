# -*- coding: utf-8 -*-
"""
地下通道渲染器
绘制连接东校区和西校区的地下通道
"""

import pyxel
import math
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.map.campus_map import (
    TUNNEL_MAP, TUNNEL_COLLISION_MAP, TUNNEL_WIDTH, TUNNEL_HEIGHT,
    TILE_TUNNEL_WALL, TILE_TUNNEL_FLOOR, TILE_TUNNEL_LIGHT,
    TILE_TUNNEL_ENTRY, TILE_TUNNEL_EXIT
)
from src.utils.font_manager import draw_text, text_width


class TunnelRenderer:
    """地下通道渲染器"""
    
    def __init__(self):
        """初始化"""
        self.time = 0
        self.light_flicker = 0
        
    def update(self, weather='sunny'):
        """更新动画"""
        self.time += 1
        # 灯光闪烁效果
        self.light_flicker = math.sin(self.time * 0.1) * 0.3 + 0.7
        
    def draw(self, camera_x, camera_y):
        """绘制地下通道"""
        # 深色背景
        pyxel.cls(0)
        
        # 确保相机坐标不为负数
        camera_x = max(0, camera_x)
        camera_y = max(0, camera_y)
        
        # 计算可见范围（确保不越界）
        start_tile_x = max(0, int(camera_x // TILE_SIZE) - 1)
        start_tile_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_tile_x = min(TUNNEL_WIDTH, int((camera_x + WINDOW_WIDTH) // TILE_SIZE) + 2)
        end_tile_y = min(TUNNEL_HEIGHT, int((camera_y + WINDOW_HEIGHT) // TILE_SIZE) + 2)
        
        # 绘制瓦片
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                self._draw_tile(x, y, camera_x, camera_y)
        
        # 绘制方向指示
        self._draw_direction_signs(camera_x, camera_y)
                
    def _draw_tile(self, tile_x, tile_y, camera_x, camera_y):
        """绘制单个瓦片"""
        # 边界检查：确保tile_y和tile_x在有效范围内
        if tile_y < 0 or tile_y >= len(TUNNEL_MAP):
            return
        if tile_x < 0 or tile_x >= len(TUNNEL_MAP[0]) if len(TUNNEL_MAP) > 0 else TUNNEL_WIDTH:
            return
            
        tile = TUNNEL_MAP[tile_y][tile_x]
        screen_x = int(tile_x * TILE_SIZE - camera_x)
        screen_y = int(tile_y * TILE_SIZE - camera_y)
        
        if tile == TILE_TUNNEL_WALL:
            # 墙壁 - 深灰色砖墙
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 5)
            # 砖纹
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE, screen_y + 4, 1)
            pyxel.line(screen_x, screen_y + 8, screen_x + TILE_SIZE, screen_y + 8, 1)
            pyxel.line(screen_x, screen_y + 12, screen_x + TILE_SIZE, screen_y + 12, 1)
            pyxel.line(screen_x + 8, screen_y, screen_x + 8, screen_y + TILE_SIZE, 1)
            
        elif tile == TILE_TUNNEL_FLOOR:
            # 地面 - 灰色地砖
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 13)
            # 地砖纹理
            pyxel.rectb(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 5)
            # 地面污渍
            seed = (tile_x * 7 + tile_y * 11) % 13
            if seed < 3:
                pyxel.pset(screen_x + seed + 4, screen_y + 8, 5)
                
        elif tile == TILE_TUNNEL_LIGHT:
            # 灯光位置 - 地面+顶灯效果
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 13)
            pyxel.rectb(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 5)
            
            # 灯光照射效果（黄色渐变）
            light_intensity = int(self.light_flicker * 3)
            if light_intensity > 0:
                pyxel.rect(screen_x + 4, screen_y + 4, 8, 8, 10)  # 金黄色光斑
                pyxel.rect(screen_x + 6, screen_y + 6, 4, 4, 7)   # 白色中心
                
            # 顶部灯具
            pyxel.rect(screen_x + 5, screen_y - 2, 6, 3, 6)
            
        elif tile == TILE_TUNNEL_ENTRY:
            # 入口（从东校区来）- 绿色地面+向上箭头标识
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            # 标识线
            pyxel.rect(screen_x + 6, screen_y + 2, 4, 12, 11)
            # 向上箭头（表示通往东校区）
            pyxel.tri(screen_x + 8, screen_y, screen_x + 4, screen_y + 6, screen_x + 12, screen_y + 6, 7)
            
        elif tile == TILE_TUNNEL_EXIT:
            # 出口（通往西校区）- 蓝色地面+向下箭头标识
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 1)
            # 标识线
            pyxel.rect(screen_x + 6, screen_y + 2, 4, 12, 12)
            # 向下箭头（表示通往西校区）
            pyxel.tri(screen_x + 8, screen_y + 16, screen_x + 4, screen_y + 10, screen_x + 12, screen_y + 10, 7)
    
    def _draw_direction_signs(self, camera_x, camera_y):
        """绘制方向指示牌"""
        # 上方指示牌（东校区方向）
        sign_x = 10 * TILE_SIZE - camera_x
        sign_y = 2 * TILE_SIZE - camera_y
        if 0 <= sign_y < WINDOW_HEIGHT:
            # 指示牌背景
            pyxel.rect(int(sign_x - 20), int(sign_y), 60, 14, 3)
            pyxel.rectb(int(sign_x - 20), int(sign_y), 60, 14, 11)
            draw_text(int(sign_x - 16), int(sign_y + 2), "↑东校区", 7)
        
        # 下方指示牌（西校区方向）
        sign_y = 27 * TILE_SIZE - camera_y
        if 0 <= sign_y < WINDOW_HEIGHT:
            pyxel.rect(int(sign_x - 20), int(sign_y), 60, 14, 1)
            pyxel.rectb(int(sign_x - 20), int(sign_y), 60, 14, 12)
            draw_text(int(sign_x - 16), int(sign_y + 2), "↓西校区", 7)
        
        # 底部施工牌子（第27行，居中）
        sign_x = 10 * TILE_SIZE - camera_x
        sign_y = 27 * TILE_SIZE - camera_y
        
        if -30 < sign_x < WINDOW_WIDTH + 30 and -30 < sign_y < WINDOW_HEIGHT + 30:
            # 牌子立杆
            pyxel.rect(int(sign_x + 6), int(sign_y + 10), 4, 22, 4)
            # 牌子板
            pyxel.rect(int(sign_x - 20), int(sign_y), 56, 20, 8)
            pyxel.rectb(int(sign_x - 20), int(sign_y), 56, 20, 9)
            # 警告条纹
            for i in range(0, 56, 8):
                pyxel.line(int(sign_x - 20 + i), int(sign_y), int(sign_x - 20 + i + 4), int(sign_y + 6), 10)
            
    def is_collision(self, x, y, width, height):
        """检查碰撞"""
        corners = [
            (x, y),
            (x + width - 1, y),
            (x, y + height - 1),
            (x + width - 1, y + height - 1)
        ]
        
        for cx, cy in corners:
            tile_x = int(cx // TILE_SIZE)
            tile_y = int(cy // TILE_SIZE)
            
            if tile_x < 0 or tile_x >= TUNNEL_WIDTH or tile_y < 0 or tile_y >= TUNNEL_HEIGHT:
                return True
                
            if TUNNEL_COLLISION_MAP[tile_y][tile_x] == 1:
                return True
                
        return False
