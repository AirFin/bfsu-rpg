# -*- coding: utf-8 -*-
"""
校园场景渲染器 - 精细版
绘制校园地图、草地、树木、校门、图书馆、金色圆顶建筑等
包含动态效果和精细像素艺术
北京外国语大学 (BFSU) 风格
"""

import pyxel
import math
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.font_manager import draw_text
from src.map.campus_map import (
    CAMPUS_MAP, COLLISION_MAP, TREE_POSITIONS, GATE_POSITION,
    TILE_GRASS, TILE_PATH, TILE_BUILDING, TILE_BUILDING_DOOR,
    TILE_PLAYGROUND, TILE_PLAYGROUND_GREEN, TILE_TREE, TILE_FLOWER,
    TILE_GATE_PILLAR, TILE_GATE_TOP, TILE_GATE_PASS, TILE_FENCE,
    TILE_WATER, TILE_BRIDGE, TILE_LIBRARY, TILE_LIBRARY_WINDOW,
    TILE_DOME, TILE_DOME_ARCH,
    TILE_CANTEEN, TILE_ADMIN, TILE_HALL, TILE_GYM, TILE_JAPAN, TILE_MAIN, TILE_PLAZA,
    TILE_MAIN_WING, TILE_MAIN_COURT,
    MAP_TILES_WIDTH, MAP_TILES_HEIGHT
)
from src.utils.font_manager import draw_text, text_width


class CampusRenderer:
    """校园场景渲染器"""
    
    def __init__(self):
        """初始化渲染器"""
        self.time = 0  # 用于动画计时
        self.current_weather = 'sunny'  # 当前天气
        
        # 草地动画点（随机分布的草叶）
        self.grass_blades = []
        self._generate_grass_blades()
        
    def _generate_grass_blades(self):
        """生成草叶位置"""
        for y in range(MAP_TILES_HEIGHT):
            for x in range(MAP_TILES_WIDTH):
                tile = CAMPUS_MAP[y][x]
                if tile == TILE_GRASS:
                    # 每个草地瓦片上放置4个草叶
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
        """绘制整个校园场景"""
        # 计算可见范围
        start_tile_x = max(0, int(camera_x // TILE_SIZE) - 1)
        start_tile_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_tile_x = min(MAP_TILES_WIDTH, int((camera_x + WINDOW_WIDTH) // TILE_SIZE) + 2)
        end_tile_y = min(MAP_TILES_HEIGHT, int((camera_y + WINDOW_HEIGHT) // TILE_SIZE) + 2)
        
        # 绘制基础瓦片
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                self._draw_tile(x, y, camera_x, camera_y)
        
        # 绘制椭圆形池塘
        self._draw_ellipse_pond(camera_x, camera_y)
                
        # 绘制动态草叶
        self._draw_grass_animation(camera_x, camera_y)
        
        # 绘制树木（带动画）
        for tx, ty in TREE_POSITIONS:
            screen_x = tx * TILE_SIZE - camera_x
            screen_y = ty * TILE_SIZE - camera_y
            if -TILE_SIZE < screen_x < WINDOW_WIDTH and -TILE_SIZE * 2 < screen_y < WINDOW_HEIGHT:
                self._draw_tree(screen_x, screen_y, tx + ty)
        
        # 绘制金色圆顶（上层装饰）
        self._draw_dome_top(camera_x, camera_y)
        
        # 绘制图书馆多语言文字塔装饰
        self._draw_library_tower(camera_x, camera_y)
        
        # 绘制日研中心顶部装饰和樱花树
        self._draw_japan_center(camera_x, camera_y)
        
        # 绘制主楼中国传统屋顶
        self._draw_main_building_roof(camera_x, camera_y)
        
        # 绘制校门（在最上层）
        self._draw_gate(camera_x, camera_y)
                
    def _draw_tile(self, tile_x, tile_y, camera_x, camera_y):
        """绘制单个瓦片"""
        if tile_y < 0 or tile_y >= MAP_TILES_HEIGHT or tile_x < 0 or tile_x >= MAP_TILES_WIDTH:
            return
            
        tile = CAMPUS_MAP[tile_y][tile_x]
        screen_x = int(tile_x * TILE_SIZE - camera_x)
        screen_y = int(tile_y * TILE_SIZE - camera_y)
        
        if tile == TILE_GRASS:
            # 草地 - 深绿色基底带纹理
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            # 随机浅色点缀
            seed = (tile_x * 7 + tile_y * 13) % 17
            if seed < 5:
                pyxel.pset(screen_x + seed, screen_y + (seed * 2) % TILE_SIZE, 11)
            if seed > 10:
                pyxel.pset(screen_x + 10, screen_y + seed % TILE_SIZE, 11)
                
        elif tile == TILE_PATH:
            # 沙土道路 - 米黄色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            # 道路纹理 - 小石子
            seed = (tile_x + tile_y) % 5
            pyxel.pset(screen_x + 3 + seed, screen_y + 5, 6)
            pyxel.pset(screen_x + 10, screen_y + 3 + seed, 6)
            pyxel.pset(screen_x + 7, screen_y + 11, 6)
            
        elif tile == TILE_BUILDING:
            # 教学楼 - 灰色/米色墙体
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 13)
            # 窗户
            pyxel.rect(screen_x + 2, screen_y + 2, 5, 6, 12)
            pyxel.rect(screen_x + 9, screen_y + 2, 5, 6, 12)
            # 窗框
            pyxel.line(screen_x + 4, screen_y + 2, screen_x + 4, screen_y + 7, 5)
            pyxel.line(screen_x + 11, screen_y + 2, screen_x + 11, screen_y + 7, 5)
            # 砖缝
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE, screen_y + 10, 5)
            pyxel.line(screen_x, screen_y + 14, screen_x + TILE_SIZE, screen_y + 14, 5)
            
        elif tile == TILE_BUILDING_DOOR:
            # 建筑门口
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 13)
            # 大门（棕色木门）
            pyxel.rect(screen_x + 3, screen_y, 10, 16, 4)
            pyxel.rect(screen_x + 4, screen_y + 1, 8, 14, 9)
            # 门把手
            pyxel.pset(screen_x + 10, screen_y + 8, 10)
            # 门顶装饰
            pyxel.line(screen_x + 2, screen_y, screen_x + 14, screen_y, 5)
            
        elif tile == TILE_PLAYGROUND:
            # 操场跑道 - 红色橡胶
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 8)
            # 跑道线
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE, screen_y + 4, 7)
            pyxel.line(screen_x, screen_y + 12, screen_x + TILE_SIZE, screen_y + 12, 7)
                
        elif tile == TILE_PLAYGROUND_GREEN:
            # 操场草坪 - 亮绿色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 11)
            # 草坪纹理
            if (tile_x + tile_y) % 2 == 0:
                pyxel.pset(screen_x + 5, screen_y + 5, 3)
                pyxel.pset(screen_x + 11, screen_y + 10, 3)
                
        elif tile == TILE_TREE:
            # 树木底部先画草地
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            
        elif tile == TILE_FLOWER:
            # 花坛
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)
            # 多彩花朵
            pyxel.pset(screen_x + 3, screen_y + 3, 8)
            pyxel.pset(screen_x + 7, screen_y + 5, 14)
            pyxel.pset(screen_x + 11, screen_y + 4, 10)
            pyxel.pset(screen_x + 5, screen_y + 10, 9)
            pyxel.pset(screen_x + 9, screen_y + 12, 8)
            
        elif tile == TILE_GATE_PILLAR:
            # 校门柱子 - 红砖色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 2)
            # 砖纹理
            for i in range(4):
                y_pos = screen_y + i * 4
                pyxel.line(screen_x, y_pos, screen_x + TILE_SIZE, y_pos, 4)
            pyxel.line(screen_x + 8, screen_y, screen_x + 8, screen_y + TILE_SIZE, 4)
            
        elif tile == TILE_GATE_TOP:
            # 校门顶部横梁
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 2)
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE, screen_y + 4, 4)
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE, screen_y + 10, 4)
            
        elif tile == TILE_GATE_PASS:
            # 校门通道 - 地面
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            pyxel.pset(screen_x + 4, screen_y + 8, 6)
            pyxel.pset(screen_x + 12, screen_y + 4, 6)
            
        elif tile == TILE_FENCE:
            # 白色栅栏
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 3)  # 草地背景
            # 白色栅栏柱
            for i in range(4):
                fx = screen_x + 2 + i * 4
                pyxel.rect(fx, screen_y + 4, 2, 12, 7)
            # 横杆
            pyxel.rect(screen_x, screen_y + 6, TILE_SIZE, 2, 7)
            pyxel.rect(screen_x, screen_y + 12, TILE_SIZE, 2, 7)
            # 栅栏顶部尖端
            for i in range(4):
                fx = screen_x + 2 + i * 4
                pyxel.tri(fx, screen_y + 4, fx + 2, screen_y + 4, fx + 1, screen_y + 2, 7)
            
        elif tile == TILE_WATER:
            # 水池瓦片 - 只绘制草地背景，椭圆池塘由 _draw_ellipse_pond 统一绘制
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 11)  # 草地底色
            
        elif tile == TILE_BRIDGE:
            # 小桥
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 4)  # 木桥
            # 桥面纹理
            pyxel.line(screen_x, screen_y + 3, screen_x + TILE_SIZE, screen_y + 3, 9)
            pyxel.line(screen_x, screen_y + 8, screen_x + TILE_SIZE, screen_y + 8, 9)
            pyxel.line(screen_x, screen_y + 13, screen_x + TILE_SIZE, screen_y + 13, 9)
            # 栏杆
            pyxel.rect(screen_x, screen_y, 2, TILE_SIZE, 9)
            pyxel.rect(screen_x + 14, screen_y, 2, TILE_SIZE, 9)
            
        elif tile == TILE_LIBRARY:
            # 图书馆建筑 - 参考北外图书馆的现代风格
            # 米灰色主体墙
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 6)
            # 横向百叶窗/遮阳板效果（深棕色条纹）
            for i in range(4):
                y_pos = screen_y + i * 4
                pyxel.rect(screen_x, y_pos, TILE_SIZE, 2, 4)
            # 窗户透光效果（浅色间隙）
            for i in range(4):
                y_pos = screen_y + 2 + i * 4
                pyxel.rect(screen_x + 1, y_pos, TILE_SIZE - 2, 2, 13)
            # 竖向分隔线
            pyxel.line(screen_x + 7, screen_y, screen_x + 7, screen_y + TILE_SIZE - 1, 5)
            
        elif tile == TILE_LIBRARY_WINDOW:
            # 图书馆大窗户区域 - 玻璃幕墙效果
            # 浅蓝色玻璃底
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 12)
            # 窗框（深色）
            pyxel.rectb(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 5)
            # 横向窗框分隔
            pyxel.line(screen_x, screen_y + 5, screen_x + TILE_SIZE - 1, screen_y + 5, 5)
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE - 1, screen_y + 10, 5)
            # 竖向窗框分隔
            pyxel.line(screen_x + 5, screen_y, screen_x + 5, screen_y + TILE_SIZE - 1, 5)
            pyxel.line(screen_x + 10, screen_y, screen_x + 10, screen_y + TILE_SIZE - 1, 5)
            # 玻璃反光效果
            pyxel.pset(screen_x + 2, screen_y + 2, 7)
            pyxel.pset(screen_x + 12, screen_y + 7, 7)
            
        elif tile == TILE_DOME:
            # 金色圆顶建筑主体（米色墙 + 精美装饰）
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            # 墙面装饰线（金色）
            pyxel.line(screen_x, screen_y + 4, screen_x + TILE_SIZE, screen_y + 4, 10)
            pyxel.line(screen_x, screen_y + 11, screen_x + TILE_SIZE, screen_y + 11, 10)
            # 伊斯兰风格几何图案
            pyxel.pset(screen_x + 4, screen_y + 7, 9)
            pyxel.pset(screen_x + 8, screen_y + 7, 9)
            pyxel.pset(screen_x + 12, screen_y + 7, 9)
            # 墙面纹理
            pyxel.pset(screen_x + 2, screen_y + 2, 7)
            pyxel.pset(screen_x + 10, screen_y + 14, 7)
            
        elif tile == TILE_DOME_ARCH:
            # 圆顶建筑拱门（精美版）
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 15)
            # 拱门外框（深棕色）
            pyxel.rect(screen_x + 2, screen_y, 12, 16, 4)
            # 拱形顶（金色装饰）
            pyxel.circ(screen_x + 8, screen_y + 2, 6, 9)
            pyxel.circ(screen_x + 8, screen_y + 3, 5, 10)
            # 门洞内部（深色）
            pyxel.rect(screen_x + 3, screen_y + 4, 10, 12, 1)
            # 拱门顶部装饰尖
            pyxel.tri(screen_x + 8, screen_y - 2, screen_x + 4, screen_y + 2, screen_x + 12, screen_y + 2, 10)
            
        elif tile == TILE_CANTEEN:
            # 食堂 - 暖色调
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 9)  # 橙色背景
            # 窗户
            pyxel.rect(screen_x + 2, screen_y + 3, 5, 5, 12)
            pyxel.rect(screen_x + 9, screen_y + 3, 5, 5, 12)
            # 横线装饰
            pyxel.line(screen_x, screen_y + 10, screen_x + TILE_SIZE, screen_y + 10, 4)
            pyxel.line(screen_x, screen_y + 14, screen_x + TILE_SIZE, screen_y + 14, 4)
            
        elif tile == TILE_ADMIN:
            # 行政楼 - 庄重灰色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 5)  # 深灰
            # 窗户（规整）
            pyxel.rect(screen_x + 2, screen_y + 2, 4, 5, 6)
            pyxel.rect(screen_x + 10, screen_y + 2, 4, 5, 6)
            # 砖纹
            pyxel.line(screen_x, screen_y + 9, screen_x + TILE_SIZE, screen_y + 9, 13)
            pyxel.line(screen_x, screen_y + 13, screen_x + TILE_SIZE, screen_y + 13, 13)
            
        elif tile == TILE_HALL:
            # 礼堂 - 红色典雅
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 2)  # 深红
            # 大窗户
            pyxel.rect(screen_x + 3, screen_y + 2, 10, 8, 1)
            # 窗格
            pyxel.line(screen_x + 8, screen_y + 2, screen_x + 8, screen_y + 10, 2)
            # 墙面装饰
            pyxel.line(screen_x, screen_y + 12, screen_x + TILE_SIZE, screen_y + 12, 4)
            
        elif tile == TILE_GYM:
            # 体育馆 - 蓝白色
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 6)  # 浅蓝
            # 弧形屋顶效果
            pyxel.line(screen_x + 2, screen_y + 2, screen_x + 14, screen_y + 2, 7)
            pyxel.line(screen_x + 1, screen_y + 4, screen_x + 15, screen_y + 4, 7)
            # 通风窗
            pyxel.rect(screen_x + 4, screen_y + 8, 3, 3, 12)
            pyxel.rect(screen_x + 9, screen_y + 8, 3, 3, 12)
            
        elif tile == TILE_JAPAN:
            # 日研中心 - 白色现代建筑风格（参考北外日本学研究中心）
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 7)  # 白色/浅灰
            # 深灰色垂直支柱（建筑特征）
            pyxel.rect(screen_x + 1, screen_y, 2, TILE_SIZE, 13)  # 左柱
            pyxel.rect(screen_x + 13, screen_y, 2, TILE_SIZE, 13)  # 右柱
            # 水平遮阳板（日式现代特色）
            pyxel.line(screen_x + 3, screen_y + 3, screen_x + 12, screen_y + 3, 5)
            pyxel.line(screen_x + 3, screen_y + 6, screen_x + 12, screen_y + 6, 5)
            pyxel.line(screen_x + 3, screen_y + 9, screen_x + 12, screen_y + 9, 5)
            pyxel.line(screen_x + 3, screen_y + 12, screen_x + 12, screen_y + 12, 5)
            # 玻璃窗（深蓝色）
            pyxel.rect(screen_x + 4, screen_y + 4, 3, 2, 1)
            pyxel.rect(screen_x + 9, screen_y + 4, 3, 2, 1)
            pyxel.rect(screen_x + 4, screen_y + 10, 3, 2, 1)
            pyxel.rect(screen_x + 9, screen_y + 10, 3, 2, 1)
            
        elif tile == TILE_MAIN:
            # 主楼主体 - 米白色墙面，中国传统风格
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 7)  # 白色墙面
            # 窗户（3列整齐排列）
            for wx in [2, 6, 10]:
                pyxel.rect(screen_x + wx, screen_y + 4, 3, 4, 1)   # 深蓝窗
                pyxel.rectb(screen_x + wx, screen_y + 4, 3, 4, 5)  # 灰色窗框
            # 底部墙裙（略深色）
            pyxel.rect(screen_x, screen_y + 11, TILE_SIZE, 5, 6)
            
        elif tile == TILE_MAIN_WING:
            # 主楼侧翼 - 白色墙面带窗
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 7)  # 白色墙面
            # 侧翼窗户（2列）
            for wx in [3, 9]:
                pyxel.rect(screen_x + wx, screen_y + 4, 3, 4, 1)   # 深蓝窗
                pyxel.rectb(screen_x + wx, screen_y + 4, 3, 4, 5)  # 窗框
            # 底部墙裙
            pyxel.rect(screen_x, screen_y + 11, TILE_SIZE, 5, 6)
            
        elif tile == TILE_MAIN_COURT:
            # 主楼庭院 - 浅灰色地砖（中式庭院地面）
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 6)  # 浅灰地面
            # 地砖纹理（细格子）
            for i in range(4):
                pyxel.line(screen_x + i*4, screen_y, screen_x + i*4, screen_y + TILE_SIZE - 1, 5)
                pyxel.line(screen_x, screen_y + i*4, screen_x + TILE_SIZE - 1, screen_y + i*4, 5)
            # 中心装饰
            pyxel.pset(screen_x + 8, screen_y + 8, 13)
            
        elif tile == TILE_PLAZA:
            # 小广场地砖
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 6)  # 浅灰蓝
            # 地砖纹理（格子）
            pyxel.line(screen_x + 8, screen_y, screen_x + 8, screen_y + TILE_SIZE, 5)
            pyxel.line(screen_x, screen_y + 8, screen_x + TILE_SIZE, screen_y + 8, 5)
    
    def _draw_ellipse_pond(self, camera_x, camera_y):
        """绘制椭圆形池塘"""
        # 池塘中心（像素坐标）
        pond_center_x = 27.5 * TILE_SIZE  # 列24-31的中心
        pond_center_y = 10.5 * TILE_SIZE  # 行9-12的中心
        
        # 椭圆半轴
        radius_x = 3.5 * TILE_SIZE  # 水平半径
        radius_y = 2.0 * TILE_SIZE  # 垂直半径
        
        # 转换为屏幕坐标
        screen_cx = pond_center_x - camera_x
        screen_cy = pond_center_y - camera_y
        
        # 检查池塘是否在可见范围内
        if (screen_cx + radius_x < -20 or screen_cx - radius_x > WINDOW_WIDTH + 20 or
            screen_cy + radius_y < -20 or screen_cy - radius_y > WINDOW_HEIGHT + 20):
            return
        
        # 绘制椭圆形池塘（用多个同心椭圆填充）
        # 外边缘（深色边框）
        pyxel.elli(int(screen_cx - radius_x), int(screen_cy - radius_y),
                   int(radius_x * 2), int(radius_y * 2), 1)
        
        # 主体（浅蓝色）
        inner_rx = radius_x - 2
        inner_ry = radius_y - 2
        pyxel.elli(int(screen_cx - inner_rx), int(screen_cy - inner_ry),
                   int(inner_rx * 2), int(inner_ry * 2), 12)
        
        # 绘制波纹动画
        wave = math.sin(self.time * 0.08) * 2
        for i in range(3):
            wave_offset = math.sin(self.time * 0.06 + i * 1.5) * 3
            wy = screen_cy - radius_y * 0.5 + i * 10 + int(wave)
            # 计算波纹在该y位置的宽度（椭圆形）
            if abs(wy - screen_cy) < radius_y - 4:
                # 椭圆方程计算x范围
                t = (wy - screen_cy) / (radius_y - 4)
                if abs(t) <= 1:
                    half_width = (radius_x - 6) * math.sqrt(1 - t * t)
                    pyxel.line(int(screen_cx - half_width + wave_offset), int(wy),
                              int(screen_cx + half_width + wave_offset), int(wy), 6)
            
    def _draw_grass_animation(self, camera_x, camera_y):
        """绘制动态草叶（根据天气变化）"""
        # 根据天气调整摆动速度
        if self.current_weather == 'sunny':
            # 晴天 - 缓慢摆动
            wind_speed = 0.015
            sway_amount = 1.2
        elif self.current_weather == 'rain':
            # 雨天 - 快速摆动
            wind_speed = 0.08
            sway_amount = 2.5
        else:
            # 雪天 - 不摆动
            wind_speed = 0
            sway_amount = 0
        
        wind = math.sin(self.time * wind_speed) if wind_speed > 0 else 0
        
        for px, py, phase in self.grass_blades:
            screen_x = px - camera_x
            screen_y = py - camera_y
            
            if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                if self.current_weather == 'snow':
                    # 雪天 - 草叶不摆动，并有积雪
                    # 绿色草叶
                    pyxel.line(
                        int(screen_x), int(screen_y + 3),
                        int(screen_x), int(screen_y),
                        11
                    )
                    # 白色积雪（草叶顶部）
                    pyxel.pset(int(screen_x), int(screen_y), 7)
                    pyxel.pset(int(screen_x), int(screen_y + 1), 7)
                else:
                    # 晴天/雨天 - 草叶摆动
                    sway = math.sin(self.time * (wind_speed * 1.5) + phase) * sway_amount * wind
                    pyxel.line(
                        int(screen_x), int(screen_y + 3),
                        int(screen_x + sway), int(screen_y),
                        11
                    )
                
    def _draw_tree(self, screen_x, screen_y, seed):
        """绘制大树（圆形树冠，无动画）"""
        # 树干（棕色，带纹理）
        trunk_x = screen_x + 5
        trunk_y = screen_y + 8
        pyxel.rect(trunk_x, trunk_y, 6, 8, 4)
        pyxel.line(trunk_x + 2, trunk_y, trunk_x + 2, trunk_y + 8, 9)
        
        # 圆形树冠
        crown_x = screen_x + 8
        crown_y = screen_y + 2
        
        # 主树冠（大圆）
        pyxel.circ(crown_x, crown_y, 8, 3)
        # 左侧树冠
        pyxel.circ(crown_x - 5, crown_y + 2, 6, 3)
        # 右侧树冠
        pyxel.circ(crown_x + 5, crown_y + 2, 6, 3)
        
        # 浅绿色高光
        pyxel.circ(crown_x - 2, crown_y - 3, 4, 11)
        pyxel.circ(crown_x + 3, crown_y - 1, 3, 11)
        
        # 细节点缀
        pyxel.pset(crown_x - 4, crown_y - 2, 11)
        pyxel.pset(crown_x + 2, crown_y - 4, 11)
        
    def _draw_tree_layer(self, cx, y, width, color, sway):
        """绘制树的一层"""
        cx = int(cx + sway)
        half_w = width // 2
        # 三角形树冠
        pyxel.tri(
            cx - half_w, int(y + 6),
            cx + half_w, int(y + 6),
            cx, int(y),
            color
        )
    
    def _draw_library_tower(self, camera_x, camera_y):
        """绘制图书馆左侧的多语言文字塔 - 北外图书馆标志性设计"""
        # 图书馆位置（根据地图：第8-11行，x=12-19，已扩大）
        lib_x = 12 * TILE_SIZE
        lib_y = 8 * TILE_SIZE  # 从第8行开始
        lib_height = 4 * TILE_SIZE  # 4行高
        lib_width = 8 * TILE_SIZE   # 8列宽
        
        screen_x = lib_x - camera_x
        screen_y = lib_y - camera_y
        
        # 检查是否在可视范围内
        if screen_x > WINDOW_WIDTH + 50 or screen_x < -180:
            return
        if screen_y > WINDOW_HEIGHT + 50 or screen_y < -100:
            return
        
        # === 文字塔（在图书馆左侧，紧贴图书馆建筑） ===
        tower_width = 20
        tower_height = lib_height + 24  # 比图书馆高一些
        tower_x = int(screen_x) - tower_width  # 在图书馆左侧
        tower_y = int(screen_y - 24)  # 向上延伸
        
        # 塔身底色（米灰色）
        pyxel.rect(tower_x, tower_y, tower_width, tower_height, 6)
        
        # 塔身内层边框（浅色装饰）
        pyxel.rectb(tower_x + 2, tower_y + 2, tower_width - 4, tower_height - 4, 13)
        
        # 塔边框（深色）
        pyxel.rectb(tower_x, tower_y, tower_width, tower_height, 5)
        
        # 竖排绘制 "图书馆" 三个中文字（居中）
        text_x = tower_x + 4
        draw_text(text_x, tower_y + 12, "图", 5)   # 深灰色文字
        draw_text(text_x, tower_y + 32, "书", 5)
        draw_text(text_x, tower_y + 52, "馆", 5)
        
        # 塔顶装饰（平顶设计，深棕色横条）
        pyxel.rect(tower_x - 2, tower_y - 4, tower_width + 4, 5, 4)
        pyxel.line(tower_x, tower_y - 2, tower_x + tower_width - 1, tower_y - 2, 9)
        # 平顶上的小装饰
        pyxel.rect(tower_x + 4, tower_y - 7, tower_width - 8, 4, 5)
        pyxel.rect(tower_x + 6, tower_y - 6, tower_width - 12, 2, 6)
        
        # === 图书馆主楼顶部装饰 ===
        roof_y = int(screen_y - 10)
        roof_width = lib_width
        
        # 屋顶主体（深棕色）
        pyxel.rect(int(screen_x), roof_y, roof_width, 12, 4)
        
        # 屋顶横线装饰
        pyxel.line(int(screen_x) + 2, roof_y + 3, int(screen_x) + roof_width - 3, roof_y + 3, 9)
        pyxel.line(int(screen_x) + 2, roof_y + 6, int(screen_x) + roof_width - 3, roof_y + 6, 9)
        pyxel.line(int(screen_x) + 2, roof_y + 9, int(screen_x) + roof_width - 3, roof_y + 9, 9)
        
        # 屋顶边缘装饰（深色边线）
        pyxel.rect(int(screen_x), roof_y - 3, roof_width, 4, 5)
        
        # 屋顶上的小装饰（类似通风口）
        for i in range(3):
            dx = int(screen_x) + 20 + i * 35
            if dx < int(screen_x) + roof_width - 10:
                pyxel.rect(dx, roof_y - 6, 8, 4, 5)
                pyxel.rect(dx + 1, roof_y - 5, 6, 2, 6)
        
        # === 图书馆底部装饰（台阶和入口装饰） ===
        base_y = int(screen_y) + lib_height
        # 入口台阶（只在左侧门的位置 x=14，即第3列）
        door1_x = int(screen_x) + 2 * TILE_SIZE  # x=14的位置
        
        # 台阶装饰
        pyxel.rect(door1_x - 4, base_y, TILE_SIZE + 8, 3, 6)
        pyxel.rect(door1_x - 2, base_y + 3, TILE_SIZE + 4, 2, 13)
        
        # === 右下角横向"图书馆"标识（小字） ===
        sign_x = int(screen_x) + lib_width - 52  # 右下角位置
        sign_y = int(screen_y) + lib_height - 18  # 靠近底部但在建筑内
        
        # 小型标识背景（完整覆盖文字，高度16像素）
        pyxel.rect(sign_x - 2, sign_y - 2, 48, 16, 6)
        pyxel.rectb(sign_x - 2, sign_y - 2, 48, 16, 5)
        
        # 横向小字 "图书馆"
        draw_text(sign_x, sign_y, "图", 5)
        draw_text(sign_x + 14, sign_y, "书", 5)
        draw_text(sign_x + 28, sign_y, "馆", 5)
        
    def _draw_dome_top(self, camera_x, camera_y):
        """绘制清真寺穹顶 - 简洁风格，单一金色圆顶"""
        # 清真寺位置（根据新地图：第1-4行，x=10-14）
        dome_x = 10 * TILE_SIZE
        dome_y = 1 * TILE_SIZE
        
        screen_x = dome_x - camera_x
        screen_y = dome_y - camera_y
        
        # 检查是否在可视范围内
        if screen_x > WINDOW_WIDTH + 50 or screen_x < -100:
            return
        if screen_y > WINDOW_HEIGHT + 50 or screen_y < -60:
            return
        
        # 建筑宽度 5 个瓦片（x=10-14）
        building_width = 5 * TILE_SIZE
        center_x = int(screen_x + building_width // 2)
        
        # === 单一金色圆顶 ===
        dome_top_y = int(screen_y - 20)
        
        # 圆顶主体（金色，从下往上画）
        pyxel.circ(center_x, dome_top_y + 15, 22, 4)   # 深色底边
        pyxel.circ(center_x, dome_top_y + 12, 20, 9)   # 橙色
        pyxel.circ(center_x, dome_top_y + 8, 17, 10)   # 金黄色
        pyxel.circ(center_x - 4, dome_top_y + 4, 10, 10)  # 高光
        
        # 顶端尖塔和新月
        pyxel.rect(center_x - 1, dome_top_y - 12, 3, 14, 10)  # 尖塔
        # 新月符号
        pyxel.circ(center_x, dome_top_y - 16, 5, 10)
        pyxel.circ(center_x + 2, dome_top_y - 16, 4, 1)  # 遮挡形成新月
        
        # 闪光效果
        if (self.time // 25) % 3 == 0:
            pyxel.pset(center_x, dome_top_y - 14, 7)
            pyxel.pset(center_x - 8, dome_top_y + 2, 7)
        
    def _draw_japan_center(self, camera_x, camera_y):
        """绘制日研中心顶部装饰和樱花树"""
        # 日研中心位置（根据地图：第21-23行，x=29-33）
        jp_x = 29 * TILE_SIZE
        jp_y = 21 * TILE_SIZE
        
        screen_x = jp_x - camera_x
        screen_y = jp_y - camera_y
        
        # 检查是否在可视范围内
        if screen_x > WINDOW_WIDTH + 100 or screen_x < -150:
            return
        if screen_y > WINDOW_HEIGHT + 50 or screen_y < -80:
            return
        
        # 建筑宽度 5 个瓦片
        building_width = 5 * TILE_SIZE
        center_x = int(screen_x + building_width // 2)
        
        # === 顶部檐篷装饰（深色遮阳结构）===
        canopy_y = int(screen_y - 8)
        # 深灰色大檐篷
        pyxel.rect(int(screen_x - 4), canopy_y, building_width + 8, 6, 5)
        # 底部阴影线
        pyxel.line(int(screen_x - 4), canopy_y + 5, int(screen_x + building_width + 4), canopy_y + 5, 1)
        
        # === 招牌区域（金色字）===
        sign_y = canopy_y - 12
        # 米色招牌背景
        pyxel.rect(int(screen_x + 10), sign_y, building_width - 20, 10, 15)
        # 金色文字框
        pyxel.rectb(int(screen_x + 10), sign_y, building_width - 20, 10, 10)
        
        # === 樱花树（左侧）===
        sakura_x1 = int(screen_x - 30)
        sakura_y1 = int(screen_y - 10)
        self._draw_sakura_tree(sakura_x1, sakura_y1, 0)
        
        # === 樱花树（右侧）===
        sakura_x2 = int(screen_x + building_width + 10)
        sakura_y2 = int(screen_y - 5)
        self._draw_sakura_tree(sakura_x2, sakura_y2, 1)
        
        # === 飘落的樱花花瓣 ===
        self._draw_falling_petals(int(screen_x - 40), int(screen_y - 40), 120, 100)
    
    def _draw_sakura_tree(self, x, y, seed):
        """绘制樱花树"""
        # 树干（深棕色）
        trunk_x = x + 8
        trunk_y = y + 18
        pyxel.rect(trunk_x, trunk_y, 5, 14, 4)
        pyxel.line(trunk_x + 2, trunk_y, trunk_x + 2, trunk_y + 14, 9)
        
        # 樱花树冠（粉色）
        crown_x = x + 10
        crown_y = y + 8
        
        # 主树冠（多层粉色）
        pyxel.circ(crown_x, crown_y, 12, 14)  # 深粉色底
        pyxel.circ(crown_x - 6, crown_y + 3, 8, 14)  # 左侧
        pyxel.circ(crown_x + 6, crown_y + 3, 8, 14)  # 右侧
        pyxel.circ(crown_x, crown_y + 6, 9, 14)  # 底部
        
        # 浅粉色高光
        pyxel.circ(crown_x - 3, crown_y - 4, 6, 8)   # 浅粉（用红色8模拟）
        pyxel.circ(crown_x + 4, crown_y - 2, 5, 8)
        
        # 白色花朵点缀
        petal_offset = (self.time // 10 + seed * 5) % 6
        pyxel.pset(crown_x - 5 + petal_offset, crown_y - 3, 7)
        pyxel.pset(crown_x + 3, crown_y - 5 + (petal_offset % 3), 7)
        pyxel.pset(crown_x - 2 + (petal_offset % 4), crown_y + 2, 7)
        pyxel.pset(crown_x + 5 - (petal_offset % 3), crown_y, 7)
        pyxel.pset(crown_x - 7, crown_y + 1, 7)
        pyxel.pset(crown_x + 8, crown_y + 2, 7)
    
    def _draw_falling_petals(self, start_x, start_y, width, height):
        """绘制飘落的樱花花瓣"""
        # 多个花瓣，随时间飘动
        for i in range(8):
            # 基于时间和索引计算位置
            t = self.time * 0.02 + i * 0.8
            px = start_x + (i * 17 + int(math.sin(t * 2) * 15)) % width
            py = start_y + (int(t * 20 + i * 12) % height)
            
            # 花瓣颜色（粉白交替）
            color = 14 if i % 2 == 0 else 7
            
            # 绘制小花瓣（1-2像素）
            pyxel.pset(int(px), int(py), color)
            if i % 3 == 0:
                pyxel.pset(int(px) + 1, int(py), color)

    def _draw_main_building_roof(self, camera_x, camera_y):
        """绘制主楼的中国传统风格屋顶"""
        # 主楼位置：行30-32，列4-14（U形布局）
        # 左翼：列4-5，中央主体：列6-12，右翼：列13-14
        
        main_y = 30 * TILE_SIZE  # 主楼顶部行
        left_wing_x = 4 * TILE_SIZE
        right_wing_x = 13 * TILE_SIZE
        center_x = 6 * TILE_SIZE
        
        # 屏幕坐标转换
        screen_main_y = int(main_y - camera_y)
        screen_left_x = int(left_wing_x - camera_x)
        screen_right_x = int(right_wing_x - camera_x)
        screen_center_x = int(center_x - camera_x)
        
        # 检查是否在可视范围内
        if screen_main_y > WINDOW_HEIGHT + 50 or screen_main_y < -100:
            return
        if screen_right_x + 64 < 0 or screen_left_x > WINDOW_WIDTH + 50:
            return
        
        # === 主楼中央大屋顶（跨越列6-12，7个瓦片宽度）===
        center_width = 7 * TILE_SIZE  # 112像素
        roof_height = 16
        roof_top = screen_main_y - roof_height
        
        # 深灰色主屋顶（中国传统瓦顶）
        pyxel.rect(screen_center_x - 4, roof_top, center_width + 8, roof_height, 5)
        
        # 屋顶瓦片纹理（横向线条模拟瓦片）
        for i in range(1, roof_height, 3):
            pyxel.line(screen_center_x - 4, roof_top + i, 
                      screen_center_x + center_width + 4, roof_top + i, 13)
        
        # 屋脊（顶部亮线）
        pyxel.rect(screen_center_x, roof_top - 3, center_width, 3, 13)
        pyxel.line(screen_center_x, roof_top - 3, 
                  screen_center_x + center_width, roof_top - 3, 7)
        
        # 飞檐效果（两侧向上翘）
        # 左侧飞檐
        pyxel.line(screen_center_x - 6, roof_top + roof_height - 2,
                   screen_center_x - 10, roof_top + roof_height - 6, 5)
        pyxel.line(screen_center_x - 6, roof_top + roof_height - 3,
                   screen_center_x - 9, roof_top + roof_height - 6, 13)
        # 右侧飞檐
        pyxel.line(screen_center_x + center_width + 6, roof_top + roof_height - 2,
                   screen_center_x + center_width + 10, roof_top + roof_height - 6, 5)
        pyxel.line(screen_center_x + center_width + 6, roof_top + roof_height - 3,
                   screen_center_x + center_width + 9, roof_top + roof_height - 6, 13)
        
        # 檐下阴影
        pyxel.rect(screen_center_x - 4, roof_top + roof_height, center_width + 8, 2, 1)
        
        # === 左翼屋顶（列4-5，2个瓦片宽度）===
        wing_width = 2 * TILE_SIZE  # 32像素
        wing_roof_height = 12
        wing_roof_top = screen_main_y - wing_roof_height
        
        # 左翼屋顶
        pyxel.rect(screen_left_x - 2, wing_roof_top, wing_width + 4, wing_roof_height, 5)
        # 瓦片纹理
        for i in range(1, wing_roof_height, 3):
            pyxel.line(screen_left_x - 2, wing_roof_top + i,
                       screen_left_x + wing_width + 2, wing_roof_top + i, 13)
        # 屋脊
        pyxel.rect(screen_left_x, wing_roof_top - 2, wing_width, 2, 13)
        # 飞檐
        pyxel.line(screen_left_x - 4, wing_roof_top + wing_roof_height - 2,
                   screen_left_x - 7, wing_roof_top + wing_roof_height - 5, 5)
        
        # === 右翼屋顶（列13-14，2个瓦片宽度）===
        # 右翼屋顶
        pyxel.rect(screen_right_x - 2, wing_roof_top, wing_width + 4, wing_roof_height, 5)
        # 瓦片纹理
        for i in range(1, wing_roof_height, 3):
            pyxel.line(screen_right_x - 2, wing_roof_top + i,
                       screen_right_x + wing_width + 2, wing_roof_top + i, 13)
        # 屋脊
        pyxel.rect(screen_right_x, wing_roof_top - 2, wing_width, 2, 13)
        # 飞檐
        pyxel.line(screen_right_x + wing_width + 4, wing_roof_top + wing_roof_height - 2,
                   screen_right_x + wing_width + 7, wing_roof_top + wing_roof_height - 5, 5)
        
        # === 主入口装饰（中央正门）===
        entrance_x = screen_center_x + center_width // 2 - 12
        entrance_y = screen_main_y + 2 * TILE_SIZE  # 第32行
        
        # 入口顶部牌匾
        pyxel.rect(entrance_x - 4, entrance_y - 14, 30, 10, 2)  # 红色牌匾
        pyxel.rectb(entrance_x - 4, entrance_y - 14, 30, 10, 4)  # 深红边框
        
        # 门口台阶（浅灰色）
        pyxel.rect(entrance_x - 2, entrance_y + 8, 28, 4, 6)
        pyxel.line(entrance_x - 2, entrance_y + 8, entrance_x + 26, entrance_y + 8, 13)

    def _draw_gate(self, camera_x, camera_y):
        """绘制北外校门 - 精细版红砖拱门"""
        gate_left = GATE_POSITION['left_pillar_x'] * TILE_SIZE
        gate_right = (GATE_POSITION['right_pillar_x'] + 1) * TILE_SIZE
        gate_top = GATE_POSITION['top_y'] * TILE_SIZE
        
        screen_left = int(gate_left - camera_x)
        screen_right = int(gate_right - camera_x)
        screen_top = int(gate_top - camera_y)
        
        gate_width = gate_right - gate_left
        gate_center = (screen_left + screen_right) // 2
        
        if screen_right < -50 or screen_left > WINDOW_WIDTH + 50:
            return
        if screen_top > WINDOW_HEIGHT + 50 or screen_top < -100:
            return
            
        # === 拱门主体 ===
        arch_y = screen_top - 32
        
        # 门楣背景（深红色）
        pyxel.rect(screen_left - 8, arch_y, gate_width + 16, 36, 2)
        
        # 装饰边框
        pyxel.rectb(screen_left - 8, arch_y, gate_width + 16, 36, 4)
        pyxel.rectb(screen_left - 6, arch_y + 2, gate_width + 12, 32, 4)
        
        # 拱形底部
        for i in range(int(gate_width + 16)):
            x = screen_left - 8 + i
            progress = (i - (gate_width + 16) / 2) / ((gate_width + 16) / 2)
            curve = int(12 * (1 - progress * progress))
            if curve > 0:
                pyxel.rect(x, arch_y + 28 + curve, 1, 8, 2)
        
        # === 校名文字 ===
        # "北京外国语大学" 
        text_x = gate_center - 40
        text_y = arch_y + 6
        
        # 模拟中文 "北京外国语大学" (使用矩形块模拟汉字)
        # 现在使用自定义字体显示中文
        
        # 校徽（盾形 - 蓝白色）
        badge_x = gate_center - 8
        badge_y = arch_y + 14
        pyxel.rect(badge_x, badge_y, 16, 18, 1)  # 蓝色盾底
        pyxel.tri(badge_x, badge_y + 18, badge_x + 16, badge_y + 18, 
                  badge_x + 8, badge_y + 24, 1)  # 盾形底部
        pyxel.rect(badge_x + 4, badge_y + 4, 8, 8, 7)  # 白色内部
        
        # 校名（中文）
        school_name = "北外"
        name_w = text_width(school_name)
        draw_text(gate_center - name_w // 2, arch_y + 2, school_name, 7)
        
        # === 柱子 ===
        pillar_h = 48
        
        # 左柱子
        pyxel.rect(screen_left - 8, screen_top - 16, 20, pillar_h + 16, 2)
        # 砖纹
        for i in range(12):
            py = screen_top - 16 + i * 4
            pyxel.line(screen_left - 8, py, screen_left + 12, py, 4)
        # 攀爬植物
        vine_sway = math.sin(self.time * 0.02) * 1
        for i in range(6):
            vy = screen_top - 10 + i * 7
            pyxel.pset(int(screen_left - 4 + vine_sway), vy, 3)
            pyxel.pset(int(screen_left - 2 + vine_sway * 0.5), vy + 3, 11)
        
        # 右柱子
        right_pillar_x = screen_right - 12
        pyxel.rect(right_pillar_x, screen_top - 16, 20, pillar_h + 16, 2)
        for i in range(12):
            py = screen_top - 16 + i * 4
            pyxel.line(right_pillar_x, py, right_pillar_x + 20, py, 4)
        
        # === 灯光 ===
        light_phase = (self.time // 20) % 3
        if light_phase != 2:
            # 左灯
            pyxel.circ(screen_left + 2, screen_top - 20, 4, 10)
            pyxel.pset(screen_left + 2, screen_top - 20, 7)
            # 右灯
            pyxel.circ(right_pillar_x + 10, screen_top - 20, 4, 10)
            pyxel.pset(right_pillar_x + 10, screen_top - 20, 7)
        
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
            
            if tile_x < 0 or tile_x >= MAP_TILES_WIDTH or tile_y < 0 or tile_y >= MAP_TILES_HEIGHT:
                return True
                
            if COLLISION_MAP[tile_y][tile_x] == 1:
                return True
                
        return False
