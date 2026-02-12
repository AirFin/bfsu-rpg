# -*- coding: utf-8 -*-
"""
对话系统模块
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK
from src.utils.font_manager import draw_text, text_width


class DialogueSystem:
    """对话系统"""
    
    def __init__(self):
        """初始化对话系统"""
        self.active = False
        self.dialogues = []
        self.current_index = 0
        self.speaker = ""
        self.text = ""
        self.text_display_index = 0  # 用于打字机效果
        self.text_speed = 2  # 每几帧显示一个字符
        self.frame_counter = 0
        
    def start_dialogue(self, dialogues, speaker=""):
        """开始对话"""
        self.active = True
        self.dialogues = dialogues
        self.current_index = 0
        self.speaker = speaker
        self.text = dialogues[0] if dialogues else ""
        self.text_display_index = 0
        self.frame_counter = 0
        
    def update(self):
        """更新对话"""
        if not self.active:
            return
            
        # 打字机效果
        self.frame_counter += 1
        if self.frame_counter >= self.text_speed:
            self.frame_counter = 0
            if self.text_display_index < len(self.text):
                self.text_display_index += 1
                
        # 按键处理
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.text_display_index < len(self.text):
                # 跳过打字机效果，直接显示全部
                self.text_display_index = len(self.text)
            else:
                # 下一句对话
                self.current_index += 1
                if self.current_index < len(self.dialogues):
                    self.text = self.dialogues[self.current_index]
                    self.text_display_index = 0
                else:
                    self.end_dialogue()
                    
    def end_dialogue(self):
        """结束对话"""
        self.active = False
        self.dialogues = []
        self.current_index = 0
        self.text = ""
        
    def draw(self):
        """绘制对话框"""
        if not self.active:
            return
            
        # 对话框背景
        box_height = 60
        box_y = WINDOW_HEIGHT - box_height - 10
        pyxel.rect(10, box_y, WINDOW_WIDTH - 20, box_height, COLOR_BLACK)
        pyxel.rectb(10, box_y, WINDOW_WIDTH - 20, box_height, COLOR_WHITE)
        
        # 说话者名字
        if self.speaker:
            draw_text(20, box_y + 8, self.speaker, COLOR_WHITE)
            
        # 对话文字（显示到当前索引）
        display_text = self.text[:self.text_display_index]
        draw_text(20, box_y + 26, display_text, COLOR_WHITE)
        
        # 继续提示（文字显示完毕后）
        if self.text_display_index >= len(self.text):
            draw_text(WINDOW_WIDTH - 30, box_y + box_height - 16, "▼", COLOR_WHITE)
