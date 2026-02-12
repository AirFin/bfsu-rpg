# -*- coding: utf-8 -*-
"""
游戏菜单系统
包含主菜单、背包、任务、设置等子菜单
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW
from src.systems.input_handler import InputHandler
from src.utils.font_manager import draw_text, text_width


class GameMenu:
    """游戏菜单系统"""
    
    def __init__(self):
        """初始化菜单系统"""
        self.active = False
        self.current_menu = 'main'  # main, inventory, quests, settings
        self.selected = 0
        
        # 主菜单选项
        self.main_options = ['背包', '任务', '设置', '返回游戏']
        
        # 背包数据（示例）
        self.inventory_items = []
        
        # 任务数据（示例）
        self.quests = [
            {'name': '欢迎来到北外', 'desc': '与校园里的NPC对话', 'completed': False},
        ]
        
        # 设置选项
        self.settings_options = ['音量: 开', '天气: 随机', '返回']
        self.sound_on = True
        
        # 天气设置
        self.weather_modes = ['随机', '晴天', '下雨', '下雪']
        self.weather_mode_index = 0  # 0=随机
        self.weather_callback = None  # 用于通知游戏场景天气变化
        
        # 滚动位置（用于长列表）
        self.scroll_offset = 0
        
    def open(self):
        """打开菜单"""
        self.active = True
        self.current_menu = 'main'
        self.selected = 0
        self.scroll_offset = 0
        
    def close(self):
        """关闭菜单"""
        self.active = False
        self.current_menu = 'main'
        self.selected = 0
        
    def add_item(self, item_name, item_desc=""):
        """添加物品到背包（相同物品会叠加）"""
        # 查找是否已有相同物品
        for item in self.inventory_items:
            if item['name'] == item_name:
                # 叠加数量
                item['count'] = item.get('count', 1) + 1
                return
        # 新物品
        self.inventory_items.append({'name': item_name, 'desc': item_desc, 'count': 1})
        
    def add_quest(self, quest_name, quest_desc):
        """添加任务"""
        self.quests.append({'name': quest_name, 'desc': quest_desc, 'completed': False})
        
    def complete_quest(self, quest_name):
        """完成任务"""
        for quest in self.quests:
            if quest['name'] == quest_name:
                quest['completed'] = True
                break
                
    def update(self):
        """更新菜单"""
        if not self.active:
            return
            
        # 菜单键关闭/返回
        if InputHandler.is_just_pressed(InputHandler.MENU):
            if self.current_menu == 'main':
                self.close()
            else:
                self.current_menu = 'main'
                self.selected = 0
            return
            
        # 取消键关闭/返回（键盘 Esc/X，手柄 B）
        if InputHandler.is_just_pressed(InputHandler.CANCEL):
            if self.current_menu == 'main':
                self.close()
            else:
                self.current_menu = 'main'
                self.selected = 0
            return
            
        # 根据当前菜单处理输入
        if self.current_menu == 'main':
            self._update_main_menu()
        elif self.current_menu == 'inventory':
            self._update_inventory()
        elif self.current_menu == 'quests':
            self._update_quests()
        elif self.current_menu == 'settings':
            self._update_settings()
            
    def _update_main_menu(self):
        """更新主菜单"""
        # 上下选择
        if InputHandler.is_just_pressed(InputHandler.MOVE_UP):
            self.selected = (self.selected - 1) % len(self.main_options)
        elif InputHandler.is_just_pressed(InputHandler.MOVE_DOWN):
            self.selected = (self.selected + 1) % len(self.main_options)
            
        # 确认选择
        if InputHandler.is_just_pressed(InputHandler.CONFIRM):
            option = self.main_options[self.selected]
            if option == '背包':
                self.current_menu = 'inventory'
                self.selected = 0
            elif option == '任务':
                self.current_menu = 'quests'
                self.selected = 0
            elif option == '设置':
                self.current_menu = 'settings'
                self.selected = 0
            elif option == '返回游戏':
                self.close()
                
    def _update_inventory(self):
        """更新背包菜单"""
        if len(self.inventory_items) == 0:
            return
            
        if InputHandler.is_just_pressed(InputHandler.MOVE_UP):
            self.selected = (self.selected - 1) % len(self.inventory_items)
        elif InputHandler.is_just_pressed(InputHandler.MOVE_DOWN):
            self.selected = (self.selected + 1) % len(self.inventory_items)
            
    def _update_quests(self):
        """更新任务菜单"""
        if len(self.quests) == 0:
            return
            
        if InputHandler.is_just_pressed(InputHandler.MOVE_UP):
            self.selected = (self.selected - 1) % len(self.quests)
        elif InputHandler.is_just_pressed(InputHandler.MOVE_DOWN):
            self.selected = (self.selected + 1) % len(self.quests)
            
    def _update_settings(self):
        """更新设置菜单"""
        if InputHandler.is_just_pressed(InputHandler.MOVE_UP):
            self.selected = (self.selected - 1) % len(self.settings_options)
        elif InputHandler.is_just_pressed(InputHandler.MOVE_DOWN):
            self.selected = (self.selected + 1) % len(self.settings_options)
            
        # 确认选择
        if InputHandler.is_just_pressed(InputHandler.CONFIRM):
            if self.selected == 0:  # 音量开关
                self.sound_on = not self.sound_on
                self.settings_options[0] = '音量: 开' if self.sound_on else '音量: 关'
            elif self.selected == 1:  # 天气设置
                self.weather_mode_index = (self.weather_mode_index + 1) % len(self.weather_modes)
                self.settings_options[1] = '天气: ' + self.weather_modes[self.weather_mode_index]
                # 通知游戏场景更新天气
                if self.weather_callback:
                    self.weather_callback(self.weather_mode_index)
            elif self.selected == 2:  # 返回
                self.current_menu = 'main'
                self.selected = 0
                
    def draw(self):
        """绘制菜单"""
        if not self.active:
            return
            
        # 半透明背景遮罩
        for y in range(0, WINDOW_HEIGHT, 2):
            for x in range(0, WINDOW_WIDTH, 2):
                pyxel.pset(x, y, 0)
        
        # 根据当前菜单绘制
        if self.current_menu == 'main':
            self._draw_main_menu()
        elif self.current_menu == 'inventory':
            self._draw_inventory()
        elif self.current_menu == 'quests':
            self._draw_quests()
        elif self.current_menu == 'settings':
            self._draw_settings()
            
    def _draw_menu_frame(self, title, width=180, height=160):
        """绘制菜单框架"""
        x = (WINDOW_WIDTH - width) // 2
        y = (WINDOW_HEIGHT - height) // 2
        
        # 背景
        pyxel.rect(x, y, width, height, 1)
        # 边框
        pyxel.rectb(x, y, width, height, 7)
        pyxel.rectb(x + 1, y + 1, width - 2, height - 2, 5)
        
        # 标题栏
        pyxel.rect(x + 2, y + 2, width - 4, 16, 5)
        title_x = x + (width - text_width(title)) // 2
        draw_text(title_x, y + 5, title, 7)
        
        return x, y
        
    def _draw_main_menu(self):
        """绘制主菜单"""
        x, y = self._draw_menu_frame("菜单", 120, 120)
        
        # 选项
        for i, option in enumerate(self.main_options):
            opt_y = y + 28 + i * 20
            if i == self.selected:
                # 选中项高亮
                pyxel.rect(x + 4, opt_y - 2, 112, 16, 5)
                draw_text(x + 12, opt_y, "▶ " + option, 10)
            else:
                draw_text(x + 20, opt_y, option, 7)
                
        # 操作提示
        hint = "A/Z/Enter:确认  B/X/Esc:关闭"
        draw_text(x + (120 - text_width(hint)) // 2, y + 120 - 16, hint, 13)
        
    def _draw_inventory(self):
        """绘制背包"""
        x, y = self._draw_menu_frame("背包", 200, 180)
        
        if len(self.inventory_items) == 0:
            draw_text(x + 20, y + 50, "背包是空的", 13)
        else:
            # 物品列表
            visible_items = 6  # 可见物品数
            start_idx = max(0, self.selected - visible_items + 1)
            
            for i, item in enumerate(self.inventory_items[start_idx:start_idx + visible_items]):
                real_idx = start_idx + i
                item_y = y + 28 + i * 20
                
                # 显示名称和数量
                count = item.get('count', 1)
                if count > 1:
                    display_name = f"{item['name']} x{count}"
                else:
                    display_name = item['name']
                
                if real_idx == self.selected:
                    pyxel.rect(x + 4, item_y - 2, 192, 16, 5)
                    draw_text(x + 12, item_y, "▶ " + display_name, 10)
                else:
                    draw_text(x + 20, item_y, display_name, 7)
                    
            # 显示选中物品的描述
            if self.selected < len(self.inventory_items):
                desc = self.inventory_items[self.selected].get('desc', '')
                if desc:
                    draw_text(x + 10, y + 155, desc[:20], 13)
                    
        # 操作提示
        hint = "B/X/Esc:返回"
        draw_text(x + (200 - text_width(hint)) // 2, y + 180 - 16, hint, 13)
        
    def _draw_quests(self):
        """绘制任务列表"""
        x, y = self._draw_menu_frame("任务", 220, 180)
        
        if len(self.quests) == 0:
            draw_text(x + 20, y + 50, "暂无任务", 13)
        else:
            visible_quests = 5
            start_idx = max(0, self.selected - visible_quests + 1)
            
            for i, quest in enumerate(self.quests[start_idx:start_idx + visible_quests]):
                real_idx = start_idx + i
                quest_y = y + 28 + i * 24
                
                # 任务状态标记
                status = "✓" if quest['completed'] else "○"
                status_color = 11 if quest['completed'] else 8
                
                if real_idx == self.selected:
                    pyxel.rect(x + 4, quest_y - 2, 212, 20, 5)
                    draw_text(x + 10, quest_y, status, status_color)
                    draw_text(x + 24, quest_y, quest['name'], 10)
                else:
                    draw_text(x + 10, quest_y, status, status_color)
                    draw_text(x + 24, quest_y, quest['name'], 7)
                    
            # 显示选中任务的描述
            if self.selected < len(self.quests):
                desc = self.quests[self.selected].get('desc', '')
                if desc:
                    # 截断长描述
                    if len(desc) > 24:
                        desc = desc[:24] + "..."
                    draw_text(x + 10, y + 155, desc, 13)
                    
        # 操作提示
        hint = "B/X/Esc:返回"
        draw_text(x + (220 - text_width(hint)) // 2, y + 180 - 16, hint, 13)
        
    def _draw_settings(self):
        """绘制设置"""
        x, y = self._draw_menu_frame("设置", 150, 130)
        
        for i, option in enumerate(self.settings_options):
            opt_y = y + 30 + i * 22
            if i == self.selected:
                pyxel.rect(x + 4, opt_y - 2, 142, 18, 5)
                draw_text(x + 12, opt_y, "▶ " + option, 10)
            else:
                draw_text(x + 20, opt_y, option, 7)
                
        # 操作提示
        hint = "A/Z:切换  B/X/Esc:返回"
        draw_text(x + (150 - text_width(hint)) // 2, y + 130 - 16, hint, 13)
