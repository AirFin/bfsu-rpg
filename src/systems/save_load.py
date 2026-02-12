# -*- coding: utf-8 -*-
"""
存档系统模块
"""

import json
import os


class SaveLoadSystem:
    """存档系统"""
    
    SAVE_DIR = "saves"
    
    def __init__(self):
        """初始化存档系统"""
        # 确保存档目录存在
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
            
    def save_game(self, slot, game_data):
        """
        保存游戏
        game_data: 包含玩家数据、位置、背包等信息的字典
        """
        filename = os.path.join(self.SAVE_DIR, f"save_{slot}.json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
            
    def load_game(self, slot):
        """加载游戏"""
        filename = os.path.join(self.SAVE_DIR, f"save_{slot}.json")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"存档 {slot} 不存在")
            return None
        except Exception as e:
            print(f"加载失败: {e}")
            return None
            
    def delete_save(self, slot):
        """删除存档"""
        filename = os.path.join(self.SAVE_DIR, f"save_{slot}.json")
        try:
            os.remove(filename)
            return True
        except FileNotFoundError:
            return False
            
    def get_save_info(self, slot):
        """获取存档信息（用于显示）"""
        filename = os.path.join(self.SAVE_DIR, f"save_{slot}.json")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    "exists": True,
                    "player_name": data.get("player_name", "未知"),
                    "play_time": data.get("play_time", 0),
                    "level": data.get("level", 1)
                }
        except:
            return {"exists": False}
            
    def list_saves(self):
        """列出所有存档"""
        saves = []
        for i in range(1, 4):  # 假设最多3个存档槽
            saves.append(self.get_save_info(i))
        return saves
