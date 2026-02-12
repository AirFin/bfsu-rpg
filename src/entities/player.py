# -*- coding: utf-8 -*-
"""
玩家角色类
"""

import pyxel
from config import (
    PLAYER_SPEED, PLAYER_MAX_HP, TILE_SIZE
)
from src.map.campus_map import PLAYER_START_TILE_X, PLAYER_START_TILE_Y, MAP_TILES_WIDTH, MAP_TILES_HEIGHT
from src.systems.input_handler import InputHandler


class Player:
    """玩家类"""
    
    # 肤色映射
    SKIN_COLORS = {
        'yellow': 15,  # 浅黄肤色
        'white': 7,    # 白色
        'brown': 4,    # 棕色
        'black': 1     # 深色
    }
    
    def __init__(self, collision_checker=None, player_data=None):
        """初始化玩家"""
        # 从瓦片坐标计算像素坐标
        self.x = PLAYER_START_TILE_X * TILE_SIZE
        self.y = PLAYER_START_TILE_Y * TILE_SIZE
        self.width = 12  # 玩家碰撞框稍小于瓦片
        self.height = 14
        self.speed = PLAYER_SPEED
        
        # 碰撞检测器
        self.collision_checker = collision_checker
        
        # 玩家自定义数据
        if player_data:
            self.name = player_data.get('name', 'SharkFin')
            self.gender = player_data.get('gender', 'male')
            self.skin_color_name = player_data.get('skin_color', 'yellow')
        else:
            self.name = 'SharkFin'
            self.gender = 'male'
            self.skin_color_name = 'yellow'
            
        self.skin_color = self.SKIN_COLORS.get(self.skin_color_name, 15)
        self.cloth_color = 12 if self.gender == 'male' else 14  # 男蓝，女粉
        self.hair_color = 0 if self.gender == 'male' else 4     # 男黑发，女棕发
        self.is_male = self.gender == 'male'
        
        # 状态
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.direction = "down"  # up, down, left, right
        
        # 滑板模式
        self.has_skateboard = False  # 是否拥有滑板
        self.skateboard_mode = False  # 是否在使用滑板
        self.base_speed = PLAYER_SPEED  # 基础速度
        self.skateboard_speed = PLAYER_SPEED * 1.2  # 滑板速度（1.2倍）
        
        # 动画
        self.frame = 0
        self.anim_timer = 0
        self.is_moving = False
        
    def update(self):
        """更新玩家状态"""
        # B键切换滑板模式
        if InputHandler.is_just_pressed(InputHandler.SKATE_TOGGLE) and self.has_skateboard:
            self.skateboard_mode = not self.skateboard_mode
            if self.skateboard_mode:
                self.speed = self.skateboard_speed
            else:
                self.speed = self.base_speed
        
        # 处理输入（键盘 + 手柄）
        move_x, move_y = InputHandler.get_movement()
        dx = move_x * self.speed
        dy = move_y * self.speed

        if abs(move_x) > 0.001 or abs(move_y) > 0.001:
            if abs(move_x) > abs(move_y):
                self.direction = "right" if move_x > 0 else "left"
            else:
                self.direction = "down" if move_y > 0 else "up"

        self.is_moving = abs(dx) > 0.001 or abs(dy) > 0.001
        
        # 尝试移动（带碰撞检测）
        if dx != 0:
            new_x = self.x + dx
            if not self._check_collision(new_x, self.y):
                self.x = new_x
                
        if dy != 0:
            new_y = self.y + dy
            if not self._check_collision(self.x, new_y):
                self.y = new_y
        
        # 地图边界限制
        max_x = MAP_TILES_WIDTH * TILE_SIZE - self.width
        max_y = MAP_TILES_HEIGHT * TILE_SIZE - self.height
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
        
        # 动画更新
        if self.is_moving:
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.frame = (self.frame + 1) % 4
        else:
            self.frame = 0
            self.anim_timer = 0
            
    def _check_collision(self, x, y):
        """检查碰撞"""
        if self.collision_checker:
            return self.collision_checker(x + 2, y + 2, self.width - 4, self.height - 4)
        return False
            
    def draw(self, camera_x=0, camera_y=0):
        """绘制玩家"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 滑板模式下绘制滑板动画
        if self.skateboard_mode:
            self._draw_skateboard_character(screen_x, screen_y)
        else:
            # 绘制玩家身体
            self._draw_character(screen_x, screen_y)
        
    def _draw_skateboard_character(self, x, y):
        """绘制滑滑板的角色"""
        skin = self.skin_color
        cloth = self.cloth_color
        hair = self.hair_color
        
        # 滑板左右摇晃动画
        sway = 0
        if self.is_moving:
            # 滑行时轻微左右摇晃
            if self.frame in [1, 3]:
                sway = 1
            else:
                sway = -1
        
        # 根据方向绘制
        if self.direction in ["left", "right"]:
            # 侧面滑行姿势
            # 滑板
            pyxel.rect(x, y + 12, 12, 3, 4)  # 棕色板身
            pyxel.rect(x + 1, y + 13, 10, 1, 15)  # 浅色条纹
            pyxel.pset(x + 2, y + 15, 0)  # 左轮
            pyxel.pset(x + 9, y + 15, 0)  # 右轮
            
            # 身体（略微弯曲）
            body_y = y + sway
            # 头发
            pyxel.rect(x + 4, body_y - 1, 5, 3, hair)
            # 头部
            pyxel.rect(x + 4, body_y + 1, 5, 4, skin)
            # 眼睛
            if self.direction == "right":
                pyxel.pset(x + 7, body_y + 3, 0)
            else:
                pyxel.pset(x + 5, body_y + 3, 0)
            # 身体
            pyxel.rect(x + 3, body_y + 5, 6, 5, cloth)
            # 手臂（向前伸展保持平衡）
            if self.direction == "right":
                pyxel.rect(x + 8, body_y + 5, 3, 2, skin)
                pyxel.rect(x + 1, body_y + 6, 3, 2, skin)
            else:
                pyxel.rect(x + 1, body_y + 5, 3, 2, skin)
                pyxel.rect(x + 8, body_y + 6, 3, 2, skin)
            # 腿（弯曲站在滑板上）
            pyxel.rect(x + 3, body_y + 10, 3, 2, skin)
            pyxel.rect(x + 6, body_y + 10, 3, 2, skin)
        else:
            # 正面/背面滑行姿势
            # 滑板
            pyxel.rect(x + 1, y + 13, 10, 3, 4)  # 棕色板身
            pyxel.rect(x + 2, y + 14, 8, 1, 15)  # 浅色条纹
            pyxel.pset(x + 3, y + 16, 0)  # 左轮
            pyxel.pset(x + 8, y + 16, 0)  # 右轮
            
            body_y = y + sway
            # 头发
            pyxel.rect(x + 3, body_y, 6, 3, hair)
            if not self.is_male:
                pyxel.rect(x + 2, body_y + 2, 2, 3, hair)
                pyxel.rect(x + 8, body_y + 2, 2, 3, hair)
            # 头部
            pyxel.rect(x + 3, body_y + 2, 6, 4, skin)
            # 眼睛
            if self.direction == "down":
                pyxel.pset(x + 4, body_y + 4, 0)
                pyxel.pset(x + 7, body_y + 4, 0)
            # 身体
            pyxel.rect(x + 2, body_y + 6, 8, 5, cloth)
            # 手臂（向两侧伸展保持平衡）
            pyxel.rect(x, body_y + 6, 3, 2, skin)
            pyxel.rect(x + 9, body_y + 6, 3, 2, skin)
            # 腿（弯曲站在滑板上）
            pyxel.rect(x + 3, body_y + 11, 2, 2, skin)
            pyxel.rect(x + 7, body_y + 11, 2, 2, skin)
    
    def _draw_character(self, x, y):
        """绘制角色精灵 - 带行走动画"""
        # 行走时的身体上下弹跳
        body_bounce = 0
        if self.is_moving:
            # 四帧动画: 0,1,2,3 对应不同的腿部姿势
            if self.frame in [1, 3]:
                body_bounce = -1  # 身体稍微抬起
        
        # 计算实际绘制位置
        draw_y = y + body_bounce
        
        # 根据方向和帧数绘制不同姿势
        if self.direction == "down":
            self._draw_facing_down(x, draw_y)
        elif self.direction == "up":
            self._draw_facing_up(x, draw_y)
        elif self.direction == "left":
            self._draw_facing_left(x, draw_y)
        elif self.direction == "right":
            self._draw_facing_right(x, draw_y)
    
    def _draw_facing_down(self, x, y):
        """绘制朝下的角色"""
        frame = self.frame if self.is_moving else 0
        skin = self.skin_color
        cloth = self.cloth_color
        hair = self.hair_color
        
        # 头发
        pyxel.rect(x + 3, y, 6, 3, hair)
        if not self.is_male:  # 女性长发
            pyxel.rect(x + 2, y + 2, 2, 4, hair)
            pyxel.rect(x + 8, y + 2, 2, 4, hair)
        # 头部（肤色）
        pyxel.rect(x + 3, y + 2, 6, 5, skin)
        # 眼睛
        pyxel.pset(x + 4, y + 4, 0)
        pyxel.pset(x + 7, y + 4, 0)
        
        # 身体
        pyxel.rect(x + 2, y + 7, 8, 6, cloth)
        
        # 手臂动画
        if self.is_moving:
            if frame in [0, 2]:
                # 手臂自然下垂
                pyxel.rect(x + 1, y + 7, 2, 4, skin)  # 左手
                pyxel.rect(x + 9, y + 7, 2, 4, skin)  # 右手
            elif frame == 1:
                # 左手向前，右手向后
                pyxel.rect(x + 1, y + 8, 2, 3, skin)  # 左手
                pyxel.rect(x + 9, y + 6, 2, 3, skin)  # 右手
            else:  # frame == 3
                # 右手向前，左手向后
                pyxel.rect(x + 1, y + 6, 2, 3, skin)  # 左手
                pyxel.rect(x + 9, y + 8, 2, 3, skin)  # 右手
        else:
            # 站立时手臂下垂
            pyxel.rect(x + 1, y + 7, 2, 4, skin)
            pyxel.rect(x + 9, y + 7, 2, 4, skin)
        
        # 腿部动画
        if self.is_moving:
            if frame == 0:
                # 左腿前，右腿后
                pyxel.rect(x + 3, y + 13, 3, 3, 1)   # 左腿
                pyxel.rect(x + 6, y + 13, 3, 2, 1)   # 右腿
            elif frame == 1:
                # 双腿交叉中间
                pyxel.rect(x + 4, y + 13, 4, 3, 1)
            elif frame == 2:
                # 右腿前，左腿后
                pyxel.rect(x + 3, y + 13, 3, 2, 1)   # 左腿
                pyxel.rect(x + 6, y + 13, 3, 3, 1)   # 右腿
            else:  # frame == 3
                # 双腿交叉中间
                pyxel.rect(x + 4, y + 13, 4, 3, 1)
        else:
            # 站立
            pyxel.rect(x + 3, y + 13, 3, 3, 1)
            pyxel.rect(x + 6, y + 13, 3, 3, 1)
    
    def _draw_facing_up(self, x, y):
        """绘制朝上的角色（背面）"""
        frame = self.frame if self.is_moving else 0
        skin = self.skin_color
        cloth = self.cloth_color
        hair = self.hair_color
        
        # 头发（背面更多）
        pyxel.rect(x + 3, y, 6, 5, hair)
        if not self.is_male:  # 女性长发
            pyxel.rect(x + 2, y + 2, 2, 6, hair)
            pyxel.rect(x + 8, y + 2, 2, 6, hair)
        # 头部侧面（肤色）
        pyxel.rect(x + 3, y + 4, 1, 2, skin)
        pyxel.rect(x + 8, y + 4, 1, 2, skin)
        
        # 身体
        pyxel.rect(x + 2, y + 7, 8, 6, cloth)
        
        # 手臂动画
        if self.is_moving:
            if frame in [0, 2]:
                pyxel.rect(x + 1, y + 7, 2, 4, 15)
                pyxel.rect(x + 9, y + 7, 2, 4, 15)
            elif frame == 1:
                pyxel.rect(x + 1, y + 6, 2, 3, skin)
                pyxel.rect(x + 9, y + 8, 2, 3, skin)
            else:
                pyxel.rect(x + 1, y + 8, 2, 3, skin)
                pyxel.rect(x + 9, y + 6, 2, 3, skin)
        else:
            pyxel.rect(x + 1, y + 7, 2, 4, skin)
            pyxel.rect(x + 9, y + 7, 2, 4, skin)
        
        # 腿部动画
        if self.is_moving:
            if frame == 0:
                pyxel.rect(x + 3, y + 13, 3, 2, 1)
                pyxel.rect(x + 6, y + 13, 3, 3, 1)
            elif frame == 1:
                pyxel.rect(x + 4, y + 13, 4, 3, 1)
            elif frame == 2:
                pyxel.rect(x + 3, y + 13, 3, 3, 1)
                pyxel.rect(x + 6, y + 13, 3, 2, 1)
            else:
                pyxel.rect(x + 4, y + 13, 4, 3, 1)
        else:
            pyxel.rect(x + 3, y + 13, 3, 3, 1)
            pyxel.rect(x + 6, y + 13, 3, 3, 1)
    
    def _draw_facing_left(self, x, y):
        """绘制朝左的角色"""
        frame = self.frame if self.is_moving else 0
        skin = self.skin_color
        cloth = self.cloth_color
        hair = self.hair_color
        
        # 头发
        pyxel.rect(x + 4, y, 5, 3, hair)
        if not self.is_male:
            pyxel.rect(x + 6, y + 2, 3, 5, hair)
        # 头部
        pyxel.rect(x + 3, y + 2, 5, 5, skin)
        # 眼睛
        pyxel.pset(x + 4, y + 4, 0)
        
        # 身体
        pyxel.rect(x + 3, y + 7, 6, 6, cloth)
        
        # 手臂（侧面只显示一只）
        if self.is_moving:
            if frame in [0, 2]:
                pyxel.rect(x + 2, y + 7, 2, 4, skin)
            elif frame == 1:
                pyxel.rect(x + 1, y + 8, 2, 4, skin)  # 手臂向后
            else:
                pyxel.rect(x + 3, y + 6, 2, 4, skin)  # 手臂向前
        else:
            pyxel.rect(x + 2, y + 7, 2, 4, skin)
        
        # 腿部动画 - 侧面行走
        if self.is_moving:
            if frame == 0:
                # 左腿向前伸
                pyxel.line(x + 4, y + 13, x + 2, y + 15, 1)
                pyxel.line(x + 6, y + 13, x + 7, y + 15, 1)
            elif frame == 1:
                # 双腿并拢
                pyxel.rect(x + 4, y + 13, 3, 3, 1)
            elif frame == 2:
                # 右腿向前伸
                pyxel.line(x + 4, y + 13, x + 3, y + 15, 1)
                pyxel.line(x + 6, y + 13, x + 8, y + 15, 1)
            else:
                # 双腿并拢
                pyxel.rect(x + 4, y + 13, 3, 3, 1)
        else:
            pyxel.rect(x + 4, y + 13, 3, 3, 1)
    
    def _draw_facing_right(self, x, y):
        """绘制朝右的角色"""
        frame = self.frame if self.is_moving else 0
        skin = self.skin_color
        cloth = self.cloth_color
        hair = self.hair_color
        
        # 头发
        pyxel.rect(x + 3, y, 5, 3, hair)
        if not self.is_male:
            pyxel.rect(x + 3, y + 2, 3, 5, hair)
        # 头部
        pyxel.rect(x + 4, y + 2, 5, 5, skin)
        # 眼睛
        pyxel.pset(x + 7, y + 4, 0)
        
        # 身体
        pyxel.rect(x + 3, y + 7, 6, 6, cloth)
        
        # 手臂（侧面只显示一只）
        if self.is_moving:
            if frame in [0, 2]:
                pyxel.rect(x + 8, y + 7, 2, 4, skin)
            elif frame == 1:
                pyxel.rect(x + 7, y + 6, 2, 4, skin)  # 手臂向前
            else:
                pyxel.rect(x + 9, y + 8, 2, 4, skin)  # 手臂向后
        else:
            pyxel.rect(x + 8, y + 7, 2, 4, skin)
        
        # 腿部动画 - 侧面行走
        if self.is_moving:
            if frame == 0:
                # 右腿向前伸
                pyxel.line(x + 5, y + 13, x + 4, y + 15, 1)
                pyxel.line(x + 7, y + 13, x + 9, y + 15, 1)
            elif frame == 1:
                # 双腿并拢
                pyxel.rect(x + 5, y + 13, 3, 3, 1)
            elif frame == 2:
                # 左腿向前伸
                pyxel.line(x + 5, y + 13, x + 3, y + 15, 1)
                pyxel.line(x + 7, y + 13, x + 8, y + 15, 1)
            else:
                # 双腿并拢
                pyxel.rect(x + 5, y + 13, 3, 3, 1)
        else:
            pyxel.rect(x + 5, y + 13, 3, 3, 1)
            
    def take_damage(self, amount):
        """受到伤害"""
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0
        
    def heal(self, amount):
        """恢复生命"""
        self.hp = min(self.max_hp, self.hp + amount)
