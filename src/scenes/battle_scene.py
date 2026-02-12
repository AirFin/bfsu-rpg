# -*- coding: utf-8 -*-
"""
战斗场景
回合制战斗系统
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_RED
from src.systems.input_handler import InputHandler
from src.utils.font_manager import draw_text, text_width


class BattleScene:
    """战斗场景"""
    
    def __init__(self, scene_manager):
        """初始化战斗场景"""
        self.scene_manager = scene_manager
        self.enemy_hp = 50
        self.player_hp = 100
        self.turn = "player"
        self.message = "战斗开始！"
        
    def on_enter(self):
        """进入场景时调用"""
        self.enemy_hp = 50
        self.player_hp = 100
        self.turn = "player"
        self.message = "战斗开始！"
        
    def on_exit(self):
        """退出场景时调用"""
        pass
        
    def update(self):
        """更新逻辑"""
        if self.turn == "player":
            # 玩家回合
            if InputHandler.is_just_pressed(InputHandler.CONFIRM):  # 攻击
                damage = 10
                self.enemy_hp -= damage
                self.message = f"造成 {damage} 点伤害！"
                self.turn = "enemy"
            elif InputHandler.is_just_pressed(InputHandler.CANCEL) or InputHandler.is_just_pressed([pyxel.KEY_R]):  # 逃跑
                from src.scenes.scene_manager import SceneType
                self.scene_manager.change_scene(SceneType.GAME)
                
        # 检查战斗结果
        if self.enemy_hp <= 0:
            self.message = "战斗胜利！"
            # TODO: 返回游戏场景
            
    def draw(self):
        """绘制画面"""
        # 绘制敌人区域
        pyxel.rect(WINDOW_WIDTH // 2 - 20, 50, 40, 40, COLOR_RED)
        hp_text = f"HP: {self.enemy_hp}"
        draw_text(WINDOW_WIDTH // 2 - text_width(hp_text) // 2, 100, hp_text, COLOR_WHITE)
        
        # 绘制战斗菜单
        draw_text(20, 180, "[A] 攻击", COLOR_WHITE)
        draw_text(20, 196, "[B/R] 逃跑", COLOR_WHITE)
        
        # 绘制消息
        draw_text(20, 216, self.message, COLOR_WHITE)
        
        # 绘制玩家 HP
        draw_text(20, 236, f"玩家 HP: {self.player_hp}", COLOR_WHITE)
