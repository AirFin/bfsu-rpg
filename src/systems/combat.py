# -*- coding: utf-8 -*-
"""
战斗系统模块
"""

import random


class CombatSystem:
    """战斗系统"""
    
    def __init__(self, player, enemy):
        """初始化战斗"""
        self.player = player
        self.enemy = enemy
        self.turn = "player"
        self.is_finished = False
        self.winner = None
        self.log = []
        
    def player_attack(self):
        """玩家攻击"""
        # 基础伤害计算
        base_damage = 10
        variance = random.randint(-2, 5)
        damage = max(1, base_damage + variance)
        
        # 暴击判定
        if random.random() < 0.1:  # 10% 暴击率
            damage *= 2
            self.log.append(f"暴击！造成 {damage} 点伤害！")
        else:
            self.log.append(f"攻击造成 {damage} 点伤害！")
            
        self.enemy.take_damage(damage)
        self._check_battle_end()
        self.turn = "enemy"
        return damage
        
    def enemy_attack(self):
        """敌人攻击"""
        if not self.enemy.alive:
            return 0
            
        damage = self.enemy.do_attack()
        variance = random.randint(-1, 2)
        damage = max(1, damage + variance)
        
        self.log.append(f"{self.enemy.name} 造成 {damage} 点伤害！")
        self.player.take_damage(damage)
        self._check_battle_end()
        self.turn = "player"
        return damage
        
    def _check_battle_end(self):
        """检查战斗是否结束"""
        if self.player.hp <= 0:
            self.is_finished = True
            self.winner = "enemy"
            self.log.append("你被击败了...")
        elif not self.enemy.alive:
            self.is_finished = True
            self.winner = "player"
            self.log.append("战斗胜利！")
            
    def try_escape(self):
        """尝试逃跑"""
        if random.random() < 0.5:  # 50% 成功率
            self.is_finished = True
            self.winner = None
            self.log.append("成功逃跑！")
            return True
        else:
            self.log.append("逃跑失败！")
            self.turn = "enemy"
            return False
