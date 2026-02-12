# -*- coding: utf-8 -*-
"""
游戏场景 - 校园探索
主要游戏玩法场景，包含NPC对话系统和AI对话功能
支持多地图：东校区、地下通道、西校区、图书馆内部
"""

import pyxel
import random
from config import TILE_SIZE, COLOR_WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.entities.player import Player
from src.entities.npc import NPCManager
from src.entities.football import Football
from src.entities.goal import Goal
from src.map.campus_renderer import CampusRenderer
from src.map.tunnel_renderer import TunnelRenderer
from src.map.library_renderer import LibraryRenderer
from src.map.campus_map import (MAP_TILES_WIDTH, MAP_TILES_HEIGHT, NPC_DATA, CAT_DATA,
    CAMPUS_MAP, TILE_DOME, TILE_DOME_ARCH, TILE_LIBRARY, TILE_LIBRARY_WINDOW,
    TILE_CANTEEN, TILE_ADMIN, TILE_HALL, TILE_GYM, TILE_JAPAN, TILE_MAIN, TILE_WATER,
    TUNNEL_WIDTH, TUNNEL_HEIGHT, WEST_MAP_WIDTH, WEST_MAP_HEIGHT,
    LIBRARY_WIDTH, LIBRARY_HEIGHT, LIBRARY_NPC_DATA, LIBRARY_BOOKSHELF_CONTENT,
    TILE_LIB_BOOKSHELF, TILE_LIB_CHAIR)
from src.systems.ai_dialogue import AIDialogueSystem
from src.systems.input_handler import InputHandler
from src.ui.game_menu import GameMenu
from src.utils.font_manager import draw_text, text_width


# 地图类型常量
MAP_EAST_CAMPUS = 'east'      # 东校区
MAP_TUNNEL = 'tunnel'          # 地下通道
MAP_WEST_CAMPUS = 'west'       # 西校区
MAP_LIBRARY = 'library'        # 图书馆内部


# 操场草坪边界（根据地图数据计算，像素坐标）
# 新地图：操场草坪在第22-26行（y），第7-22列（x）
FIELD_MIN_X = 7 * TILE_SIZE + 4   # 左边界+一点内边距
FIELD_MIN_Y = 22 * TILE_SIZE + 4  # 上边界+一点内边距
FIELD_MAX_X = 23 * TILE_SIZE - 4  # 右边界-一点内边距
FIELD_MAX_Y = 26 * TILE_SIZE - 4  # 下边界-一点内边距


class GameScene:
    """游戏场景"""
    
    def __init__(self, scene_manager):
        """初始化游戏场景"""
        self.scene_manager = scene_manager
        
        # 当前地图
        self.current_map = MAP_EAST_CAMPUS
        
        # 创建各地图渲染器
        self.campus = CampusRenderer()           # 东校区
        self.tunnel = TunnelRenderer()           # 地下通道
        self.library = LibraryRenderer()         # 图书馆内部
        
        # 获取角色创建数据
        player_data = getattr(scene_manager, 'player_data', None)
        
        # 创建玩家，传入碰撞检测函数和角色数据
        self.player = Player(collision_checker=self._get_collision_checker(), player_data=player_data)
        
        # 创建NPC管理器
        self.npc_manager = NPCManager()
        self.npc_manager.load_npcs(NPC_DATA, CAT_DATA)
        
        # 为所有NPC设置碰撞检测器
        for npc in self.npc_manager.npcs:
            npc.collision_checker = self._get_collision_checker()
        
        # 相机位置
        self.camera_x = 0
        self.camera_y = 0
        
        # 对话状态
        self.show_interaction_hint = False
        self.nearby_npc = None
        self.current_dialogue_npc = None  # 当前正在对话的NPC
        
        # AI 对话系统
        self.ai_dialogue = AIDialogueSystem()
        self.llm_enabled = False
        
        # 足球（放在操场中央）
        field_center_x = (FIELD_MIN_X + FIELD_MAX_X) // 2
        field_center_y = (FIELD_MIN_Y + FIELD_MAX_Y) // 2
        self.football = Football(
            field_center_x, field_center_y,
            (FIELD_MIN_X, FIELD_MIN_Y, FIELD_MAX_X, FIELD_MAX_Y)
        )
        
        # 创建两个球门（左右两边）
        # 左球门紧贴操场左边缘（球门开口朝右，球门背面在场外）
        self.goal_left = Goal(FIELD_MIN_X, field_center_y, 'left')
        # 右球门在操场右侧（稍微往左一些，避免到跑道上）
        self.goal_right = Goal(FIELD_MAX_X - 16, field_center_y, 'right')
        self.goals = [self.goal_left, self.goal_right]
        
        # 进球消息
        self.goal_message = ""
        self.goal_message_timer = 0
        
        # 游戏菜单
        self.game_menu = GameMenu()
        # 添加一些初始物品（示例）
        self.game_menu.add_item("学生证", "北外学生证明")
        
        # 清真寺室内状态
        self.in_mosque = False
        self.mosque_player_x = 0
        self.mosque_player_y = 0
        # 保存室外玩家位置（用于返回时）
        self.outdoor_player_x = 0
        self.outdoor_player_y = 0
        # 清真寺入口冷却（防止退出后立刻重新进入）
        self.mosque_entrance_cooldown = 0
        
        # 清真寺入口位置（拱门区域）- 新位置：第4行，列11-13
        self.mosque_entrance = {
            'min_x': 11 * TILE_SIZE,
            'max_x': 14 * TILE_SIZE,
            'y': 5 * TILE_SIZE  # 拱门下方（第4行拱门，检测第5行）
        }
        
        # 地图切换入口位置
        # 东校区校门（进入地下通道）- 在地图底部边界（第39行之后）
        self.east_gate_entrance = {
            'min_x': 13 * TILE_SIZE,
            'max_x': 19 * TILE_SIZE,
            'y': 39 * TILE_SIZE  # 地图底部边界
        }
        # 地下通道入口（返回东校区）
        self.tunnel_entry_to_east = {
            'min_x': 7 * TILE_SIZE,
            'max_x': 13 * TILE_SIZE,
            'y': 0  # 顶部
        }
        # 地下通道底部施工牌子
        self.construction_sign = {
            'min_x': 7 * TILE_SIZE,
            'max_x': 13 * TILE_SIZE,
            'y': 27 * TILE_SIZE,  # 底部牌子位置
            'text': '未完待续，正在建设中'
        }
        # 图书馆入口位置（图书馆门：列14，行11）
        self.library_entrance = {
            'x': 14 * TILE_SIZE,
            'y': 12 * TILE_SIZE  # 门下方（行11的门，检测行12）
        }
        # 图书馆出口（内部）
        self.library_exit = {
            'x': 7 * TILE_SIZE,
            'y': 11 * TILE_SIZE  # 底部门
        }
        # 图书馆相关状态
        self.library_entrance_cooldown = 0
        self.outdoor_pos_before_library = {'x': 0, 'y': 0}  # 进入图书馆前的位置
        
        # 图书馆内交互状态
        self.library_interaction = {
            'show_bookshelf': False,
            'bookshelf_content': None,
            'show_sit_option': False,
            'is_sitting': False,
            'sit_position': None
        }
        
        # 图书馆NPC管理
        self.library_npc_manager = None  # 延迟初始化
        
        # 地图切换冷却
        self.map_switch_cooldown = 120  # 启动时2秒冷却，防止误触发
        
        # 施工牌子提示
        self.show_sign_hint = False
        self.sign_message = ""
        
        # 可收集的花朵（红花和黄花）
        self.flowers = self._generate_flowers()
        
        # 滑板道具（操场旁边）
        self.skateboard = {
            'x': 24 * TILE_SIZE + 4,  # 操场右侧草地
            'y': 20 * TILE_SIZE + 4,
            'collected': False
        }
        
        # 收集提示
        self.collect_message = ""
        self.collect_message_timer = 0
        
        # 锦鲤系统（小碧池）
        self.koi_fish = self._init_koi_fish()
        
        # 天气系统
        self.weather_types = ['sunny', 'rain', 'snow']
        self.current_weather = 'sunny'
        self.weather_timer = 0
        self.weather_duration = 60 * 30  # 每种天气持续30秒（60帧/秒）
        self.weather_particles = []  # 天气粒子（雨滴/雪花）
        self.weather_mode = 0  # 0=随机, 1=晴天, 2=下雨, 3=下雪
        self._init_weather_particles()
        
        # 设置菜单的天气回调
        self.game_menu.weather_callback = self._on_weather_setting_changed
    
    def _get_collision_checker(self):
        """获取当前地图的碰撞检测函数"""
        def checker(x, y, width, height):
            if self.current_map == MAP_EAST_CAMPUS:
                return self.campus.is_collision(x, y, width, height)
            elif self.current_map == MAP_TUNNEL:
                return self.tunnel.is_collision(x, y, width, height)
            elif self.current_map == MAP_LIBRARY:
                return self.library.is_collision(x, y, width, height)
            return False
        return checker
    
    def _init_library_npcs(self):
        """初始化图书馆内的NPC"""
        if self.library_npc_manager is None:
            self.library_npc_manager = NPCManager()
            self.library_npc_manager.load_npcs(LIBRARY_NPC_DATA, [])
            # 设置碰撞检测
            for npc in self.library_npc_manager.npcs:
                npc.collision_checker = self._get_collision_checker()
        
    def _init_weather_particles(self):
        """初始化天气粒子"""
        self.weather_particles = []
        for _ in range(100):
            self.weather_particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(-WINDOW_HEIGHT, WINDOW_HEIGHT),
                'speed': random.uniform(2, 5),
                'size': random.randint(1, 3)
            })
    
    def _init_koi_fish(self):
        """初始化池塘中的锦鲤"""
        import math
        koi_fish = []
        # 椭圆形池塘参数（与渲染器保持一致）
        pond_center_x = 27.5 * TILE_SIZE  # 池塘中心x
        pond_center_y = 10.5 * TILE_SIZE  # 池塘中心y
        pond_radius_x = 3.0 * TILE_SIZE   # 水平半径（留边距）
        pond_radius_y = 1.5 * TILE_SIZE   # 垂直半径（留边距）
        
        # 创建5条锦鲤
        fish_configs = [
            {'color': 8, 'name': '红锦鲤'},   # 红色
            {'color': 8, 'name': '红锦鲤'},   # 红色
            {'color': 7, 'name': '白锦鲤'},   # 白色
            {'color': 7, 'name': '白锦鲤'},   # 白色
            {'color': 8, 'name': '红锦鲤'},   # 红色
        ]
        
        for i, config in enumerate(fish_configs):
            # 在椭圆内随机生成位置
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(0.3, 0.8)  # 距离中心的比例
            x = pond_center_x + math.cos(angle) * pond_radius_x * r
            y = pond_center_y + math.sin(angle) * pond_radius_y * r
            
            koi_fish.append({
                'x': x,
                'y': y,
                'color': config['color'],
                'name': config['name'],
                'direction': random.uniform(0, 2 * math.pi),
                'speed': random.uniform(0.3, 0.5),
                'turn_timer': random.randint(30, 90),
                'tail_phase': random.uniform(0, 6.28),
                # 椭圆参数
                'pond_center_x': pond_center_x,
                'pond_center_y': pond_center_y,
                'pond_radius_x': pond_radius_x,
                'pond_radius_y': pond_radius_y
            })
        
        return koi_fish
    
    def _on_weather_setting_changed(self, mode_index):
        """天气设置改变时的回调"""
        self.weather_mode = mode_index
        if mode_index == 0:  # 随机模式
            pass  # 保持当前天气，下次切换时随机
        elif mode_index == 1:  # 晴天
            self.current_weather = 'sunny'
        elif mode_index == 2:  # 下雨
            self.current_weather = 'rain'
        elif mode_index == 3:  # 下雪
            self.current_weather = 'snow'
        self._init_weather_particles()
        
    def _generate_flowers(self):
        """在草地上生成红花和黄花（只放在确定的草地位置）"""
        flowers = []
        # 红花位置（都在草地G=0的位置）
        red_flower_positions = [
            (1, 1), (3, 1), (5, 1),      # 第1行左侧草地
            (1, 3), (3, 3),              # 第3行左侧草地
            (17, 3), (19, 3), (21, 3),   # 第3行中间草地
            (34, 4), (36, 4),            # 第4行右侧草地
            (1, 6), (3, 6),              # 第6行左侧草地
            (34, 7), (36, 7),            # 第7行右侧草地
            (25, 21), (27, 21),          # 操场右侧草地
            (35, 24), (37, 24),          # 日本楼右侧草地
        ]
        # 黄花位置（都在草地G=0的位置）
        yellow_flower_positions = [
            (4, 1), (6, 1),              # 第1行左侧草地
            (2, 3), (4, 3),              # 第3行左侧草地
            (18, 3), (20, 3),            # 第3行中间草地
            (35, 4), (37, 4),            # 第4行右侧草地
            (2, 6), (4, 6),              # 第6行左侧草地
            (35, 7), (37, 7),            # 第7行右侧草地
            (26, 21), (28, 21),          # 操场右侧草地
            (36, 24), (38, 24),          # 日本楼右侧草地
        ]
        
        for tx, ty in red_flower_positions:
            flowers.append({
                'x': tx * TILE_SIZE + 4,
                'y': ty * TILE_SIZE + 4,
                'collected': False,
                'name': '红花',
                'type': 'red'
            })
        
        for tx, ty in yellow_flower_positions:
            flowers.append({
                'x': tx * TILE_SIZE + 4,
                'y': ty * TILE_SIZE + 4,
                'collected': False,
                'name': '黄花',
                'type': 'yellow'
            })
        
        return flowers
        
    def on_enter(self):
        """进入场景时调用"""
        self._sync_llm_settings()

        # 检查是否有新的角色数据需要应用
        player_data = getattr(self.scene_manager, 'player_data', None)
        if player_data:
            # 更新玩家外观
            self.player.name = player_data.get('name', '艾北外')
            self.player.gender = player_data.get('gender', 'male')
            self.player.skin_color_name = player_data.get('skin_color', 'yellow')
            self.player.skin_color = self.player.SKIN_COLORS.get(self.player.skin_color_name, 15)
            self.player.cloth_color = 12 if self.player.gender == 'male' else 14
            self.player.hair_color = 0 if self.player.gender == 'male' else 4
            self.player.is_male = self.player.gender == 'male'
            print(f"[游戏] 已加载角色: {self.player.name}, 性别: {self.player.gender}, 肤色: {self.player.skin_color_name}")
            
            # 更新学生证描述，显示玩家姓名
            for item in self.game_menu.inventory_items:
                if item['name'] == '学生证':
                    item['desc'] = f"姓名：{self.player.name}"
                    break

    def _sync_llm_settings(self):
        """同步并应用本次运行的 LLM 设置"""
        settings = getattr(self.scene_manager, 'llm_settings', {}) or {}
        enabled = bool(settings.get('enabled', False))
        api_key = str(settings.get('api_key', '')).strip()
        base_url = str(settings.get('base_url', '')).strip()
        model = str(settings.get('model', '')).strip()

        if enabled and api_key and base_url and model:
            self.llm_enabled = True
            self.ai_dialogue.llm.configure(api_key, base_url, model)
            print("[游戏] LLM 已启用（使用设置页配置）")
        else:
            self.llm_enabled = False
            self.ai_dialogue.llm.disable()
            print("[游戏] LLM 已关闭，NPC将使用预设回复")
        
    def on_exit(self):
        """退出场景时调用"""
        pass
        
    def update(self):
        """更新逻辑"""
        # 如果在清真寺内部
        if self.in_mosque:
            self._update_mosque_interior()
            return
            
        # 如果菜单打开，优先处理菜单
        if self.game_menu.active:
            self.game_menu.update()
            return
        
        # 如果正在 AI 对话中
        if self.ai_dialogue.active:
            self.ai_dialogue.update()
            if self.ai_dialogue.active:
                return  # AI 对话时不能做其他事

        # 优先处理 AI 失败降级
        failure_message = self.ai_dialogue.consume_failure_message()
        if failure_message:
            self.collect_message = failure_message
            self.collect_message_timer = 120
            if self.current_dialogue_npc:
                self.npc_manager.start_dialogue(self.current_dialogue_npc)
                self.current_dialogue_npc = None
                self.ai_dialogue.pending_action = None
                return
        
        # 检查对话刚结束，是否有待执行的动作
        if self.ai_dialogue.pending_action and self.current_dialogue_npc:
            action = self.ai_dialogue.pending_action
            npc = self.current_dialogue_npc
            print(f"[游戏] 检测到待执行动作: {action}, NPC: {npc.name}")
            self.ai_dialogue.pending_action = None
            self.current_dialogue_npc = None
            self._trigger_npc_action(npc, action)
        elif self.current_dialogue_npc and not self.ai_dialogue.active:
            # 对话结束但没有动作，也要清空
            print(f"[游戏] 对话结束，无动作")
            self.current_dialogue_npc = None
            
        # 如果正在普通对话中（东校区）
        if self.npc_manager.is_in_dialogue():
            # 按确认键继续对话
            if InputHandler.is_just_pressed(InputHandler.CONFIRM):
                self.npc_manager.next_dialogue()
            return  # 对话时不能移动
        
        # 如果正在图书馆NPC对话中
        if self.current_map == MAP_LIBRARY and self.library_npc_manager and self.library_npc_manager.is_in_dialogue():
            if InputHandler.is_just_pressed(InputHandler.CONFIRM):
                self.library_npc_manager.next_dialogue()
            return
        
        # 如果在图书馆且正在查看书架
        if self.current_map == MAP_LIBRARY and self.library_interaction['show_bookshelf']:
            if (InputHandler.is_just_pressed(InputHandler.CONFIRM) or
                    InputHandler.is_just_pressed(InputHandler.CANCEL)):
                self.library_interaction['show_bookshelf'] = False
                self.library_interaction['bookshelf_content'] = None
            return
            
        # 更新天气系统
        self._update_weather()
        
        # 更新锦鲤
        self._update_koi_fish()
        
        # 更新当前地图渲染器
        if self.current_map == MAP_EAST_CAMPUS:
            self.campus.update(self.current_weather)
        elif self.current_map == MAP_TUNNEL:
            self.tunnel.update(self.current_weather)
            # 检查是否靠近施工牌子
            self._check_construction_sign()
        elif self.current_map == MAP_LIBRARY:
            self.library.update()
            # 更新图书馆NPC
            if self.library_npc_manager:
                self.library_npc_manager.update()
            # 检查图书馆交互
            self._check_library_interaction()
        
        # 更新NPC（只在东校区）
        if self.current_map == MAP_EAST_CAMPUS:
            self.npc_manager.update()
        
        # 更新玩家
        self.player.update()
        
        # 检查花朵收集
        self._check_flower_collection()
        
        # 检查滑板收集
        self._check_skateboard_collection()
        
        # 更新收集提示计时器
        if self.collect_message_timer > 0:
            self.collect_message_timer -= 1
        
        # 检查玩家是否踢到足球（只在东校区）
        if self.current_map == MAP_EAST_CAMPUS:
            self.football.check_kick(
                self.player.x, self.player.y,
                self.player.width, self.player.height
            )
            
            # 检查NPC是否踢到足球（NPC踢球时朝向目标球门）
            for npc in self.npc_manager.npcs:
                # 如果NPC有目标球门，就朝球门踢
                if hasattr(npc, 'target_goal') and npc.target_goal:
                    goal_x, goal_y = npc.target_goal.get_target_position()
                    self.football.check_kick(npc.x, npc.y, npc.width, npc.height, goal_x, goal_y)
                else:
                    self.football.check_kick(npc.x, npc.y, npc.width, npc.height)
            
            # 更新足球
            self.football.update()
            
            # 更新球门并检测进球
            for goal in self.goals:
                goal.update()
                if goal.check_goal(self.football.x, self.football.y, self.football.radius):
                    # 进球了！
                    side_name = "左" if goal.side == 'left' else "右"
                    self.goal_message = f"进球！{side_name}侧球门！"
                    self.goal_message_timer = 120  # 显示2秒
                    print(f"[游戏] 进球！{side_name}侧球门，总计: {goal.score}")
                    # 将球重置到中场
                    field_center_x = (FIELD_MIN_X + FIELD_MAX_X) // 2
                    field_center_y = (FIELD_MIN_Y + FIELD_MAX_Y) // 2
                    self.football.x = field_center_x
                    self.football.y = field_center_y
                    self.football.vx = 0
                    self.football.vy = 0
        
        # 更新进球消息计时器
        if self.goal_message_timer > 0:
            self.goal_message_timer -= 1
        
        # 检查是否有可交互的NPC（只在东校区）
        if self.current_map == MAP_EAST_CAMPUS:
            self.nearby_npc = self.npc_manager.check_interaction(
                self.player.x, self.player.y, 
                self.player.width, self.player.height
            )
            self.show_interaction_hint = self.nearby_npc is not None
            
            # 按交互键与NPC交互（进入AI对话模式）
            if self.show_interaction_hint and InputHandler.is_just_pressed(InputHandler.INTERACT):
                # 如果NPC正在执行动作，不能对话
                if self.nearby_npc.is_busy():
                    pass
                # 开启LLM且NPC有personality设定时，使用AI对话
                elif self.llm_enabled and self.nearby_npc.personality:
                    self.current_dialogue_npc = self.nearby_npc  # 保存当前对话的NPC
                    self.ai_dialogue.start_dialogue(
                        self.nearby_npc.name,
                        self.nearby_npc.personality,
                        self.nearby_npc.can_play_football
                    )
                else:
                    # 否则使用普通对话
                    self.npc_manager.start_dialogue(self.nearby_npc)
        else:
            self.nearby_npc = None
            self.show_interaction_hint = False
        
        # 检查是否进入清真寺
        self._check_mosque_entrance()
        
        # 检查是否进入图书馆
        self._check_library_entrance()
        
        # 检查是否切换地图
        self._check_map_switch()
        
        # 更新相机跟随玩家
        self._update_camera()
        
        # 菜单键打开菜单（M / 手柄Start）
        if InputHandler.is_just_pressed(InputHandler.MENU):
            self.game_menu.open()
    
    def _update_weather(self):
        """更新天气系统"""
        # 只有在随机模式下才切换天气
        if self.weather_mode == 0:  # 随机模式
            self.weather_timer += 1
            if self.weather_timer >= self.weather_duration:
                self.weather_timer = 0
                # 随机切换天气（晴天概率更高）
                weather_weights = [50, 30, 20]  # sunny, rain, snow
                self.current_weather = random.choices(self.weather_types, weights=weather_weights)[0]
        
        # 更新天气粒子
        if self.current_weather in ['rain', 'snow']:
            for particle in self.weather_particles:
                if self.current_weather == 'rain':
                    # 雨滴快速下落
                    particle['y'] += particle['speed'] * 3
                    particle['x'] += 1  # 略微倾斜
                else:
                    # 雪花缓慢飘落
                    particle['y'] += particle['speed'] * 0.5
                    particle['x'] += random.uniform(-1, 1)  # 左右飘动
                
                # 超出屏幕则重置
                if particle['y'] > WINDOW_HEIGHT:
                    particle['y'] = random.randint(-20, 0)
                    particle['x'] = random.randint(0, WINDOW_WIDTH)
                if particle['x'] < 0:
                    particle['x'] = WINDOW_WIDTH
                elif particle['x'] > WINDOW_WIDTH:
                    particle['x'] = 0
    
    def _update_koi_fish(self):
        """更新锦鲤游动"""
        import math
        for fish in self.koi_fish:
            cx = fish['pond_center_x']
            cy = fish['pond_center_y']
            rx = fish['pond_radius_x']
            ry = fish['pond_radius_y']
            
            # 更新转向计时器
            fish['turn_timer'] -= 1
            if fish['turn_timer'] <= 0:
                # 随机改变方向
                fish['direction'] += random.uniform(-0.8, 0.8)
                fish['turn_timer'] = random.randint(40, 100)
            
            # 根据方向移动
            dx = math.cos(fish['direction']) * fish['speed']
            dy = math.sin(fish['direction']) * fish['speed']
            
            new_x = fish['x'] + dx
            new_y = fish['y'] + dy
            
            # 椭圆边界检测: (x-cx)²/rx² + (y-cy)²/ry² <= 1
            norm_x = (new_x - cx) / rx
            norm_y = (new_y - cy) / ry
            distance = norm_x * norm_x + norm_y * norm_y
            
            if distance > 0.85:  # 接近边界时掉头
                # 计算指向中心的方向
                to_center = math.atan2(cy - fish['y'], cx - fish['x'])
                # 朝向中心偏转
                fish['direction'] = to_center + random.uniform(-0.5, 0.5)
                fish['turn_timer'] = random.randint(20, 50)
                # 不更新位置，等待下一帧
            else:
                fish['x'] = new_x
                fish['y'] = new_y
            
            # 更新尾巴摆动相位
            fish['tail_phase'] += 0.3

    def _check_flower_collection(self):
        """检查并收集花朵"""
        # 只在东校区收集花朵
        if self.current_map != MAP_EAST_CAMPUS:
            return
            
        px, py = self.player.x, self.player.y
        pw, ph = self.player.width, self.player.height
        
        for flower in self.flowers:
            if flower['collected']:
                continue
            
            # 简单的碰撞检测
            fx, fy = flower['x'], flower['y']
            flower_size = 8
            
            if (px < fx + flower_size and px + pw > fx and
                py < fy + flower_size and py + ph > fy):
                # 收集花朵
                flower['collected'] = True
                
                # 根据花朵类型设置描述
                if flower.get('type') == 'red':
                    desc = "红颜色的花。"
                else:
                    desc = "黄颜色的花。"
                
                # 添加到背包
                self.game_menu.add_item(flower['name'], desc)
                
                # 显示收集提示
                self.collect_message = f"获得了 {flower['name']}！"
                self.collect_message_timer = 90  # 显示1.5秒
                
                # 统计收集数量
                collected_count = sum(1 for f in self.flowers if f['collected'])
                total_count = len(self.flowers)
                print(f"[游戏] 收集了{flower['name']}! ({collected_count}/{total_count})")
    
    def _check_skateboard_collection(self):
        """检查并收集滑板"""
        if self.skateboard['collected']:
            return
        
        if self.current_map != MAP_EAST_CAMPUS:
            return
            
        px, py = self.player.x, self.player.y
        pw, ph = self.player.width, self.player.height
        
        sx, sy = self.skateboard['x'], self.skateboard['y']
        skateboard_size = 12
        
        if (px < sx + skateboard_size and px + pw > sx and
            py < sy + skateboard_size and py + ph > sy):
            # 收集滑板
            self.skateboard['collected'] = True
            self.player.has_skateboard = True
            
            # 添加到背包
            self.game_menu.add_item("滑板", "按B键或手柄X切换滑板模式，移动更快！")
            
            # 显示收集提示
            self.collect_message = "获得了 滑板！按B键或手柄X使用"
            self.collect_message_timer = 120  # 显示2秒
            
            print("[游戏] 收集了滑板！")
    
    def _check_mosque_entrance(self):
        """检查玩家是否进入清真寺入口"""
        # 只在东校区检测
        if self.current_map != MAP_EAST_CAMPUS:
            return
            
        # 冷却中则不检测
        if self.mosque_entrance_cooldown > 0:
            self.mosque_entrance_cooldown -= 1
            return
            
        px, py = self.player.x, self.player.y
        entrance = self.mosque_entrance
        
        # 检查玩家是否走到拱门区域并且朝上走
        if (entrance['min_x'] <= px <= entrance['max_x'] and
            py <= entrance['y'] and 
            self.player.direction == 'up'):
            # 保存室外位置
            self.outdoor_player_x = px
            self.outdoor_player_y = py
            # 进入清真寺
            self.in_mosque = True
            # 设置室内初始位置（入口处）
            self.mosque_player_x = 128  # 室内中央
            self.mosque_player_y = 200  # 靠近下方出口
            self.player.x = self.mosque_player_x
            self.player.y = self.mosque_player_y
            self.player.direction = 'up'
            print("[游戏] 进入清真寺内部")
    
    def _update_mosque_interior(self):
        """更新清真寺内部逻辑"""
        # 处理玩家移动（简化版，无碰撞）
        dx, dy = 0, 0
        speed = 2
        
        move_x, move_y = InputHandler.get_movement()

        if move_y < 0:
            dy = -speed
            self.player.direction = "up"
        elif move_y > 0:
            dy = speed
            self.player.direction = "down"
        if move_x < 0:
            dx = -speed
            self.player.direction = "left"
        elif move_x > 0:
            dx = speed
            self.player.direction = "right"
        
        self.player.is_moving = dx != 0 or dy != 0
        
        # 更新玩家位置（室内边界）
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # 室内边界 (留出墙壁空间)
        INTERIOR_MIN_X = 40
        INTERIOR_MAX_X = 216
        INTERIOR_MIN_Y = 40
        INTERIOR_MAX_Y = 210
        
        if INTERIOR_MIN_X <= new_x <= INTERIOR_MAX_X:
            self.player.x = new_x
        if INTERIOR_MIN_Y <= new_y <= INTERIOR_MAX_Y:
            self.player.y = new_y
        
        # 更新动画
        if self.player.is_moving:
            self.player.anim_timer += 1
            if self.player.anim_timer >= 8:
                self.player.anim_timer = 0
                self.player.frame = (self.player.frame + 1) % 4
        
        # 检查是否离开清真寺（走到下方出口）
        if self.player.y >= INTERIOR_MAX_Y - 5 and self.player.direction == 'down':
            # 离开清真寺
            self.in_mosque = False
            # 恢复室外位置（向下偏移更多，避免立刻重新触发入口）
            self.player.x = self.outdoor_player_x
            self.player.y = self.outdoor_player_y + 32  # 向下偏移2个瓦片
            self.player.direction = 'down'
            # 设置入口冷却时间（约1秒）
            self.mosque_entrance_cooldown = 60
            print("[游戏] 离开清真寺")
    
    def _check_map_switch(self):
        """检查是否需要切换地图"""
        # 冷却中则不检测
        if self.map_switch_cooldown > 0:
            self.map_switch_cooldown -= 1
            return
        
        px, py = self.player.x, self.player.y
        direction = self.player.direction
        
        if self.current_map == MAP_EAST_CAMPUS:
            # 在东校区：检查是否走到地图底部（进入地下通道）
            gate = self.east_gate_entrance
            # 必须在校门X范围、向下走、且走到地图底部
            if (gate['min_x'] <= px <= gate['max_x'] and 
                py >= gate['y'] and
                direction == 'down'):
                print(f"[调试] 触发东→地下: px={px}, py={py}, gate_y={gate['y']}, dir={direction}")
                self._switch_to_map(MAP_TUNNEL, 'from_east')
                
        elif self.current_map == MAP_TUNNEL:
            # 在地下通道：检查是否走到顶部（返回东校区）
            entry = self.tunnel_entry_to_east
            if (entry['min_x'] <= px <= entry['max_x'] and 
                py <= 1 * TILE_SIZE and
                self.player.direction == 'up'):
                self._switch_to_map(MAP_EAST_CAMPUS, 'from_tunnel')
        
        elif self.current_map == MAP_LIBRARY:
            # 在图书馆内：检查是否走到出口（底部门）
            exit_pos = self.library_exit
            if (abs(px - exit_pos['x']) < TILE_SIZE and
                py >= exit_pos['y'] and
                direction == 'down'):
                self._switch_to_map(MAP_EAST_CAMPUS, 'from_library')
    
    def _check_library_entrance(self):
        """检查是否进入图书馆（自动进入）"""
        if self.current_map != MAP_EAST_CAMPUS:
            return
        if self.library_entrance_cooldown > 0:
            self.library_entrance_cooldown -= 1
            return
        
        px, py = self.player.x, self.player.y
        entrance = self.library_entrance
        
        # 检查玩家是否在图书馆门前（自动进入，不需要按交互键）
        if (abs(px - entrance['x']) < TILE_SIZE * 1.2 and
            abs(py - entrance['y']) < TILE_SIZE * 1.2):
            # 保存当前位置
            self.outdoor_pos_before_library['x'] = px
            self.outdoor_pos_before_library['y'] = py
            # 切换到图书馆
            self._switch_to_map(MAP_LIBRARY, 'from_campus')
    
    def _switch_to_map(self, target_map, from_direction):
        """切换到目标地图"""
        print(f"[地图切换] {self.current_map} -> {target_map}, 来源={from_direction}")
        old_map = self.current_map
        self.current_map = target_map
        self.map_switch_cooldown = 60  # 1秒冷却
        
        # 根据目标地图和来源方向设置玩家位置
        if target_map == MAP_TUNNEL:
            # 从东校区进入，出现在通道顶部（安全位置）
            self.player.x = 10 * TILE_SIZE
            self.player.y = 3 * TILE_SIZE  # 稍微靠下，避免立刻触发返回
            self.player.direction = 'down'
                
        elif target_map == MAP_EAST_CAMPUS:
            if from_direction == 'from_library':
                # 从图书馆返回，回到保存的位置
                self.player.x = self.outdoor_pos_before_library['x']
                self.player.y = self.outdoor_pos_before_library['y'] + 16
                self.player.direction = 'down'
                self.library_entrance_cooldown = 60
            else:
                # 从地下通道返回东校区
                self.player.x = 16 * TILE_SIZE
                self.player.y = 34 * TILE_SIZE
                self.player.direction = 'up'
        
        elif target_map == MAP_LIBRARY:
            # 进入图书馆，出现在门口
            self.player.x = 7 * TILE_SIZE
            self.player.y = 10 * TILE_SIZE
            self.player.direction = 'up'
            # 初始化图书馆NPC
            self._init_library_npcs()
        
        # 强制更新相机到正确位置
        self.camera_x = self.player.x - WINDOW_WIDTH // 2
        self.camera_y = self.player.y - WINDOW_HEIGHT // 2
        self._update_camera()
        
        print(f"[游戏] 切换地图: {old_map} -> {target_map}, 玩家位置: ({self.player.x}, {self.player.y})")
    
    def _check_library_interaction(self):
        """检查图书馆内的交互（书架）"""
        if self.current_map != MAP_LIBRARY:
            return
        
        px, py = self.player.x, self.player.y
        tile_x, tile_y = self.library.get_tile_pos(px + 8, py + 8)
        
        # 检查附近的书架
        nearby_bookshelf = None
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # 上下左右
            check_x, check_y = tile_x + dx, tile_y + dy
            if (check_x, check_y) in LIBRARY_BOOKSHELF_CONTENT:
                nearby_bookshelf = (check_x, check_y)
                break
        
        # 显示交互提示
        if nearby_bookshelf:
            self.show_interaction_hint = True
            self.nearby_npc = None
            if InputHandler.is_just_pressed(InputHandler.INTERACT):
                content = LIBRARY_BOOKSHELF_CONTENT[nearby_bookshelf]
                self.library_interaction['show_bookshelf'] = True
                self.library_interaction['bookshelf_content'] = content
        else:
            self.show_interaction_hint = False
            self.nearby_npc = None

    def _check_construction_sign(self):
        """检查是否靠近施工牌子"""
        sign = self.construction_sign
        px, py = self.player.x, self.player.y
        
        # 检查玩家是否在牌子附近
        if (sign['min_x'] - 32 <= px <= sign['max_x'] + 32 and 
            sign['y'] - 32 <= py <= sign['y'] + 48):
            self.show_sign_hint = True
            self.sign_message = sign['text']
            # 按交互键阅读牌子
            if InputHandler.is_just_pressed(InputHandler.INTERACT):
                print(f"[游戏] 阅读牌子: {sign['text']}")
        else:
            self.show_sign_hint = False
            
    def _trigger_npc_action(self, npc, action):
        """触发NPC执行动作"""
        if action == 'play_football':
            # 让NPC去踢足球
            # 目标是足球的位置
            target_x = self.football.x
            target_y = self.football.y
            # 5秒 = 300帧，给NPC更多时间踢球
            npc.start_action('play_football', target_x, target_y, duration=300)
            # 传递足球引用和目标球门，让NPC能够追踪足球并往球门踢
            # 随机选择一个球门作为目标
            target_goal = random.choice(self.goals)
            npc.set_football_ref(self.football, target_goal)
            print(f"[游戏] {npc.name} 开始去踢足球，目标球门: {target_goal.side}")
            
    def _update_camera(self):
        """更新相机位置，跟随玩家"""
        # 目标相机位置：将玩家置于屏幕中央
        target_x = self.player.x - WINDOW_WIDTH // 2 + self.player.width // 2
        target_y = self.player.y - WINDOW_HEIGHT // 2 + self.player.height // 2
        
        # 平滑跟随
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # 根据当前地图限制相机边界
        if self.current_map == MAP_EAST_CAMPUS:
            map_pixel_width = MAP_TILES_WIDTH * TILE_SIZE
            map_pixel_height = MAP_TILES_HEIGHT * TILE_SIZE
        elif self.current_map == MAP_TUNNEL:
            map_pixel_width = TUNNEL_WIDTH * TILE_SIZE
            map_pixel_height = TUNNEL_HEIGHT * TILE_SIZE
        elif self.current_map == MAP_LIBRARY:
            map_pixel_width = LIBRARY_WIDTH * TILE_SIZE
            map_pixel_height = LIBRARY_HEIGHT * TILE_SIZE
        else:
            map_pixel_width = MAP_TILES_WIDTH * TILE_SIZE
            map_pixel_height = MAP_TILES_HEIGHT * TILE_SIZE
        
        self.camera_x = max(0, min(self.camera_x, map_pixel_width - WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, map_pixel_height - WINDOW_HEIGHT))
            
    def draw(self):
        """绘制画面"""
        # 如果在清真寺内部
        if self.in_mosque:
            self._draw_mosque_interior()
            return
        
        # 根据当前地图绘制
        if self.current_map == MAP_EAST_CAMPUS:
            self._draw_east_campus()
        elif self.current_map == MAP_TUNNEL:
            self._draw_tunnel()
        elif self.current_map == MAP_LIBRARY:
            self._draw_library()
        
        # 绘制天气效果（地下通道和室内除外）
        if self.current_map not in [MAP_TUNNEL, MAP_LIBRARY]:
            self._draw_weather()
        
        # 绘制交互提示（东校区和图书馆）
        if self.current_map == MAP_EAST_CAMPUS:
            if self.show_interaction_hint and not self.npc_manager.is_in_dialogue() and not self.ai_dialogue.active:
                self._draw_interaction_hint()
            
            # 绘制普通对话框
            if self.npc_manager.is_in_dialogue():
                self._draw_dialogue_box()
                
            # 绘制AI对话界面
            if self.ai_dialogue.active:
                self.ai_dialogue.draw()
        
        elif self.current_map == MAP_LIBRARY:
            # 图书馆交互提示和对话
            if self.library_interaction['show_bookshelf']:
                self._draw_bookshelf_content()
            elif self.show_interaction_hint:
                self._draw_interaction_hint()
            elif self.library_interaction['show_sit_option']:
                self._draw_sit_hint()
            
            # 图书馆NPC对话
            if self.library_npc_manager and self.library_npc_manager.is_in_dialogue():
                self._draw_dialogue_box()
        
        # 绘制 HUD
        self._draw_hud()
        
        # 绘制游戏菜单（最后绘制，覆盖其他UI）
        if self.game_menu.active:
            self.game_menu.draw()
    
    def _draw_east_campus(self):
        """绘制东校区"""
        # 绘制校园场景
        self.campus.draw(self.camera_x, self.camera_y)
        
        # 绘制锦鲤（在水面上）
        self._draw_koi_fish()
        
        # 绘制花朵
        self._draw_flowers()
        
        # 绘制滑板道具
        self._draw_skateboard()
        
        # 绘制球门（在NPC之前，作为背景元素）
        for goal in self.goals:
            goal.draw(self.camera_x, self.camera_y)
        
        # 绘制NPC
        self.npc_manager.draw(self.camera_x, self.camera_y)
        
        # 绘制足球
        self.football.draw(self.camera_x, self.camera_y)
        
        # 绘制玩家
        self.player.draw(self.camera_x, self.camera_y)
    
    def _draw_tunnel(self):
        """绘制地下通道"""
        # 绘制通道场景
        self.tunnel.draw(self.camera_x, self.camera_y)
        
        # 绘制玩家
        self.player.draw(self.camera_x, self.camera_y)
        
        # 绘制施工牌子提示
        if self.show_sign_hint:
            # 绘制提示框
            box_x = WINDOW_WIDTH // 2 - 70
            box_y = 20
            box_w = 140
            box_h = 30
            
            # 背景框
            pyxel.rect(box_x, box_y, box_w, box_h, 0)
            pyxel.rectb(box_x, box_y, box_w, box_h, 8)
            
            # 文字
            text = self.sign_message
            text_x = box_x + (box_w - text_width(text)) // 2
            draw_text(text_x, box_y + 11, text, 10)
    
    def _draw_library(self):
        """绘制图书馆内部"""
        # 绘制图书馆场景
        self.library.render(self.camera_x, self.camera_y)
        
        # 绘制图书馆NPC
        if self.library_npc_manager:
            self.library_npc_manager.draw(self.camera_x, self.camera_y)
        
        # 绘制玩家（如果坐下则特殊处理）
        if self.library_interaction['is_sitting']:
            # 坐下时只绘制上半身
            self._draw_player_sitting()
        else:
            self.player.draw(self.camera_x, self.camera_y)
        
        # 绘制顶部标题
        draw_text(WINDOW_WIDTH // 2 - 30, 5, "北外图书馆", 1)
        
        # 出口提示
        exit_screen_x = int(7 * TILE_SIZE - self.camera_x)
        exit_screen_y = int(11 * TILE_SIZE - self.camera_y)
        if abs(self.player.x - 7 * TILE_SIZE) < TILE_SIZE and abs(self.player.y - 10 * TILE_SIZE) < TILE_SIZE:
            draw_text(exit_screen_x - 10, exit_screen_y - 10, "↓出口", 8)
    
    def _draw_player_sitting(self):
        """绘制坐下的玩家"""
        screen_x = int(self.player.x - self.camera_x)
        screen_y = int(self.player.y - self.camera_y)
        # 简单绘制上半身
        pyxel.rect(screen_x + 2, screen_y + 2, 12, 8, self.player.skin_color)  # 头
        pyxel.rect(screen_x + 4, screen_y + 10, 8, 6, self.player.cloth_color)  # 身体
    
    def _draw_bookshelf_content(self):
        """绘制书架内容弹窗"""
        content = self.library_interaction['bookshelf_content']
        if not content:
            return
        
        # 弹窗背景
        box_x = 30
        box_y = 40
        box_w = WINDOW_WIDTH - 60
        box_h = 130
        
        pyxel.rect(box_x, box_y, box_w, box_h, 1)
        pyxel.rectb(box_x, box_y, box_w, box_h, 7)
        pyxel.rectb(box_x + 2, box_y + 2, box_w - 4, box_h - 4, 5)
        
        # 标题
        title = content['title']
        draw_text(box_x + (box_w - text_width(title)) // 2, box_y + 8, title, 10)
        
        # 分隔线
        pyxel.line(box_x + 10, box_y + 25, box_x + box_w - 10, box_y + 25, 5)
        
        # 书籍列表
        books = content['books']
        for i, book in enumerate(books):
            draw_text(box_x + 20, box_y + 35 + i * 20, f"• {book}", 7)
        
        # 关闭提示
        hint = "按A/Enter关闭"
        draw_text(box_x + (box_w - text_width(hint)) // 2, box_y + box_h - 20, hint, 13)
    
    def _draw_sit_hint(self):
        """绘制坐下提示"""
        if self.library_interaction['is_sitting']:
            hint = "按A/Enter站起来"
        else:
            hint = "按A/Enter坐下"
        
        box_x = WINDOW_WIDTH // 2 - 40
        box_y = 20
        pyxel.rect(box_x, box_y, 80, 16, 0)
        pyxel.rectb(box_x, box_y, 80, 16, 7)
        draw_text(box_x + 5, box_y + 4, hint, 7)
    
    def _draw_west_campus(self):
        """绘制西校区"""
        # 绘制西校区场景
        self.west_campus.draw(self.camera_x, self.camera_y)
        
        # 绘制玩家
        self.player.draw(self.camera_x, self.camera_y)
        
    def _draw_interaction_hint(self):
        """绘制交互提示"""
        if self.nearby_npc:
            # 在NPC头顶显示提示
            npc_screen_x = int(self.nearby_npc.x - self.camera_x)
            npc_screen_y = int(self.nearby_npc.y - self.camera_y)
            
            # 感叹号气泡
            bubble_x = npc_screen_x + 3
            bubble_y = npc_screen_y - 12
            pyxel.rect(bubble_x, bubble_y, 10, 10, 7)
            draw_text(bubble_x + 2, bubble_y, "!", 0)
        elif self.current_map == MAP_EAST_CAMPUS:
            # 检查是否在图书馆门前
            px, py = self.player.x, self.player.y
            entrance = self.library_entrance
            if (abs(px - entrance['x']) < TILE_SIZE * 1.5 and
                abs(py - entrance['y']) < TILE_SIZE * 1.5 and
                self.player.direction == 'up'):
                # 显示进入图书馆提示
                hint = "按A/Enter进入图书馆"
                box_x = WINDOW_WIDTH // 2 - 55
                box_y = 20
                pyxel.rect(box_x, box_y, 110, 18, 0)
                pyxel.rectb(box_x, box_y, 110, 18, 7)
                draw_text(box_x + 5, box_y + 4, hint, 7)
        elif self.current_map == MAP_LIBRARY:
            # 图书馆内交互提示
            if self.nearby_npc:
                hint = "按A/Enter对话"
            else:
                hint = "按A/Enter查看书架"
            box_x = WINDOW_WIDTH // 2 - 50
            box_y = 20
            pyxel.rect(box_x, box_y, 100, 18, 0)
            pyxel.rectb(box_x, box_y, 100, 18, 7)
            draw_text(box_x + 5, box_y + 4, hint, 7)
            
    def _draw_dialogue_box(self):
        """绘制对话框"""
        # 对话框背景
        box_x = 10
        box_y = WINDOW_HEIGHT - 70
        box_w = WINDOW_WIDTH - 20
        box_h = 60
        
        # 外框
        pyxel.rect(box_x, box_y, box_w, box_h, 1)
        pyxel.rectb(box_x, box_y, box_w, box_h, 7)
        pyxel.rectb(box_x + 2, box_y + 2, box_w - 4, box_h - 4, 12)
        
        # 获取当前对话的NPC（可能是东校区或图书馆的）
        current_npc = None
        current_text = None
        if self.current_map == MAP_LIBRARY and self.library_npc_manager:
            current_npc = self.library_npc_manager.current_npc
            current_text = self.library_npc_manager.current_dialogue
        else:
            current_npc = self.npc_manager.current_npc
            current_text = self.npc_manager.current_dialogue
        
        # NPC名称
        if current_npc:
            name = current_npc.name
            name_w = text_width(name) + 8
            pyxel.rect(box_x + 8, box_y - 6, name_w, 14, 1)
            draw_text(box_x + 12, box_y - 4, name, 10)
        
        # 对话内容
        if self.npc_manager.current_dialogue:
            # 简单的文本换行
            text = current_text if current_text else ""
            max_width = box_w - 24
            lines = self._wrap_text_simple(text, max_width)
            y_offset = 0
            
            for line in lines[:3]:  # 最多显示3行
                draw_text(box_x + 12, box_y + 12 + y_offset, line, 7)
                y_offset += 14
        
        # 继续提示
        if (pyxel.frame_count // 30) % 2 == 0:
            draw_text(box_x + box_w - 30, box_y + box_h - 14, ">>", 7)
            
    def _wrap_text_simple(self, text, max_width):
        """简单文本换行"""
        lines = []
        current_line = ""
        for char in text:
            test_line = current_line + char
            if text_width(test_line) > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines if lines else [""]
    
    def _draw_koi_fish(self):
        """绘制池塘中游动的锦鲤"""
        import math
        for fish in self.koi_fish:
            # 计算屏幕位置
            screen_x = int(fish['x'] - self.camera_x)
            screen_y = int(fish['y'] - self.camera_y)
            
            # 检查是否在屏幕内
            if -20 < screen_x < WINDOW_WIDTH + 20 and -20 < screen_y < WINDOW_HEIGHT + 20:
                color = fish['color']
                direction = fish['direction']
                tail_offset = math.sin(fish['tail_phase']) * 1.5
                
                # 计算朝向
                dx = math.cos(direction)
                dy = math.sin(direction)
                
                # 鱼身体（椭圆形）- 根据朝向绘制
                # 身体中心
                pyxel.circ(screen_x, screen_y, 3, color)
                
                # 身体前端（头部方向）
                head_x = screen_x + int(dx * 3)
                head_y = screen_y + int(dy * 3)
                pyxel.circ(head_x, head_y, 2, color)
                
                # 尾巴（与头相反方向，加上摆动）
                tail_x = screen_x - int(dx * 4) + int(tail_offset * dy)
                tail_y = screen_y - int(dy * 4) - int(tail_offset * dx)
                pyxel.tri(
                    int(screen_x - dx * 2), int(screen_y - dy * 2),  # 尾巴根部
                    int(tail_x - dy * 2), int(tail_y + dx * 2),      # 尾巴左端
                    int(tail_x + dy * 2), int(tail_y - dx * 2),      # 尾巴右端
                    color
                )
                
                # 花纹（白锦鲤加红斑点，红锦鲤加白斑点）
                if color == 7:  # 白锦鲤
                    pyxel.pset(screen_x, screen_y, 8)  # 红色斑点
                else:  # 红锦鲤
                    pyxel.pset(screen_x, screen_y, 7)  # 白色斑点
                
                # 眼睛（小黑点）
                eye_x = head_x + int(dx * 1)
                eye_y = head_y + int(dy * 1)
                pyxel.pset(eye_x, eye_y, 0)

    def _draw_flowers(self):
        """绘制可收集的花朵"""
        for flower in self.flowers:
            if flower['collected']:
                continue
            
            # 计算屏幕位置
            screen_x = int(flower['x'] - self.camera_x)
            screen_y = int(flower['y'] - self.camera_y)
            
            # 检查是否在屏幕内
            if -16 < screen_x < WINDOW_WIDTH + 16 and -16 < screen_y < WINDOW_HEIGHT + 16:
                # 根据花朵类型选择颜色
                flower_type = flower.get('type', 'red')
                if flower_type == 'red':
                    petal_color = 8   # 红色
                    center_color = 10  # 黄色花蕊
                else:  # yellow
                    petal_color = 10  # 黄色
                    center_color = 9   # 橙色花蕊
                
                # 花茎
                pyxel.line(screen_x + 4, screen_y + 8, screen_x + 4, screen_y + 4, 11)
                # 花瓣
                pyxel.circ(screen_x + 4, screen_y + 3, 3, petal_color)
                pyxel.circ(screen_x + 2, screen_y + 2, 2, petal_color)
                pyxel.circ(screen_x + 6, screen_y + 2, 2, petal_color)
                pyxel.circ(screen_x + 4, screen_y + 1, 2, petal_color)
                # 花蕊
                pyxel.pset(screen_x + 4, screen_y + 3, center_color)
                # 叶子
                pyxel.pset(screen_x + 2, screen_y + 6, 11)
                pyxel.pset(screen_x + 6, screen_y + 6, 11)
    
    def _draw_skateboard(self):
        """绘制滑板道具"""
        if self.skateboard['collected']:
            return
        
        # 计算屏幕位置
        screen_x = int(self.skateboard['x'] - self.camera_x)
        screen_y = int(self.skateboard['y'] - self.camera_y)
        
        # 检查是否在屏幕内
        if -16 < screen_x < WINDOW_WIDTH + 16 and -16 < screen_y < WINDOW_HEIGHT + 16:
            # 滑板板身（木色）
            pyxel.rect(screen_x, screen_y + 3, 12, 4, 4)  # 棕色板身
            pyxel.rect(screen_x + 1, screen_y + 4, 10, 2, 15)  # 浅色表面
            # 滑板翘起的两端
            pyxel.pset(screen_x, screen_y + 2, 4)
            pyxel.pset(screen_x + 11, screen_y + 2, 4)
            # 轮子
            pyxel.pset(screen_x + 2, screen_y + 7, 0)
            pyxel.pset(screen_x + 9, screen_y + 7, 0)
            # 闪烁效果（提示可收集）
            if pyxel.frame_count % 30 < 15:
                pyxel.circb(screen_x + 6, screen_y + 4, 8, 10)
    
    def _draw_weather(self):
        """绘制天气效果"""
        if self.current_weather == 'sunny':
            # 晴天 - 无特效
            pass
                
        elif self.current_weather == 'rain':
            # 下雨 - 只绘制雨滴
            for particle in self.weather_particles:
                x, y = int(particle['x']), int(particle['y'])
                if 0 <= y < WINDOW_HEIGHT:
                    pyxel.line(x, y, x + 1, y + 4, 12)  # 蓝色雨滴
                    
        elif self.current_weather == 'snow':
            # 下雪 - 只绘制雪花
            for particle in self.weather_particles:
                x, y = int(particle['x']), int(particle['y'])
                size = particle['size']
                if 0 <= y < WINDOW_HEIGHT:
                    pyxel.pset(x, y, 7)  # 白色雪花
                    if size > 1:
                        pyxel.pset(x + 1, y, 7)
                        pyxel.pset(x, y + 1, 7)
                    if size > 2:
                        pyxel.pset(x - 1, y, 7)
                        pyxel.pset(x, y - 1, 7)
    
    def _draw_mosque_interior(self):
        """绘制清真寺内部"""
        # 背景 - 米色地板
        pyxel.cls(15)
        
        # 地板瓷砖图案
        for y in range(0, WINDOW_HEIGHT, 32):
            for x in range(0, WINDOW_WIDTH, 32):
                pyxel.rectb(x, y, 32, 32, 6)
                # 伊斯兰几何图案
                pyxel.pset(x + 16, y + 16, 10)
                pyxel.rect(x + 14, y + 14, 4, 4, 10)
        
        # 墙壁 - 四周
        wall_color = 7  # 白色墙
        wall_decor = 10  # 金色装饰
        
        # 上墙（有精美图案）
        pyxel.rect(0, 0, WINDOW_WIDTH, 35, wall_color)
        pyxel.rect(0, 30, WINDOW_WIDTH, 5, wall_decor)
        # 伊斯兰拱形装饰
        for i in range(5):
            arch_x = 30 + i * 50
            pyxel.circ(arch_x, 20, 15, 12)
            pyxel.circ(arch_x, 22, 12, wall_color)
            pyxel.tri(arch_x, 5, arch_x - 8, 20, arch_x + 8, 20, 12)
        
        # 左墙
        pyxel.rect(0, 0, 35, WINDOW_HEIGHT, wall_color)
        pyxel.rect(30, 0, 5, WINDOW_HEIGHT, wall_decor)
        # 窗户
        for y in [60, 120, 180]:
            pyxel.rect(8, y, 16, 24, 12)
            pyxel.rectb(8, y, 16, 24, wall_decor)
            pyxel.line(16, y, 16, y + 24, wall_decor)
        
        # 右墙
        pyxel.rect(WINDOW_WIDTH - 35, 0, 35, WINDOW_HEIGHT, wall_color)
        pyxel.rect(WINDOW_WIDTH - 35, 0, 5, WINDOW_HEIGHT, wall_decor)
        # 窗户
        for y in [60, 120, 180]:
            pyxel.rect(WINDOW_WIDTH - 24, y, 16, 24, 12)
            pyxel.rectb(WINDOW_WIDTH - 24, y, 16, 24, wall_decor)
            pyxel.line(WINDOW_WIDTH - 16, y, WINDOW_WIDTH - 16, y + 24, wall_decor)
        
        # 下墙（有出口门）
        pyxel.rect(0, WINDOW_HEIGHT - 35, WINDOW_WIDTH, 35, wall_color)
        pyxel.rect(0, WINDOW_HEIGHT - 35, WINDOW_WIDTH, 5, wall_decor)
        # 出口门
        door_x = WINDOW_WIDTH // 2 - 20
        pyxel.rect(door_x, WINDOW_HEIGHT - 35, 40, 30, 4)  # 棕色门
        pyxel.circ(door_x + 20, WINDOW_HEIGHT - 35, 20, 4)  # 拱形顶
        pyxel.rectb(door_x, WINDOW_HEIGHT - 35, 40, 30, 9)
        
        # 中央祈祷大厅装饰
        # 吊灯
        chandelier_x = WINDOW_WIDTH // 2
        chandelier_y = 60
        pyxel.circ(chandelier_x, chandelier_y, 20, 10)
        pyxel.circ(chandelier_x, chandelier_y, 15, 9)
        pyxel.line(chandelier_x, 35, chandelier_x, chandelier_y - 15, 10)
        # 吊灯光芒
        for i in range(8):
            import math
            angle = i * math.pi / 4
            px = chandelier_x + int(12 * math.cos(angle))
            py = chandelier_y + int(12 * math.sin(angle))
            pyxel.pset(px, py, 7)
        
        # 地毯
        carpet_x = 60
        carpet_y = 100
        carpet_w = WINDOW_WIDTH - 120
        carpet_h = 80
        pyxel.rect(carpet_x, carpet_y, carpet_w, carpet_h, 8)  # 红色地毯
        pyxel.rectb(carpet_x, carpet_y, carpet_w, carpet_h, 9)
        pyxel.rectb(carpet_x + 4, carpet_y + 4, carpet_w - 8, carpet_h - 8, 10)
        # 地毯图案
        for i in range(3):
            pattern_x = carpet_x + 30 + i * 50
            pattern_y = carpet_y + carpet_h // 2
            pyxel.circ(pattern_x, pattern_y, 12, 9)
            pyxel.circ(pattern_x, pattern_y, 8, 10)
        
        # 绘制玩家（室内无相机偏移）
        self.player.draw(0, 0)
        
        # 提示文字
        hint = "阿拉伯语学院内部 - 向下走离开"
        draw_text(WINDOW_WIDTH // 2 - text_width(hint) // 2, WINDOW_HEIGHT - 20, hint, 0)
        
    def _draw_hud(self):
        """绘制界面信息"""
        # 显示当前区域名称
        if self.current_map == MAP_LIBRARY:
            location_name = "北外图书馆"
        elif self.in_mosque:
            location_name = "阿拉伯语学院"
        elif self.current_map == MAP_TUNNEL:
            location_name = "地下通道"
        else:
            # 东校区：检测玩家附近的建筑
            location_name = self._get_nearby_building_name()
        
        # 区域名称背景
        name_width = text_width(location_name) + 12
        pyxel.rect(2, 2, name_width, 16, 0)
        pyxel.rectb(2, 2, name_width, 16, 5)
        draw_text(8, 5, location_name, COLOR_WHITE)
        
        # 进球消息
        if self.goal_message_timer > 0:
            msg_x = WINDOW_WIDTH // 2 - text_width(self.goal_message) // 2
            msg_y = WINDOW_HEIGHT // 2 - 20
            # 闪烁背景
            if self.goal_message_timer % 10 < 5:
                pyxel.rect(msg_x - 4, msg_y - 2, text_width(self.goal_message) + 8, 16, 10)
            else:
                pyxel.rect(msg_x - 4, msg_y - 2, text_width(self.goal_message) + 8, 16, 8)
            draw_text(msg_x, msg_y, self.goal_message, 7)
        
        # 花朵收集提示
        if self.collect_message_timer > 0:
            msg_x = WINDOW_WIDTH // 2 - text_width(self.collect_message) // 2
            msg_y = 50
            # 绿色背景
            pyxel.rect(msg_x - 6, msg_y - 4, text_width(self.collect_message) + 12, 18, 3)
            pyxel.rectb(msg_x - 6, msg_y - 4, text_width(self.collect_message) + 12, 18, 11)
            draw_text(msg_x, msg_y, self.collect_message, 7)
        
        # 操作提示（对话时隐藏）
        if not self.npc_manager.is_in_dialogue() and not self.ai_dialogue.active:
            hint = "方向/WASD/手柄:移动 A:对话 Start/M:菜单"
            # 如果有滑板，添加滑板提示
            if self.player.has_skateboard:
                if self.player.skateboard_mode:
                    hint = "方向/WASD:移动 B键/手柄X:下滑板 A:对话 Start/M:菜单"
                    # 显示滑板模式指示
                    mode_text = "🛹滑板模式"
                    draw_text(4, WINDOW_HEIGHT - 28, mode_text, 10)
                else:
                    hint = "方向/WASD:移动 B键/手柄X:滑板 A:对话 Start/M:菜单"
            draw_text(WINDOW_WIDTH - text_width(hint) - 4, WINDOW_HEIGHT - 14, hint, 7)
        
    def _get_nearby_building_name(self):
        """检测玩家附近的建筑物并返回名称"""
        # 获取玩家当前瓦片位置
        player_tile_x = int(self.player.x // TILE_SIZE)
        player_tile_y = int(self.player.y // TILE_SIZE)
        
        # 检查周围3x3范围内的瓦片
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                check_x = player_tile_x + dx
                check_y = player_tile_y + dy
                
                # 边界检查
                if 0 <= check_x < MAP_TILES_WIDTH and 0 <= check_y < MAP_TILES_HEIGHT:
                    tile = CAMPUS_MAP[check_y][check_x]
                    
                    # 根据瓦片类型返回建筑名称
                    if tile in [TILE_DOME, TILE_DOME_ARCH]:
                        return "阿拉伯语学院"
                    elif tile in [TILE_LIBRARY, TILE_LIBRARY_WINDOW]:
                        return "图书馆"
                    elif tile == TILE_CANTEEN:
                        return "食堂"
                    elif tile == TILE_ADMIN:
                        return "行政楼"
                    elif tile == TILE_HALL:
                        return "礼堂"
                    elif tile == TILE_GYM:
                        return "体育馆"
                    elif tile == TILE_JAPAN:
                        return "日研中心"
                    elif tile == TILE_MAIN:
                        return "主楼"
                    elif tile == TILE_WATER:
                        return "小碧池"
        
        # 默认显示东校区
        return "东校区"
