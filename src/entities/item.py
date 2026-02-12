# -*- coding: utf-8 -*-
"""
物品类
"""


class Item:
    """物品基类"""
    
    def __init__(self, name, item_type="misc", value=0, description=""):
        """初始化物品"""
        self.name = name
        self.item_type = item_type  # weapon, armor, consumable, misc
        self.value = value
        self.description = description
        self.stackable = item_type in ["consumable", "misc"]
        self.quantity = 1
        

class Weapon(Item):
    """武器类"""
    
    def __init__(self, name, attack=10, value=100, description=""):
        super().__init__(name, "weapon", value, description)
        self.attack = attack
        

class Armor(Item):
    """防具类"""
    
    def __init__(self, name, defense=5, value=80, description=""):
        super().__init__(name, "armor", value, description)
        self.defense = defense
        

class Consumable(Item):
    """消耗品类"""
    
    def __init__(self, name, effect_type="heal", effect_value=20, value=10, description=""):
        super().__init__(name, "consumable", value, description)
        self.effect_type = effect_type  # heal, mana, buff
        self.effect_value = effect_value
        
    def use(self, target):
        """使用物品"""
        if self.effect_type == "heal":
            target.heal(self.effect_value)
            return True
        return False
