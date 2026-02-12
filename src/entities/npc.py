# -*- coding: utf-8 -*-
"""
NPC 类 - 精细版
支持多种NPC类型（学生、教授、猫咪等）和对话功能
"""

import pyxel
import math
from config import TILE_SIZE


class NPC:
    """NPC 基类"""
    
    def __init__(self, npc_data):
        """初始化 NPC"""
        self.id = npc_data.get('id', 'npc')
        self.name = npc_data.get('name', 'NPC')
        self.type = npc_data.get('type', 'student')
        self.x = npc_data.get('x', 0)
        self.y = npc_data.get('y', 0)
        self.direction = npc_data.get('direction', 'down')
        self.dialogues = npc_data.get('dialogues', ["..."])
        self.personality = npc_data.get('personality', '')  # AI 人物设定
        self.can_play_football = npc_data.get('can_play_football', False)  # 是否可以踢足球
        
        self.width = 14
        self.height = 16
        self.dialogue_index = 0
        self.is_talking = False
        
        # 碰撞检测
        self.collision_checker = None  # 碰撞检测函数，由外部设置
        
        # 动画
        self.anim_timer = 0
        self.anim_frame = 0
        self.idle_timer = 0
        
        # 动作系统
        self.action_state = 'idle'  # idle, moving_to_target, doing_action, returning
        self.action_type = None  # 当前执行的动作类型
        self.action_timer = 0  # 动作计时器
        self.action_duration = 0  # 动作持续时间
        self.home_x = self.x  # 原始位置X
        self.home_y = self.y  # 原始位置Y
        self.target_x = 0  # 目标位置X
        self.target_y = 0  # 目标位置Y
        self.move_speed = 1.5  # 移动速度
        
    def start_action(self, action_type, target_x, target_y, duration=180):
        """
        开始执行动作
        
        参数:
            action_type: 动作类型 ('play_football', etc.)
            target_x, target_y: 目标位置
            duration: 动作持续时间（帧数，60帧=1秒）
        """
        if self.action_state != 'idle':
            return False
            
        self.action_type = action_type
        self.target_x = target_x
        self.target_y = target_y
        self.action_duration = duration
        self.action_timer = 0
        self.action_state = 'moving_to_target'
        self.football_ref = None  # 足球引用，用于踢球时追踪
        self.target_goal = None  # 目标球门
        return True
    
    def set_football_ref(self, football, target_goal=None):
        """
        设置足球引用和目标球门，用于踢球动作
        
        参数:
            football: 足球对象
            target_goal: 目标球门对象（可选）
        """
        self.football_ref = football
        self.target_goal = target_goal
        
    def update(self):
        """更新 NPC 状态"""
        self.anim_timer += 1
        if self.anim_timer >= 30:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2
        
        # 处理动作状态
        if self.action_state == 'moving_to_target':
            self._move_towards(self.target_x, self.target_y)
            # 检查是否到达目标
            if self._distance_to(self.target_x, self.target_y) < 10:
                self.action_state = 'doing_action'
                self.action_timer = 0
                
        elif self.action_state == 'doing_action':
            self.action_timer += 1
            # 执行动作期间的特殊行为
            if self.action_type == 'play_football' and self.football_ref:
                football = self.football_ref
                ball_dist = self._distance_to(football.x, football.y)
                
                # 计算NPC相对于球的位置，站到球和球门相反的一侧
                if self.target_goal:
                    goal_x, goal_y = self.target_goal.get_target_position()
                    # 计算从球门到足球的方向（NPC应该站在这个方向的延长线上）
                    dx = football.x - goal_x
                    dy = football.y - goal_y
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist > 0:
                        # NPC站在足球后面（相对于球门）
                        offset_dist = 20  # 站在球后面20像素
                        approach_x = football.x + (dx / dist) * offset_dist
                        approach_y = football.y + (dy / dist) * offset_dist
                        
                        # 限制目标位置在合理范围内（避免卡在边界外）
                        if hasattr(football, 'field_min_x'):
                            approach_x = max(football.field_min_x + 20, min(approach_x, football.field_max_x - 20))
                            approach_y = max(football.field_min_y + 20, min(approach_y, football.field_max_y - 20))
                        
                        # 先移动到球后面的位置
                        approach_dist = self._distance_to(approach_x, approach_y)
                        if approach_dist > 18:  # 还在远处，继续接近球后位置
                            self._move_towards(approach_x, approach_y)
                        else:  # 已经接近球后位置，直接冲向足球踢它
                            self._move_towards(football.x, football.y)
                    else:
                        # 如果距离为0，直接追球
                        self._move_towards(football.x, football.y)
                else:
                    # 没有目标球门，就简单地追着足球跑
                    self._move_towards(football.x, football.y)
            
            # 动作完成，开始返回
            if self.action_timer >= self.action_duration:
                self.action_state = 'returning'
                self.football_ref = None
                self.target_goal = None
                
        elif self.action_state == 'returning':
            self._move_towards(self.home_x, self.home_y)
            # 检查是否到达原位
            if self._distance_to(self.home_x, self.home_y) < 5:
                self.x = self.home_x
                self.y = self.home_y
                self.action_state = 'idle'
                self.action_type = None
                
        else:  # idle 状态
            # 随机看向不同方向
            self.idle_timer += 1
            if self.idle_timer >= 180:  # 每3秒随机换方向
                self.idle_timer = 0
                directions = ['up', 'down', 'left', 'right']
                self.direction = directions[pyxel.rndi(0, 3)]
                
    def _move_towards(self, target_x, target_y):
        """向目标位置移动（带碰撞检测）"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # 归一化方向并应用速度
            move_x = (dx / distance) * self.move_speed
            move_y = (dy / distance) * self.move_speed
            
            # 如果有碰撞检测器，进行碰撞检测
            if self.collision_checker:
                # 尝试X方向移动
                new_x = self.x + move_x
                if not self.collision_checker(new_x + 2, self.y + 2, self.width - 4, self.height - 4):
                    self.x = new_x
                
                # 尝试Y方向移动
                new_y = self.y + move_y
                if not self.collision_checker(self.x + 2, new_y + 2, self.width - 4, self.height - 4):
                    self.y = new_y
            else:
                # 没有碰撞检测器，直接移动
                self.x += move_x
                self.y += move_y
            
            # 更新朝向
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
                
    def _distance_to(self, target_x, target_y):
        """计算到目标点的距离"""
        dx = target_x - self.x
        dy = target_y - self.y
        return math.sqrt(dx * dx + dy * dy)
        
    def is_busy(self):
        """是否正在执行动作"""
        return self.action_state != 'idle'
            
    def draw(self, camera_x, camera_y):
        """绘制 NPC"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # 根据类型绘制不同的精灵
        if self.type == 'student':
            self._draw_student(screen_x, screen_y, 12)  # 蓝色衣服
        elif self.type == 'student_female':
            self._draw_student_female(screen_x, screen_y)
        elif self.type == 'professor':
            self._draw_professor(screen_x, screen_y)
        elif self.type.startswith('cat_'):
            self._draw_cat(screen_x, screen_y)
        else:
            self._draw_student(screen_x, screen_y, 11)  # 默认绿色
            
    def _draw_student(self, x, y, shirt_color):
        """绘制男学生"""
        # 身体（衬衫）
        pyxel.rect(x + 2, y + 5, 10, 8, shirt_color)
        
        # 头部（肤色）
        pyxel.rect(x + 3, y, 8, 7, 15)
        
        # 头发（黑色）
        pyxel.rect(x + 3, y, 8, 3, 0)
        
        # 眼睛
        if self.direction != 'up':
            eye_y = y + 4
            if self.direction == 'left':
                pyxel.pset(x + 4, eye_y, 0)
            elif self.direction == 'right':
                pyxel.pset(x + 9, eye_y, 0)
            else:
                pyxel.pset(x + 5, eye_y, 0)
                pyxel.pset(x + 8, eye_y, 0)
        
        # 腿（深蓝色裤子）
        pyxel.rect(x + 3, y + 13, 4, 3, 1)
        pyxel.rect(x + 7, y + 13, 4, 3, 1)
        
    def _draw_student_female(self, x, y):
        """绘制女学生"""
        # 身体（紫色上衣）
        pyxel.rect(x + 2, y + 5, 10, 8, 14)
        
        # 头部
        pyxel.rect(x + 3, y, 8, 7, 15)
        
        # 长发（棕色）
        pyxel.rect(x + 2, y, 10, 4, 4)
        pyxel.rect(x + 2, y + 4, 3, 5, 4)  # 左侧长发
        pyxel.rect(x + 9, y + 4, 3, 5, 4)  # 右侧长发
        
        # 眼睛
        if self.direction != 'up':
            eye_y = y + 4
            if self.direction == 'left':
                pyxel.pset(x + 4, eye_y, 0)
            elif self.direction == 'right':
                pyxel.pset(x + 9, eye_y, 0)
            else:
                pyxel.pset(x + 5, eye_y, 0)
                pyxel.pset(x + 8, eye_y, 0)
        
        # 裙子
        pyxel.rect(x + 3, y + 13, 8, 3, 2)
        
    def _draw_professor(self, x, y):
        """绘制教授"""
        # 身体（西装）
        pyxel.rect(x + 2, y + 5, 10, 8, 5)  # 灰色西装
        # 领带
        pyxel.rect(x + 6, y + 5, 2, 6, 8)
        
        # 头部
        pyxel.rect(x + 3, y, 8, 7, 15)
        
        # 秃头/稀疏头发
        pyxel.rect(x + 4, y, 6, 2, 6)  # 灰色头发
        
        # 眼镜
        if self.direction != 'up':
            eye_y = y + 4
            pyxel.rect(x + 4, eye_y - 1, 3, 3, 0)  # 左眼镜框
            pyxel.rect(x + 7, eye_y - 1, 3, 3, 0)  # 右眼镜框
            pyxel.pset(x + 5, eye_y, 12)  # 左镜片
            pyxel.pset(x + 8, eye_y, 12)  # 右镜片
        
        # 腿
        pyxel.rect(x + 3, y + 13, 4, 3, 5)
        pyxel.rect(x + 7, y + 13, 4, 3, 5)
        
    def _draw_cat(self, x, y):
        """绘制猫咪"""
        # 确定颜色
        if self.type == 'cat_orange':
            body_color = 9  # 橙色
            pattern_color = 10  # 黄色
        elif self.type == 'cat_black':
            body_color = 0  # 黑色
            pattern_color = 5  # 灰色
        else:  # cat_calico
            body_color = 7  # 白色
            pattern_color = 9  # 橙色斑点
            
        # 身体
        pyxel.rect(x + 3, y + 6, 8, 6, body_color)
        
        # 头
        pyxel.rect(x + 4, y + 2, 6, 5, body_color)
        
        # 耳朵
        pyxel.tri(x + 4, y + 2, x + 6, y + 2, x + 4, y, body_color)
        pyxel.tri(x + 8, y + 2, x + 10, y + 2, x + 10, y, body_color)
        
        # 花纹（三花猫和橘猫）
        if self.type == 'cat_calico':
            pyxel.pset(x + 5, y + 7, pattern_color)
            pyxel.pset(x + 8, y + 9, 0)  # 黑色斑
        elif self.type == 'cat_orange':
            pyxel.pset(x + 5, y + 4, pattern_color)
            
        # 眼睛
        eye_y = y + 4
        pyxel.pset(x + 5, eye_y, 11)  # 绿眼睛
        pyxel.pset(x + 8, eye_y, 11)
        
        # 尾巴（带摆动）
        tail_sway = math.sin(pyxel.frame_count * 0.1) * 2
        pyxel.line(x + 10, y + 8, int(x + 13 + tail_sway), y + 5, body_color)
        
        # 腿
        pyxel.rect(x + 4, y + 12, 2, 2, body_color)
        pyxel.rect(x + 8, y + 12, 2, 2, body_color)
        
    def get_rect(self):
        """获取碰撞矩形"""
        return (self.x, self.y, self.width, self.height)
        
    def check_interaction(self, player_x, player_y, player_w, player_h):
        """检查是否可以与玩家交互"""
        # 检查距离
        dx = abs((self.x + self.width / 2) - (player_x + player_w / 2))
        dy = abs((self.y + self.height / 2) - (player_y + player_h / 2))
        return dx < 24 and dy < 24
        
    def interact(self):
        """与 NPC 交互，返回对话内容"""
        if self.dialogue_index < len(self.dialogues):
            message = self.dialogues[self.dialogue_index]
            self.dialogue_index += 1
            self.is_talking = True
            return message
        else:
            self.dialogue_index = 0
            self.is_talking = False
            return None
            
    def reset_dialogue(self):
        """重置对话状态"""
        self.dialogue_index = 0
        self.is_talking = False


class NPCManager:
    """NPC管理器"""
    
    def __init__(self):
        """初始化NPC管理器"""
        self.npcs = []
        self.current_dialogue = None
        self.current_npc = None
        
    def load_npcs(self, npc_data_list, cat_data_list):
        """加载NPC数据"""
        for npc_data in npc_data_list:
            self.npcs.append(NPC(npc_data))
            
        for cat_data in cat_data_list:
            self.npcs.append(NPC(cat_data))
            
    def update(self):
        """更新所有NPC"""
        for npc in self.npcs:
            npc.update()
            
    def draw(self, camera_x, camera_y):
        """绘制所有NPC"""
        for npc in self.npcs:
            npc.draw(camera_x, camera_y)
            
    def check_interaction(self, player_x, player_y, player_w, player_h):
        """检查玩家是否可以与某个NPC交互"""
        for npc in self.npcs:
            if npc.check_interaction(player_x, player_y, player_w, player_h):
                return npc
        return None
        
    def start_dialogue(self, npc):
        """开始与NPC对话"""
        self.current_npc = npc
        self.current_dialogue = npc.interact()
        return self.current_dialogue
        
    def next_dialogue(self):
        """获取下一句对话"""
        if self.current_npc:
            dialogue = self.current_npc.interact()
            if dialogue is None:
                self.end_dialogue()
                return None
            self.current_dialogue = dialogue
            return dialogue
        return None
        
    def end_dialogue(self):
        """结束对话"""
        if self.current_npc:
            self.current_npc.reset_dialogue()
        self.current_npc = None
        self.current_dialogue = None
        
    def is_in_dialogue(self):
        """是否正在对话中"""
        return self.current_npc is not None
