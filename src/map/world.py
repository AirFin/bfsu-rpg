# -*- coding: utf-8 -*-
"""
世界管理模块
"""

import json
import os


class World:
    """世界管理器"""
    
    def __init__(self):
        """初始化世界管理器"""
        self.maps = {}
        self.current_map_id = None
        self.current_map = None
        
    def load_map(self, map_id, map_file=None):
        """加载地图"""
        if map_file:
            try:
                with open(map_file, 'r', encoding='utf-8') as f:
                    map_data = json.load(f)
                    self.maps[map_id] = map_data
            except FileNotFoundError:
                print(f"地图文件 {map_file} 未找到")
                return False
        
        if map_id in self.maps:
            self.current_map_id = map_id
            self.current_map = self.maps[map_id]
            return True
        return False
        
    def change_map(self, map_id, spawn_x=0, spawn_y=0):
        """切换地图"""
        if self.load_map(map_id):
            # 返回新位置
            return spawn_x, spawn_y
        return None
        
    def get_current_map(self):
        """获取当前地图"""
        return self.current_map
        
    def get_map_property(self, property_name, default=None):
        """获取地图属性"""
        if self.current_map:
            return self.current_map.get(property_name, default)
        return default
