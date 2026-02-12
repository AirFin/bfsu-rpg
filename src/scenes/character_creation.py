# -*- coding: utf-8 -*-
"""
角色创建场景
让玩家选择性别、肤色和输入姓名
"""

import pyxel
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.font_manager import draw_text, text_width


class CharacterCreationScene:
    """角色创建场景"""
    
    def __init__(self, scene_manager):
        """初始化角色创建场景"""
        self.scene_manager = scene_manager
        
        # 玩家数据
        self.player_data = {
            'gender': 'male',      # male, female
            'skin_color': 'yellow', # yellow, white, brown, black
            'name': '艾北外'
        }
        
        # 选项配置
        self.gender_options = ['男', '女']
        self.skin_options = ['黄', '白', '黑']
        self.skin_colors = {
            '黄': 15,   # 浅黄肤色
            '白': 7,    # 白色
            '黑': 4     # 棕色（显示为"黑"但用棕色）
        }
        self.skin_color_names = {
            '黄': 'yellow',
            '白': 'white', 
            '黑': 'brown'  # 显示"黑"但使用brown颜色值
        }
        
        # 当前选中的菜单项 (0=性别, 1=肤色, 2=姓名, 3=确认)
        self.selected_option = 0
        self.options_count = 4
        
        # 当前选中的子选项
        self.gender_index = 0  # 默认男
        self.skin_index = 0    # 默认黄
        
        # 姓名编辑
        self.editing_name = False
        self.name_cursor_visible = True
        self.cursor_timer = 0
        
        # 动画
        self.anim_frame = 0
        self.anim_timer = 0
        self.preview_walking = True  # 预览动画是否行走
        self.preview_direction = 'down'
        self.direction_timer = 0
        
    def on_enter(self):
        """进入场景"""
        pass
        
    def on_exit(self):
        """退出场景"""
        pass
        
    def update(self):
        """更新逻辑"""
        # 动画更新
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
            
        # 方向切换（预览不同方向的动画）
        self.direction_timer += 1
        if self.direction_timer >= 60:  # 每秒切换方向
            self.direction_timer = 0
            directions = ['down', 'left', 'up', 'right']
            current_idx = directions.index(self.preview_direction)
            self.preview_direction = directions[(current_idx + 1) % 4]
            
        # 光标闪烁
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.name_cursor_visible = not self.name_cursor_visible
            
        # 如果正在编辑姓名
        if self.editing_name:
            self._handle_name_input()
            return
            
        # 上下选择
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected_option = (self.selected_option - 1) % self.options_count
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected_option = (self.selected_option + 1) % self.options_count
            
        # 左右切换选项值
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self._change_option(-1)
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self._change_option(1)
            
        # 确认
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.selected_option == 2:  # 姓名
                self.editing_name = True
            elif self.selected_option == 3:  # 确认
                self._confirm_creation()
                
    def _change_option(self, delta):
        """改变选项值"""
        if self.selected_option == 0:  # 性别
            self.gender_index = (self.gender_index + delta) % len(self.gender_options)
            self.player_data['gender'] = 'male' if self.gender_index == 0 else 'female'
        elif self.selected_option == 1:  # 肤色
            self.skin_index = (self.skin_index + delta) % len(self.skin_options)
            skin_name = self.skin_options[self.skin_index]
            self.player_data['skin_color'] = self.skin_color_names[skin_name]
            
    def _handle_name_input(self):
        """处理姓名输入"""
        # 获取输入的文字
        input_chars = pyxel.input_text
        if input_chars:
            for char in input_chars:
                if ord(char) >= 32:  # 可打印字符
                    if len(self.player_data['name']) < 12:  # 限制长度
                        self.player_data['name'] += char
                        
        # 退格删除
        if pyxel.btnp(pyxel.KEY_BACKSPACE, 10, 3):
            if self.player_data['name']:
                self.player_data['name'] = self.player_data['name'][:-1]
                
        # 回车确认
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.editing_name = False
            
        # ESC 取消
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.editing_name = False
            
    def _confirm_creation(self):
        """确认创建角色"""
        # 保存玩家数据到 scene_manager，供 game_scene 使用
        self.scene_manager.player_data = self.player_data
        
        # 切换到游戏场景
        from src.scenes.scene_manager import SceneType
        self.scene_manager.change_scene(SceneType.GAME)
        
    def draw(self):
        """绘制界面"""
        pyxel.cls(1)
        
        # 标题
        title = "创建角色"
        title_x = WINDOW_WIDTH // 2 - text_width(title) // 2
        draw_text(title_x, 15, title, 7)
        
        # 绘制选项面板（左侧）
        panel_x = 20
        panel_y = 40
        panel_width = 120
        panel_height = 140
        
        # 面板背景
        pyxel.rect(panel_x, panel_y, panel_width, panel_height, 0)
        pyxel.rectb(panel_x, panel_y, panel_width, panel_height, 7)
        
        # 选项
        options = [
            ('性别', self.gender_options[self.gender_index]),
            ('肤色', self.skin_options[self.skin_index]),
            ('姓名', self.player_data['name']),
            ('', '确认开始')
        ]
        
        for i, (label, value) in enumerate(options):
            opt_y = panel_y + 15 + i * 30
            is_selected = (i == self.selected_option)
            
            if i == 3:  # 确认按钮
                # 确认按钮居中
                btn_text = value
                btn_x = panel_x + (panel_width - text_width(btn_text)) // 2
                if is_selected:
                    pyxel.rect(panel_x + 10, opt_y - 2, panel_width - 20, 16, 5)
                    draw_text(btn_x, opt_y, btn_text, 10)
                else:
                    draw_text(btn_x, opt_y, btn_text, 7)
            else:
                # 普通选项
                if is_selected:
                    pyxel.rect(panel_x + 4, opt_y - 2, panel_width - 8, 16, 5)
                    
                # 标签
                draw_text(panel_x + 10, opt_y, label + ":", 7 if not is_selected else 10)
                
                # 值（带左右箭头）
                if i == 2:  # 姓名
                    name_display = value
                    if self.editing_name and self.name_cursor_visible:
                        name_display += "_"
                    draw_text(panel_x + 50, opt_y, name_display, 10 if is_selected else 7)
                else:
                    # 左箭头
                    if is_selected:
                        draw_text(panel_x + 45, opt_y, "<", 13)
                    # 值
                    value_x = panel_x + 60
                    draw_text(value_x, opt_y, value, 10 if is_selected else 7)
                    # 右箭头
                    if is_selected:
                        draw_text(panel_x + 95, opt_y, ">", 13)
        
        # 绘制预览面板（右侧）
        preview_x = 160
        preview_y = 40
        preview_width = 80
        preview_height = 140
        
        pyxel.rect(preview_x, preview_y, preview_width, preview_height, 13)  # 浅灰色背景
        pyxel.rectb(preview_x, preview_y, preview_width, preview_height, 7)
        
        # 预览标题
        preview_title = "预览"
        draw_text(preview_x + (preview_width - text_width(preview_title)) // 2, preview_y + 5, preview_title, 7)
        
        # 绘制角色预览（放大显示）
        char_x = preview_x + preview_width // 2 - 16
        char_y = preview_y + 35
        self._draw_character_preview(char_x, char_y, scale=2)
        
        # 显示当前方向
        dir_names = {'down': '正面', 'up': '背面', 'left': '左侧', 'right': '右侧'}
        dir_text = dir_names[self.preview_direction]
        draw_text(preview_x + (preview_width - text_width(dir_text)) // 2, preview_y + 115, dir_text, 13)
        
        # 操作提示
        if self.editing_name:
            hint = "输入姓名，回车确认"
        else:
            hint = "↑↓选择 ←→切换 Z确认"
        hint_x = WINDOW_WIDTH // 2 - text_width(hint) // 2
        draw_text(hint_x, WINDOW_HEIGHT - 20, hint, 13)
        
    def _draw_character_preview(self, x, y, scale=2):
        """绘制角色预览（带缩放）"""
        # 获取肤色
        skin_name = self.skin_options[self.skin_index]
        skin_color = self.skin_colors[skin_name]
        
        # 性别决定衣服颜色和发型
        is_male = self.gender_index == 0
        cloth_color = 12 if is_male else 14  # 男蓝色，女粉色
        
        # 行走动画的身体弹跳
        bounce = 0
        if self.anim_frame in [1, 3]:
            bounce = -scale
            
        draw_y = y + bounce
        
        # 根据方向绘制
        if self.preview_direction == 'down':
            self._draw_preview_down(x, draw_y, scale, skin_color, cloth_color, is_male)
        elif self.preview_direction == 'up':
            self._draw_preview_up(x, draw_y, scale, skin_color, cloth_color, is_male)
        elif self.preview_direction == 'left':
            self._draw_preview_left(x, draw_y, scale, skin_color, cloth_color, is_male)
        else:
            self._draw_preview_right(x, draw_y, scale, skin_color, cloth_color, is_male)
            
    def _draw_preview_down(self, x, y, s, skin, cloth, is_male):
        """绘制正面预览"""
        frame = self.anim_frame
        
        # 头发
        hair_color = 0 if is_male else 4  # 男黑发，女棕发
        pyxel.rect(x + 3*s, y, 6*s, 3*s, hair_color)
        if not is_male:  # 女性长发
            pyxel.rect(x + 2*s, y + 2*s, 2*s, 4*s, hair_color)
            pyxel.rect(x + 8*s, y + 2*s, 2*s, 4*s, hair_color)
        
        # 头部
        pyxel.rect(x + 3*s, y + 2*s, 6*s, 5*s, skin)
        # 眼睛
        pyxel.rect(x + 4*s, y + 4*s, s, s, 0)
        pyxel.rect(x + 7*s, y + 4*s, s, s, 0)
        
        # 身体
        pyxel.rect(x + 2*s, y + 7*s, 8*s, 6*s, cloth)
        
        # 手臂
        if frame in [0, 2]:
            pyxel.rect(x + s, y + 7*s, 2*s, 4*s, skin)
            pyxel.rect(x + 9*s, y + 7*s, 2*s, 4*s, skin)
        elif frame == 1:
            pyxel.rect(x + s, y + 8*s, 2*s, 3*s, skin)
            pyxel.rect(x + 9*s, y + 6*s, 2*s, 3*s, skin)
        else:
            pyxel.rect(x + s, y + 6*s, 2*s, 3*s, skin)
            pyxel.rect(x + 9*s, y + 8*s, 2*s, 3*s, skin)
        
        # 腿
        leg_color = 1
        if frame == 0:
            pyxel.rect(x + 3*s, y + 13*s, 3*s, 3*s, leg_color)
            pyxel.rect(x + 6*s, y + 13*s, 3*s, 2*s, leg_color)
        elif frame == 1:
            pyxel.rect(x + 4*s, y + 13*s, 4*s, 3*s, leg_color)
        elif frame == 2:
            pyxel.rect(x + 3*s, y + 13*s, 3*s, 2*s, leg_color)
            pyxel.rect(x + 6*s, y + 13*s, 3*s, 3*s, leg_color)
        else:
            pyxel.rect(x + 4*s, y + 13*s, 4*s, 3*s, leg_color)
            
    def _draw_preview_up(self, x, y, s, skin, cloth, is_male):
        """绘制背面预览"""
        frame = self.anim_frame
        hair_color = 0 if is_male else 4
        
        # 头发（背面更多）
        pyxel.rect(x + 3*s, y, 6*s, 5*s, hair_color)
        if not is_male:
            pyxel.rect(x + 2*s, y + 2*s, 2*s, 6*s, hair_color)
            pyxel.rect(x + 8*s, y + 2*s, 2*s, 6*s, hair_color)
        
        # 身体
        pyxel.rect(x + 2*s, y + 7*s, 8*s, 6*s, cloth)
        
        # 手臂
        if frame in [0, 2]:
            pyxel.rect(x + s, y + 7*s, 2*s, 4*s, skin)
            pyxel.rect(x + 9*s, y + 7*s, 2*s, 4*s, skin)
        elif frame == 1:
            pyxel.rect(x + s, y + 6*s, 2*s, 3*s, skin)
            pyxel.rect(x + 9*s, y + 8*s, 2*s, 3*s, skin)
        else:
            pyxel.rect(x + s, y + 8*s, 2*s, 3*s, skin)
            pyxel.rect(x + 9*s, y + 6*s, 2*s, 3*s, skin)
        
        # 腿
        leg_color = 1
        if frame == 0:
            pyxel.rect(x + 3*s, y + 13*s, 3*s, 2*s, leg_color)
            pyxel.rect(x + 6*s, y + 13*s, 3*s, 3*s, leg_color)
        elif frame == 1:
            pyxel.rect(x + 4*s, y + 13*s, 4*s, 3*s, leg_color)
        elif frame == 2:
            pyxel.rect(x + 3*s, y + 13*s, 3*s, 3*s, leg_color)
            pyxel.rect(x + 6*s, y + 13*s, 3*s, 2*s, leg_color)
        else:
            pyxel.rect(x + 4*s, y + 13*s, 4*s, 3*s, leg_color)
            
    def _draw_preview_left(self, x, y, s, skin, cloth, is_male):
        """绘制左侧预览"""
        frame = self.anim_frame
        hair_color = 0 if is_male else 4
        
        # 头发
        pyxel.rect(x + 4*s, y, 5*s, 3*s, hair_color)
        if not is_male:
            pyxel.rect(x + 6*s, y + 2*s, 3*s, 5*s, hair_color)
        
        # 头部
        pyxel.rect(x + 3*s, y + 2*s, 5*s, 5*s, skin)
        # 眼睛
        pyxel.rect(x + 4*s, y + 4*s, s, s, 0)
        
        # 身体
        pyxel.rect(x + 3*s, y + 7*s, 6*s, 6*s, cloth)
        
        # 手臂
        if frame in [0, 2]:
            pyxel.rect(x + 2*s, y + 7*s, 2*s, 4*s, skin)
        elif frame == 1:
            pyxel.rect(x + s, y + 8*s, 2*s, 4*s, skin)
        else:
            pyxel.rect(x + 3*s, y + 6*s, 2*s, 4*s, skin)
        
        # 腿
        leg_color = 1
        if frame in [0, 2]:
            pyxel.line(x + 4*s, y + 13*s, x + 3*s, y + 15*s, leg_color)
            pyxel.line(x + 5*s, y + 13*s, x + 4*s, y + 15*s, leg_color)
            pyxel.line(x + 6*s, y + 13*s, x + 8*s, y + 15*s, leg_color)
            pyxel.line(x + 7*s, y + 13*s, x + 9*s, y + 15*s, leg_color)
        else:
            pyxel.rect(x + 4*s, y + 13*s, 4*s, 3*s, leg_color)
            
    def _draw_preview_right(self, x, y, s, skin, cloth, is_male):
        """绘制右侧预览"""
        frame = self.anim_frame
        hair_color = 0 if is_male else 4
        
        # 头发
        pyxel.rect(x + 3*s, y, 5*s, 3*s, hair_color)
        if not is_male:
            pyxel.rect(x + 3*s, y + 2*s, 3*s, 5*s, hair_color)
        
        # 头部
        pyxel.rect(x + 4*s, y + 2*s, 5*s, 5*s, skin)
        # 眼睛
        pyxel.rect(x + 7*s, y + 4*s, s, s, 0)
        
        # 身体
        pyxel.rect(x + 3*s, y + 7*s, 6*s, 6*s, cloth)
        
        # 手臂
        if frame in [0, 2]:
            pyxel.rect(x + 8*s, y + 7*s, 2*s, 4*s, skin)
        elif frame == 1:
            pyxel.rect(x + 7*s, y + 6*s, 2*s, 4*s, skin)
        else:
            pyxel.rect(x + 9*s, y + 8*s, 2*s, 4*s, skin)
        
        # 腿
        leg_color = 1
        if frame in [0, 2]:
            pyxel.line(x + 5*s, y + 13*s, x + 3*s, y + 15*s, leg_color)
            pyxel.line(x + 6*s, y + 13*s, x + 4*s, y + 15*s, leg_color)
            pyxel.line(x + 7*s, y + 13*s, x + 9*s, y + 15*s, leg_color)
            pyxel.line(x + 8*s, y + 13*s, x + 10*s, y + 15*s, leg_color)
        else:
            pyxel.rect(x + 5*s, y + 13*s, 4*s, 3*s, leg_color)
