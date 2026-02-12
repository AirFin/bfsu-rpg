# -*- coding: utf-8 -*-
"""
背包系统模块
"""


class Inventory:
    """背包系统"""
    
    def __init__(self, max_slots=20):
        """初始化背包"""
        self.max_slots = max_slots
        self.items = []
        self.gold = 0
        
    def add_item(self, item):
        """添加物品"""
        # 检查是否可堆叠
        if item.stackable:
            for existing in self.items:
                if existing.name == item.name:
                    existing.quantity += item.quantity
                    return True
                    
        # 检查背包空间
        if len(self.items) >= self.max_slots:
            return False
            
        self.items.append(item)
        return True
        
    def remove_item(self, item_name, quantity=1):
        """移除物品"""
        for i, item in enumerate(self.items):
            if item.name == item_name:
                if item.stackable and item.quantity > quantity:
                    item.quantity -= quantity
                else:
                    self.items.pop(i)
                return True
        return False
        
    def get_item(self, item_name):
        """获取物品"""
        for item in self.items:
            if item.name == item_name:
                return item
        return None
        
    def add_gold(self, amount):
        """添加金币"""
        self.gold += amount
        
    def spend_gold(self, amount):
        """花费金币"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
        
    def get_items_by_type(self, item_type):
        """按类型获取物品"""
        return [item for item in self.items if item.item_type == item_type]
