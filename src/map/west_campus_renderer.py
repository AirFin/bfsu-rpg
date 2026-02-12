# -*- coding: utf-8 -*-
"""
西校区渲染器
绘制西校区地图（简化版：校门+空地）
"""

import pyxel
import math
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.map.campus_map import (
    WEST_CAMPUS_MAP, WEST_COLLISION_MAP, WEST_TREE_POSITIONS, WEST_GATE_POSITION,
    WEST_MAP_WIDTH, WEST_MAP_HEIGHT,
    TILE_GRASS, TILE_PATH, TILE_TREE, TILE_FENCE,
    TILE_GATE_PILLAR, TILE_GATE_TOP, TILE_GATE_PASS
)
from src.utils.font_manager import draw_text, text_width


class WestCampusRenderer:
    """西校区渲染器"""
    
    def __init__(self):
        """初始化"""
        self.time = 0
        self.current_weather = 'sunny'
        
        # 草地动画点
        self.grass_blades = []
        self._generate_grass_blades()
        
    def _generate_grass_blades(self):
        """生成草叶位置"""
        for y in range(WEST_MAP_HEIGHT):
            for x in range(WEST_MAP_WIDTH):
                tile = WEST_CAMPUS_MAP[y][x]
                if tile == TILE_GRASS:
                    for i in range(4):
                        px = x * TILE_SIZE + (i * 4) % TILE_SIZE
                        py = y * TILE_SIZE + ((i * 5 + 2) % TILE_SIZE)
                        phase = (x * 3 + y * 7 + i) % 100 / 10.0
                        self.grass_blades.append((px, py, phase))
                        
    def update(self, weather='sunny'):
        """更新动画"""
        self.time += 1
        self.current_weather = weather
        
    def draw(self, camera_x, camera_y):
        """绘制西校区"""
        # 计算可见范围
        start_tile_x = max(0, int(camera_x // TILE_SIZE) - 1)
        start_tile_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_tile_x = min(WEST_MAP_WIDTH, int((camera_x + WINDOW_WIDTH) // TILE_SIZE) + 2)
        end_tile_y = min(WEST_MAP_HEIGHT, int((camera_y + WINDOW_HEIGHT) // TILE_SIZE) + 2)
        
        # 绘制基础瓦片
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                self._draw_tile(x, y, camera_x, camera_y)
        
        # 绘制动态草叶
        self._draw_grass_animation(camera_x, camera_y)
        
        # 绘制树木
        for tx, ty in WEST_TREE_POSITIONS:
            screen_x = tx * TILE_SIZE - camera_x
            screen_y = ty * TILE_SIZE - camera_y
            if -TILE_SIZE < screen_x < WINDOW_WIDTH and -TILE_SIZE * 2 < screen_y < WINDOW_HEIGHT:
                self._draw_tree(screen_x, screen_y, tx + ty)
        
        # 绘制西校区校门
        self._draw_gate(camera_x, camera_y)
        
        # 绘制"西校区"标识
        self._draw_campus_sign(camera_x, camera_y)
                
    def _draw_tile(self, tile_x, tile_y, camera_x, camera_y):
        """绘制单个瓦片"""
        if tile_y < 0 or tile_y >= WEST_MAP_HEIGHT or tile_x < 0 or tile_x >= WEST_MAP_WIDTH:
            return
            
        tile = WEST_CAMPUS_MAP[tile_y][tile_x]
        screen_x = int(tile_x * TILE_SIZE - camera_x)
        screen_y = int(tile_y * TILE_SIZE - camera_y)
        
        if tile == TILE_GRASS:
            # 草地
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            seed = (tile_x * 7 + tile_y * 13) % 17
            if seed < 5:
                pyxel.pset(screen_x + seed, screen_y + (seed * 2) % TILE_SIZE, 11)
                
        elif tile == TILE_PATH:
            # 道路
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            seed = (tile_x + tile_y) % 5
            pyxel.pset(screen_x + 3 + seed, screen_y + 5, 6)
            
        elif tile == TILE_TREE:
            # 树底座
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            
        elif tile == TILE_FENCE:
            # 围栏
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            for i in range(4):
                fx = screen_x + 2 + i * 4
                pyxel.rect(fx, screen_y + 4, 2, 12, 7)
            pyxel.rect(screen_x, screen_y + 6, TILE_SIZE, 2, 7)
            pyxel.rect(screen_x, screen_y + 12, TILE_SIZE, 2, 7)
            for i in range(4):
                fx = screen_x + 2 + i * 4
                pyxel.tri(fx, screen_y + 4, fx + 2, screen_y + 4, fx + 1, screen_y + 2, 7)
                
        elif tile == TILE_GATE_PILLAR:
            # 校门柱子
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 2)
            for i in range(4):
                y_pos = screen_y + i * 4
                pyxel.line(screen_x, y_pos, screen_x + TILE_SIZE, y_pos, 4)
            pyxel.line(screen_x + 8, screen_y, screen_x + 8, screen_y + TILE_SIZE, 4)
            
        elif tile == TILE_GATE_TOP:
            # 校门顶部
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 2)
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE, screen_y + 4, 4)
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE, screen_y + 10, 4)
            
        elif tile == TILE_GATE_PASS:
            # 校门通道
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            pyxel.pset(screen_x + 4, screen_y + 8, 6)
            
    def _draw_grass_animation(self, camera_x, camera_y):
        """绘制动态草叶"""
        wind_speed = 0.015
        sway_amount = 1.2
        wind = math.sin(self.time * wind_speed)
        
        for px, py, phase in self.grass_blades:
            screen_x = px - camera_x
            screen_y = py - camera_y
            
            if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                sway = math.sin(self.time * (wind_speed * 1.5) + phase) * sway_amount * wind
                pyxel.line(
                    int(screen_x), int(screen_y + 3),
                    int(screen_x + sway), int(screen_y),
                    11
                )
    
    def _draw_tree(self, screen_x, screen_y, seed):
        """绘制树木"""
        trunk_x = screen_x + 5
        trunk_y = screen_y + 8
        pyxel.rect(trunk_x, trunk_y, 6, 8, 4)
        pyxel.line(trunk_x + 2, trunk_y, trunk_x + 2, trunk_y + 8, 9)
        
        crown_x = screen_x + 8
        crown_y = screen_y + 2
        pyxel.circ(crown_x, crown_y, 8, 3)
        pyxel.circ(crown_x - 5, crown_y + 2, 6, 3)
        pyxel.circ(crown_x + 5, crown_y + 2, 6, 3)
        pyxel.circ(crown_x - 2, crown_y - 3, 4, 11)
        pyxel.circ(crown_x + 3, crown_y - 1, 3, 11)
    
    def _draw_gate(self, camera_x, camera_y):
        """绘制西校区校门"""
        gate_left = WEST_GATE_POSITION['left_pillar_x'] * TILE_SIZE
        gate_right = (WEST_GATE_POSITION['right_pillar_x'] + 1) * TILE_SIZE
        gate_top = WEST_GATE_POSITION['top_y'] * TILE_SIZE
        
        screen_left = int(gate_left - camera_x)
        screen_right = int(gate_right - camera_x)
        screen_top = int(gate_top - camera_y)
        
        gate_width = gate_right - gate_left
        gate_center = (screen_left + screen_right) // 2
        
        if screen_right < -50 or screen_left > WINDOW_WIDTH + 50:
            return
        if screen_top > WINDOW_HEIGHT + 50 or screen_top < -100:
            return
        
        # 拱门主体（深红色）
        arch_y = screen_top - 32
        pyxel.rect(screen_left - 8, arch_y, gate_width + 16, 36, 2)
        pyxel.rectb(screen_left - 8, arch_y, gate_width + 16, 36, 4)
        pyxel.rectb(screen_left - 6, arch_y + 2, gate_width + 12, 32, 4)
        
        # 校徽
        badge_x = gate_center - 8
        badge_y = arch_y + 14
        pyxel.rect(badge_x, badge_y, 16, 18, 1)
        pyxel.tri(badge_x, badge_y + 18, badge_x + 16, badge_y + 18, badge_x + 8, badge_y + 24, 1)
        pyxel.rect(badge_x + 4, badge_y + 4, 8, 8, 7)
        
        # 校名
        school_name = "北外"
        name_w = text_width(school_name)
        draw_text(gate_center - name_w // 2, arch_y + 2, school_name, 7)
        
        # 柱子
        pillar_h = 48
        pyxel.rect(screen_left - 8, screen_top - 16, 20, pillar_h + 16, 2)
        for i in range(12):
            py = screen_top - 16 + i * 4
            pyxel.line(screen_left - 8, py, screen_left + 12, py, 4)
        
        right_pillar_x = screen_right - 12
        pyxel.rect(right_pillar_x, screen_top - 16, 20, pillar_h + 16, 2)
        for i in range(12):
            py = screen_top - 16 + i * 4
            pyxel.line(right_pillar_x, py, right_pillar_x + 20, py, 4)
        
        # 灯光
        light_phase = (self.time // 20) % 3
        if light_phase != 2:
            pyxel.circ(screen_left + 2, screen_top - 20, 4, 10)
            pyxel.pset(screen_left + 2, screen_top - 20, 7)
            pyxel.circ(right_pillar_x + 10, screen_top - 20, 4, 10)
            pyxel.pset(right_pillar_x + 10, screen_top - 20, 7)
    
    def _draw_campus_sign(self, camera_x, camera_y):
        """绘制西校区标识"""
        sign_x = 16 * TILE_SIZE - camera_x
        sign_y = 10 * TILE_SIZE - camera_y
        
        if -100 < sign_x < WINDOW_WIDTH + 100 and -50 < sign_y < WINDOW_HEIGHT + 50:
            # 大标识牌
            text = "西 校 区"
            tw = text_width(text)
            pyxel.rect(int(sign_x - tw // 2 - 10), int(sign_y - 5), tw + 20, 20, 2)
            pyxel.rectb(int(sign_x - tw // 2 - 10), int(sign_y - 5), tw + 20, 20, 4)
            draw_text(int(sign_x - tw // 2), int(sign_y), text, 7)
            
            # 建设中提示
            hint = "(建设中...)"
            hw = text_width(hint)
            draw_text(int(sign_x - hw // 2), int(sign_y + 24), hint, 6)
    
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
            
            if tile_x < 0 or tile_x >= WEST_MAP_WIDTH or tile_y < 0 or tile_y >= WEST_MAP_HEIGHT:
                return True
                
            if WEST_COLLISION_MAP[tile_y][tile_x] == 1:
                return True
                
        return False
